#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# imported modules
import argparse
import sys
import codecs
import re
from ne_matrix import *
import pickle
import string

################################################################################

def parse_args():
    """parses arguments given when program is called"""
    parser = argparse.ArgumentParser()

    # required arguments
    parser.add_argument("-a", "--alignments",  required=True, action="store", dest="alg", help="alignment file")
    parser.add_argument("-n", "--ne_recognized",  required=True, action="store", dest="ne", help="source file with recognized named entities")
    parser.add_argument("-f", "--framework",  required=True, choices=['nematus', 'neuralmonkey'], action="store", dest="frame", help="nematus / neuralmonkey")
    parser.add_argument("-d", "--dictionary",  required=True, action="store", dest="dic", help="pickle file storing src-trg NE dictionary")

    # only required for neuralmonkey alignments
    parser.add_argument("-s", "--source",  required=False, action="store", dest="src", help="source sentences")
    parser.add_argument("-t", "--trans",  required=False, action="store", dest="trs", help="translated sentences")

    # optional
    parser.add_argument("-no_bpe", action="store_false", dest="bpe", help="no bpe used")

    return parser.parse_args()


################################################################################

def check_argument(arg,value,frame):
    """checks whether argument is present, raises IOError else"""

    if not value:
        raise IOError("error: {0:s} must be defined for {1:s} alignments".format(arg,frame))


################################################################################

def readlines_from_file(filename):
    """read lines from file"""

    with codecs.open(filename,"r","utf-8") as openf:
        lines = openf.readlines()

    return lines


################################################################################

def join_bpe(source,translation):
    """remove bpe from source and translation and store where bpe parts occurred"""

    s_split = source.split()
    t_split = translation.split()

    src_bpe_indeces = [i for i in range(0,len(s_split)) if s_split[i].endswith("@@")]
    trans_bpe_indeces = [i for i in range(0,len(t_split)) if t_split[i].endswith("@@")]

    source = re.sub(r"(@@ )|(@@ ?$)",r"",source)
    translation = re.sub(r"(@@ )|(@@ ?$)",r"",translation)

    return source,translation,src_bpe_indeces,trans_bpe_indeces


################################################################################

def initialise_nematus(args):
    """initialise information for nematus alignments"""

    print("\n*** reading Nematus alignments ***")

    # counter keeps track on sentence number
    counter = 0

    # store alignment matrix for each sentence
    matrices = []

    # go over all lines in the alignment file produced by nematus
    for line in readlines_from_file(args.alg):
        line = line.rstrip()

        # if new sentence starts
        if line.startswith('{0:d} |||'.format(counter)):

            # split first line of each alignment information block and extract source sentence & translation
            splits = line.split(' ||| ')
            translation = splits[1]
            source = splits[3]

            # if bpe convert to normal text
            if args.bpe:
                source,translation,src_bpe_indeces,trans_bpe_indeces = join_bpe(source,translation)

            translation = translation.split()
            source = source.split()

            # initialise a matrix for current sentence
            matrix = Ne_Matrix(translation,source)

            # update sentence counter
            counter += 1

        # after each block add the matrix of last sentence to matrix list
        elif line == "":
            matrix.set_matrix(matrix.get_matrix()[:-1])
            if args.bpe:
                matrix.clean(0,trans_bpe_indeces)
            else:
                matrix.clean(0)
            matrices.append(matrix)

        # add lines containing the alignment information to the matrix
        else:
            line = map(float,line.split(' '))[:-1]

            # if bpe sum up attention for bpe parts
            if args.bpe:
                for i in src_bpe_indeces[::-1]:
                    line[i] += line[i+1]
                    del line[i+1]

            matrix.add_alignment(line)

    return matrices


################################################################################

def initialise_neuralmonkey(args):
    """initialise information for neuralmonkey alignments"""

    print("\n*** reading Neuralmonkey alignments ***")

    # read sentences from all needed files
    alignments = np.load(args.alg)
    source_sents = readlines_from_file(args.src)
    trans_sents = readlines_from_file(args.trs)

    # ensure all files have the same length
    try:
        assert len(alignments) == len(source_sents) == len(trans_sents)
    except AssertionError:
        print("\nAssertionError: File lengths differ!")
        sys.exit()

    matrices = []

    # iterate over all sentences
    for index,line in enumerate(alignments):

        source = source_sents[index]
        translation = trans_sents[index]

        orig_source = source.split()
        orig_translation = translation.split()

        len_source = len(source.split())
        len_translation = len(translation.split())

        # if bpe convert to normal text
        if args.bpe:
            source,translation,src_bpe_indeces,trans_bpe_indeces = join_bpe(source,translation)

        translation = translation.split()
        source = source.split()

        matrix = line[:len_translation,:len_source]

        ne_matrix = Ne_Matrix(translation,source)
        ne_matrix.set_matrix(matrix)

        # if bpe sum up attention for bpe parts
        if args.bpe:
            if matrix.shape[1] < len(orig_source) or matrix.shape[0] < len(orig_translation):
                ne_matrix.set_skip()
            else:
                ne_matrix.clean(1,src_bpe_indeces)
                ne_matrix.clean(0,trans_bpe_indeces)
        matrices.append(ne_matrix)

    return matrices


################################################################################

def initialise(args):
    """initialise information for alignments"""

    framework = args.frame
    if framework == "nematus":
        return initialise_nematus(args)

    elif framework == "neuralmonkey":
        return initialise_neuralmonkey(args)


################################################################################

