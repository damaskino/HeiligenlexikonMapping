from typing import List, Dict

from bs4 import BeautifulSoup
from tqdm import tqdm
import time
import joblib
import os
import sys
import json
import re
import stanza

from src.saint_alias_extraction import get_saint_aliases
from src.occupation_extraction import (
    extract_occupation,
    setup_occupation_list,
    setup_occupation_dict,
    get_occupation_category,
)
from src.parse_dates import convert_date
from src.regex_matching import (
    match_saint_name,
    match_canonization,
    match_second_hlex_number,
    match_hlex_number,
    match_raw_feast_day,
)


class HlexParser:
    def __init__(
            self,
            no_nlp=False,
            occupation_list=None,
            occupations_dict=None,
            include_raw_text=False,
    ):
        self.no_nlp = no_nlp
        if no_nlp:
            self.nlp = None
            self.gender_nlp = None
        else:
            self.nlp = self.setup_tokenizer_nlp()
            self.gender_nlp = self.setup_gender_nlp()
        self.occupation_list: List = occupation_list
        self.occupation_dict: Dict = occupations_dict
        self.include_raw_entry = include_raw_text

    def setup_tokenizer_nlp(self):
        stanza.download("de")
        nlp = stanza.Pipeline(lang="de", processors="tokenize")
        return nlp

    def setup_gender_nlp(self):
        stanza.download("de")
        nlp = stanza.Pipeline(lang="de", processors="tokenize,mwt,pos")
        return nlp

    def load_transformed_hlex_to_soup(self, hlex_xml_path):
        with open(hlex_xml_path, "r", encoding="utf-8") as hlex:
            soup = BeautifulSoup(hlex, features="xml")
            return soup

    def pickle_it(self, object_to_pickle, path: str):
        print("Attempting to pickle...")
        with open(path, "wb") as target_file:
            joblib.dump(value=object_to_pickle, filename=target_file)

    # the term of the entry contains the name of the saint and their canonization status
    # which is usually one variant of: S., B., V. (Sanctus, Beati or Veritit)
    def parse_term(self, term):
        raw_term = term.text
        # print("Raw:")
        # print(raw_term)

        saint_name = match_saint_name(raw_term)
        canonization_status = match_canonization(raw_term)
        hlex_number = match_hlex_number(raw_term)
        second_hlex_number = match_second_hlex_number(raw_term)
        return saint_name, canonization_status, hlex_number

    # The paragraph contains free form text, but often starts with the feast day if it is available,
    # May also contain occupation of saint
    def parse_paragraph(self, paragraph_list):
        raw_occupation = None
        occupation_category = None
        parsed_feast_days = None
        paragraph = paragraph_list[0]
        superscripts = paragraph.find_all("hi", rend="superscript")
        for superscript in superscripts:
            superscript.decompose()
        raw_paragraph = paragraph.text
        raw_feast_day = match_raw_feast_day(raw_paragraph)
        if raw_feast_day:
            try:
                parsed_feast_days = convert_date(raw_feast_day)
                parsed_feast_days = [
                    f"{date_dict['Day']}.{date_dict['Month']}."
                    for date_dict in parsed_feast_days
                ]
            except:
                parsed_feast_days = []
        occupation = extract_occupation(raw_paragraph, self.occupation_list)
        raw_occupation = occupation
        occupation_category = get_occupation_category(
            occupation=occupation, occupation_dict=self.occupation_dict
        )

        return raw_feast_day, parsed_feast_days, raw_occupation, occupation_category

    def parse_entry(self, entry):
        # namespace is found on linux, not in windows, maybe a module version error?
        # term_list = entry.find_all('tei:term')
        term_list = entry.find_all("term")
        entry_id = entry.get("xml:id")
        # print(term_list)
        entry_dict = {}
        # paragraph_list = entry.find_all('tei:p')
        paragraph_list = entry.find_all("p")
        # Assuming only one term per entry, give warning when finding other
        # print("Looking at entry: ", entry_id)
        # print(entry)
        if len(term_list) > 1:
            print(f"Error, found more than one term in entry {entry_id}!")
            sys.exit()
        else:
            # print(term_list)
            term = term_list[0]
            saint_name, canonization_status, hlex_number = self.parse_term(term)
            gender = None
            if self.no_nlp:
                gender = None
            else:
                gender = predict_gender(saint_name, nlp=self.gender_nlp)
            entry_dict["SaintName"] = saint_name
            entry_dict["CanonizationStatus"] = canonization_status
            entry_dict["NumberInHlex"] = hlex_number
            entry_dict["Gender"] = gender
            entry_dict["EntryLength"] = get_entry_length(paragraph_list)
            if self.include_raw_entry:
                entry_dict["OriginalText"] = entry.text

            # looking only at first paragraph for now, may consider looking at more later
            if paragraph_list:
                (
                    raw_feast_day,
                    parsed_feast_days,
                    raw_occupation,
                    occupation_category,
                ) = self.parse_paragraph(paragraph_list)
                entry_dict["RawFeastDay"] = raw_feast_day
                if parsed_feast_days:
                    for index, feast_day in enumerate(parsed_feast_days):
                        entry_dict["FeastDay" + str(index)] = feast_day
                entry_dict["Ocupation"] = occupation_category
                entry_dict["RawOccupation"] = raw_occupation

                text_to_parse = ""
                if self.no_nlp:
                    text_to_parse = paragraph_list[0].text

                else:
                    doc = self.nlp(paragraph_list[0].text)
                    first_sentence = doc.sentences[0]
                    tokenized_sentence = [token.text for token in first_sentence.tokens]
                    tokenized_sentence_text = " ".join(tokenized_sentence)
                    text_to_parse = tokenized_sentence_text
                aliases = None

                aliases = get_saint_aliases(saint_name, text_to_parse)
                entry_dict["Aliases"] = aliases
            else:
                entry_dict["FeastDay"] = None
                entry_dict["Occupation"] = None

            return entry_id, entry_dict

    def parse_soup(self, soup):
        entries = soup.find_all("entry")
        data = {}
        for e in tqdm(entries[:]):
            try:
                entry_id, entry_dict = self.parse_entry(e)
            except Exception as e:
                print("Error parsing entry: ", entry_id)
                e.print(Exception, e)
            if entry_id in data.keys():
                print("ERROR: Duplicate entry id found!", entry_id)
                sys.exit()

            data[entry_id] = entry_dict

        self.write_dict_to_json(data)

    @classmethod
    def write_dict_to_json(cls, data: dict):
        json_data = json.dumps(data)
        with open("../outputs_to_review/parsed_heiligenlexikon.json", "w") as json_file:
            json_file.write(json_data)


