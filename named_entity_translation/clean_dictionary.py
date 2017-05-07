#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# imported modules
import argparse
import codecs
import pickle

################################################################################

def parse_args():
    """parses arguments given when program is called"""

    parser = argparse.ArgumentParser()

    # dictionary for cleaning
    parser.add_argument("-d", "--dictionary",  required=True, action="store", dest="dic", help="pickle file storing src-trg NE dictionary")

    return parser.parse_args()


################################################################################

def print_options():

        print "\nOptions to clean dictionary:"
        print "\t- print entry (p)"
        print "\t- overwrite entry (o)"
        print "\t- add additional translation to dictionary entry (a)"
        print "\t- delete entry (d)"
        print "\t- quit (q)\n"


################################################################################

def main(args):
    """main function to help clean dictionary"""

    # read NE dictionary
    with codecs.open(args.dic, "r" ) as opened:
        dic = pickle.load(opened)

    cleaning = True

    print_options()

    while cleaning:

        option = unicode(raw_input("Choose option: "))
        print

        if option not in ["q","o","a","d","p"]:
            print option,"is an invalid option!"
            print_options()
            continue

        elif option == "q":
            cleaning = False
            continue

        elif option == "p":
            key = raw_input("Which entry would you like to see?: ").decode("utf-8")
            print key, ": ", dic[key]
            print
            continue

        elif option == "o":
            key = raw_input("Which entry should be overwritten: ").decode("utf-8")
            val = raw_input("What is the new translation of this source word?: ").decode("utf-8")

            dic[key] = [(val,1)]
            print
            continue

        elif option == "a":
            key = raw_input("For which source word do you want to add a translation: ").decode("utf-8")
            val = raw_input("What value should be added to this key?: ").decode("utf-8")

            if key not in dic:
                dic[key] = [(val,1)]
            else:
                dic[key].append((val,1))
            print
            continue

        elif option == "d":
            key = raw_input("Which entry do you want to delete?: ").decode("utf-8")

            if key in dic:
                del dic[key]
            print
            continue


    try:
        with codecs.open(args.dic,"w") as clean:
            pickle.dump(dic,clean)
    except:
        print "Saving dictionary failed"


################################################################################

if __name__ == "__main__":

    args = parse_args()
    main(args)
