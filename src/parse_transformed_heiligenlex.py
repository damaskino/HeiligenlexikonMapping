from typing import List

from bs4 import BeautifulSoup
import time
import joblib
import os
import sys
import json
import re
import stanza


class HlexParser():
    def __init__(self, nlp=None, occupation_list=None, include_raw_text=False):
        self.nlp = nlp
        self.occupation_list: List = occupation_list
        self.include_raw_entry = include_raw_text

    def setup_nlp(self):
        stanza.download('de')
        nlp = stanza.Pipeline('de')
        self.nlp = nlp

    def setup_occupation_list(self):
        with open("occupation_list.txt", "r") as occupation_file:
            tmp_occupation_list = occupation_file.readlines()
            for item in tmp_occupation_list:
                if item.startswith('#'):
                    continue
                occupation_list.append(item.strip())

            self.occupation_list = occupation_list

    def load_transformed_hlex_to_soup(self):
        hlex_xml_path = '../data/Heiligenlex-1858.xml'
        with open(hlex_xml_path, 'r', encoding='utf-8') as hlex:
            soup = BeautifulSoup(hlex, features="xml")
            return soup

    def pickle_it(self, object_to_pickle, path: str):
        print("Attempting to pickle...")
        with open(path, 'wb') as target_file:
            joblib.dump(value=object_to_pickle, filename=target_file)

    def extract_gender(self, input_name: str):
        # Assuming that this will always yield the first name
        input_split = input_name.split(" ")
        if input_split[0] != "S.":
            input_name = input_split[0]
        else:
            input_name = input_split[1]

        gender_pattern = re.compile(r"Gender=(\w+)")
        doc = self.nlp(input_name)
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
            print("found gender")
            gender_match = re.search(gender_pattern, feats_str)
            if gender_match:
                extracted_gender = gender_match.group(1)
        return extracted_gender

    def extract_occupation(self, paragraph_list):
        occupation = None
        # only look at the first two paragraphs for now

        # print("Full paragraph list")
        # print(paragraph_list)

        # print("First paragraph")
        # print(paragraph_list[0])
        first_paragraph_text = paragraph_list[0].text

        # print(paragraph_list[1])

        # for item in occupation_list:
        #     if item.lower() in paragraph_text.lower():
        #         occupation = item
        #         continue
        doc = self.nlp(first_paragraph_text)
        # print(doc)
        doc.sentences[0].print_dependencies()

        second_paragraph_text = paragraph_list[1].text
        # print("Second paragraph")
        # print(second_paragraph_text)
        doc2 = self.nlp(second_paragraph_text)
        doc2.sentences[0].print_dependencies()
        for sentence in doc2.sentences:
            sentence.print_dependencies()
        # print(doc2.entities)

        third_paragraph_text = paragraph_list[2].text
        # print("Third paragraph")
        # print(third_paragraph_text)
        # doc3 = nlp(third_paragraph_text)
        # doc3.sentences[0].print_dependencies()

        fourth_paragraph_text = paragraph_list[3].text
        # print("Fourth paragraph")
        # print(fourth_paragraph_text)

        # sys.exit()
        return occupation

    # the term of the entry contains the name of the saint and their title, usually one variant of: S., B., V. (Sanctus, Beati or Veritit
    def parse_term(self, term):
        raw_term = term.text
        print("Raw:")
        print(raw_term)

        saint_name = None
        canonization_status = None
        hlex_number = None
        footnote = None

        gender = None

        saint_pattern = r"((\w|\s)+\w)\,?\(?"
        canonization_pattern = r"[A-Z]+\."
        number_pattern = r"\(.*\)"
        footnote_pattern = r"\[.*\]"

        saint_match = re.search(saint_pattern, raw_term)
        if saint_match:
            saint_name = saint_match.group(1)
            gender = self.extract_gender(saint_name)
        else:
            print("No match found for ", raw_term)
            sys.exit()

        canonization_match = re.search(canonization_pattern, raw_term)
        if canonization_match:
            canonization_status = canonization_match.group()

        num_match = re.search(number_pattern, raw_term)
        if num_match:
            hlex_number = num_match.group()

        footnote_match = re.search(footnote_pattern, raw_term)
        if footnote_match:
            footnote = footnote_match.group()

        print("----------")
        print(saint_name)
        if canonization_status:
            print(canonization_status)
        if hlex_number:
            print(hlex_number)
        if footnote:
            print(footnote)
            if hlex_number:
                hlex_number = hlex_number + " " + footnote
            else:
                hlex_number = footnote
        print("\n")
        return saint_name, canonization_status, hlex_number, gender

    # The paragraph contains free form text, but often starts with the feast day if it is available,
    # May also contain occupation of saint
    def parse_paragraph(self, paragraph_list):
        paragraph = paragraph_list[0]
        feast_day_pattern = r"\(.?[0-9][0-9]?.*?\)"
        raw_paragraph = paragraph.text

        feast_day = None

        feast_day_match = re.search(feast_day_pattern, raw_paragraph)
        if feast_day_match:
            feast_day = feast_day_match.group()

        # occupation = extract_occupation(paragraph_list)
        occupation = None
        return feast_day, occupation

    def parse_entry(self, entry):
        # namespace is found on linux, not in windows, maybe a module version error?
        # term_list = entry.find_all('tei:term')
        term_list = entry.find_all('term')
        entry_id = entry.get('xml:id')

        # print(term_list)
        entry_dict = {}
        # paragraph_list = entry.find_all('tei:p')
        paragraph_list = entry.find_all('p')
        # Assuming only one term per entry, give warning when finding other
        print("Looking at entry: ", entry_id)
        print(entry)
        if len(term_list) > 1:
            print(f"Error, found more than one term in entry {entry_id}!")
            sys.exit()
        else:
            print(term_list)
            term = term_list[0]
            saint_name, canonization_status, hlex_number, gender = self.parse_term(term)
            entry_dict['SaintName'] = saint_name
            entry_dict['CanonizationStatus'] = canonization_status
            entry_dict['NumberInHlex'] = hlex_number
            entry_dict['Gender'] = gender
            if self.include_raw_entry:
                entry_dict['OriginalText'] = entry.text

            # TODO looking only at first paragraph for now, will have to look at more later
            if paragraph_list:

                feast_day, occupation = self.parse_paragraph(paragraph_list)
                entry_dict['FeastDay'] = feast_day
                entry_dict['Ocupation'] = occupation
            else:
                entry_dict['FeastDay'] = None
                entry_dict['Occupation'] = None

            return entry_id, entry_dict

    def parse_soup(self, soup):
        entries = soup.find_all('entry')
        data = {}
        for e in entries[:]:
            entry_id, entry_dict = self.parse_entry(e)

            if entry_id in data.keys():
                print("ERROR: Duplicate entry id found!", entry_id)
                sys.exit()

            data[entry_id] = entry_dict

        self.write_dict_to_json(data)

    @classmethod
    def write_dict_to_json(cls, data: dict):

        json_data = json.dumps(data)
        with open('../outputs_to_review/parsed_heiligenlexikon.json', 'w') as json_file:
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


if __name__ == '__main__':

    HLEX_SOUP_PICKLE = 'hlex_soup.pickle'
    occupation_list = []

    hlex_parser = HlexParser()

    hlex_soup = None
    hlex_parser.setup_nlp()
    hlex_parser.setup_occupation_list()

    if os.path.isfile('tmp/' + HLEX_SOUP_PICKLE):
        print("Pickle found, loading...")
        with open('tmp/' + HLEX_SOUP_PICKLE, 'rb') as pickle_file:
            hlex_soup = timing_wrapper(joblib.load, pickle_file)
            # print("Hlex_soup is: ")
            # print(hlex_soup)
    else:
        print("No pickle found, loading from XML...")
        hlex_soup = timing_wrapper(hlex_parser.load_transformed_hlex_to_soup, None)
        print("Size of Hlex Object: ", sys.getsizeof(hlex_soup))
        hlex_parser.pickle_it(hlex_soup, "tmp/" + HLEX_SOUP_PICKLE)
    print("Loaded", hlex_soup.title.text)
    hlex_parser.parse_soup(hlex_soup)
