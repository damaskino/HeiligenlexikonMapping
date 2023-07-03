from bs4 import BeautifulSoup
import time
import joblib
import os
import sys

HLEX_SOUP_PICKLE = 'hlex_soup.pickle'

def load_transformed_hlex_to_soup():
    hlex_xml_path = '../data/Heiligenlex-1858.xml'
    with open(hlex_xml_path, 'r') as hlex:
        soup = BeautifulSoup(hlex, features="xml")
        return soup

def pickle_it(object_to_pickle, path: str):
    print("Attempting to pickle...")
    with open(path, 'wb') as target_file:
        joblib.dump(value=object_to_pickle, filename=target_file)

def timing_wrapper(func, param):
    start = time.time()
    value = None
    if param:
        value = func(param)
    else:
        print("no param found, running function without params")
        value = func()
    end = time.time()
    print("Finished after ", end-start)
    return value

#the term of the entry contains the name of the saint and their title, usually one of: S. (Sanctus, Beati or Veritit
def parse_term(term):
    #print("Parsing term: ")
    #print(term)
    #print(type(term))
    raw_term = term.text
    print("Raw:")
    print(raw_term)

    saint_name = None
    canonization_status = None
    hlex_number = None

    if "," in raw_term:
        raw_term_split = raw_term.split(",")
        before_comma = raw_term_split[0]
        after_comma = raw_term_split[1]

        saint_name = before_comma
        after_comma = after_comma.strip()
        after_comma_split = after_comma.split(" ")

        if len(after_comma_split) == 1:
            hlex_number = after_comma_split[0]
        if len(after_comma_split) == 2:
            canonization_status = after_comma_split[0]
            hlex_number = after_comma_split[1]

    else:
        #TODO: does not catch the case where it's a saint with a number but no canonization status, also long names with
        # lots of whitespaces are a problem, try regex for that case
        raw_term_split = raw_term.split(" ")
        saint_name = raw_term_split[0]

        if len(raw_term_split) > 1:
            canonization_status = raw_term_split[1]
        if len(raw_term_split) > 2:
            hlex_number = raw_term_split[2]

    print("Parsed:")
    print(saint_name)
    if canonization_status:
        print(canonization_status)
    if hlex_number:
        print(hlex_number)
    print("\n")

def parse_entry(entry):
    term_list = entry.find_all('tei:term')
    #print(term_list)
    #Assuming only one term per entry, give warning when finding other
    if len(term_list) > 1:
        print("Error, found more than one term in an entry!")
        sys.exit()
    else:
        term = term_list[0]
        parse_term(term)

def parse_soup(soup):
    entries = soup.find_all('entry')
    for e in entries[:]:
        parse_entry(e)
        #print(type(e))


if __name__ == '__main__':
    hlex_soup = None
    #sys.setrecursionlimit(sys.getrecursionlimit()*50)
    #print("Attempting with recursionlimit:", sys.getrecursionlimit())
    #TODO: Add a check to see if pickle file is corrupt
    if os.path.isfile('tmp/'+HLEX_SOUP_PICKLE):
        print("Pickle found, loading...")
        with open('tmp/' + HLEX_SOUP_PICKLE, 'rb') as pickle_file:
            hlex_soup = timing_wrapper(joblib.load, pickle_file)
            #print("Hlex_soup is: ")
            #print(hlex_soup)
    else:
        print("No pickle found, loading from XML...")
        hlex_soup = timing_wrapper(load_transformed_hlex_to_soup, None)
        print("Size of Hlex Object: ",sys.getsizeof(hlex_soup))
        pickle_it(hlex_soup, "tmp/"+HLEX_SOUP_PICKLE)
    print("Loaded", hlex_soup.title.text)
    parse_soup(hlex_soup)