#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

__author__ = "Chantal Amrhein <chantal.amrhein@uzh.ch>"

# imported modules
import os
import re
import codecs
import argparse
import sys
from collections import defaultdict
import pickle
from nltk import FreqDist


################################################################################

def parse_args():
    """parses the arguments given when program is called"""

    parser = argparse.ArgumentParser()

    parser.add_argument("-s", "--source",  required=True, action="store", dest="src", help="source NE file")
    parser.add_argument("-t", "--target",  required=True, action="store", dest="trg", help="traget NE file")
    parser.add_argument("-a", "--alignments",  required=True, action="store", dest="alg", help="alignment file")

    return parser.parse_args()


################################################################################

def main():
    "main function -- processes all documents in a given folder"

    args = parse_args()

    # initialise counter for some status message
    counter = 0

    # open all files
    with codecs.open(args.src,'r','utf-8') as src:
        with codecs.open(args.trg,'r','utf-8') as trg:
            with codecs.open(args.alg,'r','utf-8') as alg:

                # initialise the dictionaries
                src_dic = defaultdict(list)
                trg_dic = defaultdict(list)

                # read first line
                sline = src.readline()

                # iterate line by line over all files
                while sline != '':

                    # print a status message
                    counter += 1
                    if (counter % 500000) == 0:
                        print counter,"lines read ..."

                    # preprocess current line in all files
                    sline = sline.rstrip().split(' ')
                    tline = trg.readline().rstrip().split(' ')
                    aline = alg.readline().rstrip().split(' ')

                    # create an alignment dictionary
                    s_alg_dic = defaultdict(list)
                    t_alg_dic = defaultdict(list)
                    for a in aline:
                        a = a.split('-')
                        s_alg_dic[int(a[0])].append(int(a[1]))
                        t_alg_dic[int(a[1])].append(int(a[0]))


                    to_check = []
                    checking = False
                    ner_type = None

                    # iterate over all tokens
                    for j,w in enumerate(sline):

                        # concatenate NEs spanning over multiple tokens (only if same entity type)
                        if re.match(ur'.+?\|[POGL]',w) and (ner_type == None or ner_type == w.split('|')[1][0]):
                            to_check.append((w,j))
                            checking = True
                            ner_type = w.split('|')[1][0]

                        else:

                            # after a bunch of NEs was read add them to dictionary
                            if checking:
                                match = []

                                # get all aligned tokens
                                alignments = [s_alg_dic[m] for l,m in to_check if s_alg_dic[m] != []]
                                alignments = [f for k in alignments for f in k]

                                # get NEs of aligned token range
                                if alignments != []:
                                    maxx = max(alignments)
                                    minn = min(alignments)
                                    t_alignments = [i for i in range(minn,maxx+1) if re.match(ur'.+?\|[POGL]',tline[i])]
                                    if t_alignments != []:
                                        maxx = max(t_alignments)
                                        minn = min(t_alignments)
                                        for i in range(minn,maxx+1):
                                            t_tok = tline[i]
                                            match.append(t_tok.split('|')[0])

                                        # add to dictionary
                                        if match != []:
                                            src_dic[' '.join([t[0].split('|')[0] for t in to_check])].append(' '.join(match))
                                            trg_dic[' '.join(match)].append(' '.join([t[0].split('|')[0] for t in to_check]))


                            checking = False
                            to_check = []

                            # if currently read entity was of different type --> needs to be addeded to to_check again
                            if re.match(ur'.+?\|[POGL]',w):
                                to_check.append((w,j))
                                checking = True
                                ner_type = w.split('|')[1][0]

                    # read next line
                    sline = src.readline()


    # store source dictionary - with 3 most common entries per token
    with codecs.open( "src_trg_ne_dict.pkl", "w") as out:
        for k,v in src_dic.items():
            src_dic[k] = FreqDist(v).most_common(3)
        pickle.dump( src_dic,  out)

    # store target dictionary - with 3 most common entries per token
    with codecs.open( "trg_src_ne_dict.pkl", "w") as out:
        for k,v in trg_dic.items():
            trg_dic[k] = FreqDist(v).most_common(3)
        pickle.dump( trg_dic,  out)



################################################################################


if __name__ == "__main__":

    main()