def timing_wrapper(func, param):
    start = time.time()
    value = None
    if param:
        value = func(param)
    else:
        print("no param found, running function without params")
        value = func()
    end = time.time()
    print("Finished after ", end - start)
    return value


def predict_gender(input_name: str, nlp):
    # Assuming that this will always yield the first name
    input_split = input_name.split(" ")
    if input_split[0] != "S.":
        input_name = input_split[0]
    else:
        input_name = input_split[1]

    gender_pattern = re.compile(r"Gender=(\w+)")
    doc = nlp(input_name)
    extracted_gender = None
    # print(doc)
    feats = doc.get("feats")
    if len(feats) == 0:
        return None
    if feats[0] == None:
        return None
    # print(feats)
    feats_str = feats[0]
    if "Gender" in feats_str:
        # print("found gender")
        gender_match = re.search(gender_pattern, feats_str)
        if gender_match:
            extracted_gender = gender_match.group(1)
    return extracted_gender


def get_entry_length(paragraph_list):
    full_text = ""
    for paragraph in paragraph_list:
        full_text += paragraph.text
    return len(full_text)


if __name__ == "__main__":
    HLEX_SOUP_PICKLE = "hlex_soup.pickle"

    occupations = setup_occupation_list("../resources/occupation_list.txt")
    occupations_dict = setup_occupation_dict("../resources/occupation_list.txt")
    # hlex_parser = HlexParser(
    #     no_nlp=True, occupation_list=occupations, occupations_dict=occupations_dict
    # )
    hlex_parser = HlexParser(
        no_nlp=False,
        occupation_list=occupations,
        occupations_dict=occupations_dict,
        include_raw_text=True,
    )

    hlex_soup = None

    if os.path.isfile("tmp/" + HLEX_SOUP_PICKLE):
        print("Pickle found, loading...")
        with open("tmp/" + HLEX_SOUP_PICKLE, "rb") as pickle_file:
            hlex_soup = timing_wrapper(joblib.load, pickle_file)
            # print("Hlex_soup is: ")
            # print(hlex_soup)
    else:
        print("No pickle found, loading from XML...")
        hlex_soup = timing_wrapper(hlex_parser.load_transformed_hlex_to_soup, "../data/Heiligenlex-1858.xml")
        print("Size of Hlex Object: ", sys.getsizeof(hlex_soup))
        hlex_parser.pickle_it(hlex_soup, "tmp/" + HLEX_SOUP_PICKLE)
    print("Loaded", hlex_soup.title.text)
    hlex_parser.parse_soup(hlex_soup)
