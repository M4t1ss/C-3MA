#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import numpy as np

class Ne_Matrix(object):

    def __init__(self,translation,source):

        # store source sentence and translation, initialise alignment matrix
        self.source = source
        self.translation = translation
        self.matrix = []


    def add_alignment(self,line):
        """add next row to the matrix"""

        self.matrix.append(line)

    def clean(self,axis,indeces=[]):
        """cleans attention matrix (adding bpe parts, delete last row)"""

        self.matrix = np.array(self.matrix)
        for i in indeces[::-1]:
            if axis == 0:
                self.matrix[i] += self.matrix[i+1]
            elif axis == 1:
                self.matrix[:,i] += self.matrix[:,i+1]
            else:
                print "axis has to be 0 or 1"
                return
            self.matrix = np.delete(self.matrix,i+1,axis)

    def get_matrix(self):
        """returns matrix"""

        return self.matrix

    def get_matrix_transposed(self):
        """returns transposed matrix for easy access via source sentence"""

        return self.matrix.transpose()

    def set_matrix(self,matrix):
        """set matrix for sentence"""

        self.matrix = matrix

    def get_source(self):
        """returns source sentence"""

        return self.source

    def get_translation(self):
        """returns translated sentence"""

        return self.translation