def should_enforce(ne,ne_pattern,translation_pattern,finds,ne_matrix):
    """checks if a translation should be enforced"""

    # if aligned with punctuation - do nothing
    if translation_pattern in string.punctuation:
        return False

    try:

        first = finds[0][0].split()

        # if 1 source NE aligned with multiple NEs and these are already in translation - do nothing
        if len(ne) == 1 and len(first) > 1 and all([True if tok in ne_matrix.get_translation() else False for tok in first]):
            return False

        # if first entry in dictionary is drastically longer than NE segment - do nothing
        if len(ne) / float(len(first)) < 0.3:
            return False

    except IndexError:
        pass

    # if any of the options in the dictionary are already in translation - do nothing
    if any(all(True if tok in ne_matrix.get_translation() else False for tok in f[0].split(' ')) for f in finds):
        return False

    # if all source NE tokens already in translation - do nothing
    if all(True if tok in ne_matrix.get_translation() else False for tok in ne):
        return False

    # if 'some_token aligned with some_token - do nothing
    if (translation_pattern[:6] == "&apos;" and translation_pattern[6:] == ne_pattern):
        return False

    # if given translation in dictionary entry - to nothing
    if translation_pattern in [token for token, count in finds]:
        return False

    return True


################################################################################

def enforce(args,sentences):
    """enforce translation of named entities"""

    print("\n*** start NE translation enforcing ***")

    # read NE dictionary
    with codecs.open(args.dic, "r" ) as opened:
        dic = pickle.load(opened)

    # open outfile
    with codecs.open("translation_ne_corrected.txt", "w", "utf-8") as outfile:

        # read source sentences with named entity markers
        nes = readlines_from_file(args.ne)

        # ensure same length
        assert len(sentences) == len(nes)

        # iterate over sentences
        for index,ne_source in enumerate(nes):
            ne_source = ne_source.split()
            ne_matrix = sentences[index]

            copy = ne_matrix.get_translation()

            # if no NEs occur in sentence continue with next sentence
            if ne_source == ne_matrix.get_source() or ne_matrix.should_skip():
                outfile.write(' '.join(copy)+"\n")
                continue


            delete = []
            ids = []
            ne = []
            force = False
            reading = False
            ne_type = None
            typechange = False

            ne_source.append(' ')

            for i,token in enumerate(ne_source):

                # find a bunch of NEs following each other with same type e.g. European Union
                if re.match(r".+?\|[PLOG]",token):

                    token_split = token.split("|")
                    token_without_tag = token_split[0]
                    cur_ne_type = token_split[1][0]
                    if ne_type == None or cur_ne_type == ne_type:
                        reading = True
                        force = True
                        ids.append(i)
                        ne.append(token_without_tag)
                    else:
                        typechange = True
                        ne_type = cur_ne_type
                        store_ne = [token_without_tag]
                        store_ids = [i]


                else:
                    reading = False

                # enforce translation for NE group read before
                if (not reading and force) or typechange:

                    search_pattern =  re.sub(r"@-@",r"-",' '.join(ne))
                    finds = dic[search_pattern]

                    skip = False

                    # if there are entries in the dictionary for source NE
                    if finds != []:

                        aligned = []
                        matrix = ne_matrix.get_matrix_transposed()

                        # get all max alignments from attention matrix
                        for j in ids:
                            candidate = np.argmax(matrix[j])
                            if np.argmax(ne_matrix.get_matrix()[candidate]) == j:
                                aligned.append(candidate)

                        # if some aligned tokens were found
                        if aligned != []:

                            max_i = np.max(aligned)
                            min_i = np.min(aligned)

                            match = ' '.join(ne_matrix.get_translation()[min_i:max_i+1])

                            # update translation with dictionary entry
                            if should_enforce(ne,search_pattern,match,finds,ne_matrix):
                                copy[min_i] = finds[0][0]
                                delete += range(min_i+1,max_i+1)

                        else:
                            skip = True

                    # else iterate over single NE tokens
                    if finds == [] or skip:

                        for j in ids:
                            search_pattern = ne_matrix.get_source()[j]
                            finds = dic[search_pattern]
                            matrix = ne_matrix.get_matrix_transposed()
                            candidate = np.argmax(matrix[j])

                            # if max alignment is mirrored
                            if np.argmax(ne_matrix.get_matrix()[candidate]) == j:
                                match = ne_matrix.get_translation()[candidate]

                                # update translation with dictionary entry
                                if should_enforce(ne,search_pattern,match,finds,ne_matrix):
                                    if ne_type == "P":
                                        copy[candidate] = search_pattern
                                    else:
                                        # if ORG or LOC in dictionary take from there
                                        if finds != []:
                                            copy[candidate] = finds[0][0]

                                        # else check if strings are similar and only copy if they are
                                        else:
                                            if float(len([t for t in match if t in search_pattern]))/max(len(match),len(search_pattern)) >= 0.85:
                                                copy[candidate] = search_pattern

                    force = False
                    ne = []
                    ids = []

                # if NE type for group changed before, add current NE to new group
                if typechange:
                    typechange = False
                    ne = store_ne
                    ids = store_ids
                    reading = True
                    force = True

            # delete all tokens that are not needed
            for d in delete[::-1]:
                del copy[d]

            # write corrected line to outfile
            outfile.write(' '.join(copy)+"\n")


################################################################################

def main(args):
    """main function to enforce translation of named entities"""

    # initialise attention matrices for all sentences
    sentences = initialise(args)

    # enforce translation of NEs
    enforce(args,sentences)

################################################################################

if __name__ == "__main__":

    args = parse_args()

    # ensure source and translated sentences are given for neuralmonkey
    try:
        if args.frame == "neuralmonkey":
            check_argument("-s (source)",args.src,"neuralmokey")
            check_argument("-t (translation)",args.trs,"neuralmonkey")
    except IOError as e:
        sys.exit(e)

    main(args)
