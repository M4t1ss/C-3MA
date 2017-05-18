#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals


# imported modules
from nltk import ne_chunk, pos_tag, word_tokenize
import os
import re
import codecs
import argparse
import sys
import spacy


################################################################################

def parse_args():
    """parses the arguments given when program is called"""

    parser = argparse.ArgumentParser()

    parser.add_argument("-f", "--folder",  required=True, action="store", dest="folder", help="input folder")
    parser.add_argument("-t", "--tool",  required=True, action="store", dest="tool", choices=["spacy","stanford"], help="NER tool")
    parser.add_argument("-l", "--lang",  required=True, action="store", dest="lang", help="language")

    return parser.parse_args()

################################################################################


def ner_nltk(filepath):
    """performs named entity recognition on given file with stanford NER tool"""

    out = ""

    with codecs.open(filepath,'r','utf-8') as current_file:

        text = current_file.readlines()

    with codecs.open(filepath+".ner",'w','utf-8') as outfile:

        for line in text:

            tokenized = line.split()
            tagged = pos_tag(tokenized)
            ne = ne_chunk(tagged)

            for index,token in enumerate(ne):
                if type(token) != tuple:
                    outfile.write(' '.join([tok[0]+"|"+token.label() for tok in token])+' ')
                else:
                    outfile.write(token[0]+' ')
            outfile.write('\n')

################################################################################

def ner_spacy(filepath):
    """performs named entity recognition on given file with spacy"""


    out = ""

    with codecs.open(filepath,'r','utf-8') as current_file:

        text = current_file.readlines()

    with codecs.open(filepath+".ner",'w','utf-8') as outfile:

        for line in text:
            doc = nlp(line.rstrip())
            for word in doc:
                if word.ent_type_ != u"":
                    outfile.write(word.text+"|"+word.ent_type_+' ')
                else:
                    outfile.write(word.text+' ')
            outfile.write('\n')


################################################################################

def main():
    "main function -- processes all documents in a given folder"

    args = parse_args()
    tool = args.tool
    global lang
    lang = args.lang

    if tool == "stanford":
        ner = ner_nltk
    elif tool == "spacy":
        global nlp
        nlp = spacy.load(lang)
        ner = ner_spacy

    if args.folder[-1] == "/":
        args.folder = args.folder[:-1]

    for f in os.listdir(args.folder):

        if f.endswith(lang):

            filepath = args.folder + "/" + f
            ner(filepath)


################################################################################


if __name__ == "__main__":

    main()
