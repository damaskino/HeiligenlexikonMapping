from bs4 import BeautifulSoup
import time
import pickle
import os
import sys

HLEX_SOUP_PICKLE = 'hlex_soup.pickle'

def load_transformed_hlex_to_soup():
    hlex_xml_path = '../data/Heiligenlex-1858.xml'
    with open(hlex_xml_path, 'r') as hlex:
        soup = BeautifulSoup(hlex, 'lxml')
        return soup

def pickle_it(object_to_pickle, path: str):
    print("Attempting to pickle...")
    with open(path, 'wb') as target_file:
        pickle.dump(obj=object_to_pickle, file=target_file, protocol=pickle.HIGHEST_PROTOCOL)

def timing_wrapper(func, param):
    start = time.time()
    value = None
    if param:
        value = func(param)
    else:
        value = func()
    end = time.time()
    print("Finished after ", end-start)
    return value

if __name__ == '__main__':
    hlex_soup = None
    sys.setrecursionlimit(sys.getrecursionlimit()*50)
    print("Attempting with recursionlimit:", sys.getrecursionlimit())
    #TODO: Add a check to see if pickle is corrupt
    if os.path.isfile('tmp/'+HLEX_SOUP_PICKLE):
        print("Pickle found, loading...")
        with open('tmp/' + HLEX_SOUP_PICKLE, 'rb') as pickle_file:
            pickle.load(pickle_file)
            hlex_soup = timing_wrapper(pickle.load, pickle_file)
    else:
        print("No pickle found, loading from XML...")
        hlex_soup = timing_wrapper(load_transformed_hlex_to_soup, None)
        print("Size of Hlex Object: ",sys.getsizeof(hlex_soup))
        pickle_it(hlex_soup, "tmp/"+HLEX_SOUP_PICKLE)

    print(hlex_soup.title)