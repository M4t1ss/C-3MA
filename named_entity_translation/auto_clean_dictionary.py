#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import argparse
import codecs
import pickle
import re

def parse_args():
    """parses arguments given when program is called"""

    parser = argparse.ArgumentParser()

    # dictionary for cleaning
    parser.add_argument("-d", "--dictionary",  required=True, action="store", dest="dic", help="pickle file storing src-trg NE dictionary")

    return parser.parse_args()

def main(args):
    """main function to help clean dictionary"""

    # read NE dictionary
    with codecs.open(args.dic, "r" ) as opened:
        dic = pickle.load(opened)
        for key, values in dic.copy().items():

            for index,value in zip(range(len(values)-1,-1,-1),values[::-1]):

                if checkValue(key, value[0]):
                        del dic[key][index]

            if dic[key] == []:
                del dic[key]
    try:
        with codecs.open(args.dic,"w") as clean:
            pickle.dump(dic,clean)
    except:
        print "Saving dictionary failed"


def checkValue(key, value):
    #Remove any dictionary entry that contains any of the following symbols
    badThings = [";", ",", ")", "(", "]", "[", "/", "\\"]
    if (
            #Remove very long dictionary entries
            len(key) > 70 or
            len(value) > 70 or
            #Remove dictionary entries with too different lengths
            len(key) > len(value) + 15 or
            len(value) > len(key) + 15 or
            #Remove dictionary entries with too many words
            len(key.split()) > 5 or
            len(value.split()) > 5 or
            #Remove dictionary entries with too different word counts
            len(value.split()) > len(key.split()) + 2 or
            len(key.split()) > len(value.split()) + 2 or
            #Remove dictionary entries that start with a dash
            key[:1] == "-" or
            value[:1] == "-" or
            #Remove dictionary entries that don't contain any alphabetical characters
            re.search('^[^a-zA-Z]*$', key) or
            re.search('^[^a-zA-Z]*$', value) or
            #Remove any dictionary entry that contains any of the mentioned symbols
            any(badThing in key for badThing in badThings) or
            any(badThing in value for badThing in badThings)
        ):
        return True

    return False

if __name__ == "__main__":

    args = parse_args()
    main(args)
