import pandas as pd
import numpy as np
import pickle
import random
import os

from librosa.core import load
from librosa.feature import melspectrogram
from librosa import power_to_db

from config import RAW_DATAPATH


class Data():

    def __init__(self, genres, datapath):
        self.raw_data   = None
        self.GENRES     = genres
        self.DATAPATH   = datapath
        print("\n-> Data() object is initialized.")

    def make_raw_data(self):
        records = list()
        for i, genre in enumerate(self.GENRES):
            GENREPATH = self.DATAPATH + genre + '/'
            files = os.listdir(GENREPATH)
            random.shuffle(files)
            files = [:200]
            for j, track in enumerate(files):
                TRACKPATH   = GENREPATH + track
                print("%d.%s\t\t%s (%d)" % (i + 1, genre, TRACKPATH, j + 1))
                y, sr       = load(TRACKPATH, mono=True, sr=22050)
                S           = melspectrogram(y=y, sr=sr).T
                if S.shape[0] % 128 != 0:
                    S           = S[:-1 * (S.shape[0] % 128)]
                num_chunk   = S.shape[0] / 128
                data_chunks = np.split(S, num_chunk)
                data_chunks = [(data, genre) for data in data_chunks]
                records.append(data_chunks)

        records = [data for record in records for data in record]
        self.raw_data = pd.DataFrame.from_records(records, columns=['spectrogram', 'genre'])
        return

    def save(self):
        with open(RAW_DATAPATH, 'wb') as outfile:
            pickle.dump(self.raw_data, outfile, pickle.HIGHEST_PROTOCOL)
        print('-> Data() object is saved.\n')
        return

    def load(self):
        with open(RAW_DATAPATH, 'rb') as infile:
            self.raw_data   = pickle.load(infile)
        print("-> Data() object is loaded.")
        return
