import numpy
import os
import sys

VOCAB_SIZE = 35000
SRC = "lv"
TGT = "en"
DATA_DIR = "~/data/LvEn/"

from nematus.nmt import train


if __name__ == '__main__':
    validerr = train(saveto='model/LvEn.npz',
                    datasets=[DATA_DIR + '/full.bpe.' + SRC, DATA_DIR + '/full.bpe.' + TGT],
                    valid_datasets=[DATA_DIR + '/dev.bpe.' + SRC, DATA_DIR + '/dev.bpe.' + TGT],
                    dictionaries=[DATA_DIR + '/full.bpe.' + SRC + '.json',DATA_DIR + '/full.bpe.' + TGT + '.json'],
                    validFreq=15000,
                    dispFreq=2000,
                    saveFreq=15000,
                    sampleFreq=10000,
                    use_dropout=True,
                    external_validation_script='./validate.sh')
    print validerr
