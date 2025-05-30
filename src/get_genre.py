import numpy as np
import torch
import sys
import json

from collections import Counter
from sklearn.preprocessing import LabelEncoder

from librosa.core import load
from librosa.feature import melspectrogram
from librosa import power_to_db

from model import genreNet
from config import MODELPATH
from config import GENRES

import warnings
warnings.filterwarnings("ignore")


def main(argv):

    if len(argv) != 3:
        print("Usage: python3 get_genre.py model genre audiopath")
        exit()
    MODELPATH = argv[0]
    genre = argv[1]
    le = LabelEncoder().fit(GENRES[genre])
    # ------------------------------- #
    ## LOAD TRAINED GENRENET MODEL
    net         = genreNet(GENRES[genre])
    net.load_state_dict(torch.load(MODELPATH, map_location='cpu'))
    # ------------------------------- #
    ## LOAD AUDIO
    audio_path  = argv[2]
    y, sr       = load(audio_path, mono=True, sr=22050)
    #print(f"SHAPE Y: {y.shape}")
    # ------------------------------- #
    ## GET CHUNKS OF AUDIO SPECTROGRAMS
    S           = melspectrogram(y=y, sr=sr).T
    #print(f"SHAPE S: {S.shape}")
    if S.shape[0] % 128 != 0:
        S           = S[:-1 * (S.shape[0] % 128)]
    num_chunk   = S.shape[0] / 128
    #print(f"CHUNKS: {num_chunk}")
    # Short circuit if input is too tiny
    if num_chunk == 0:
        print("{}")
        return
    data_chunks = np.split(S, num_chunk)
    # ------------------------------- #
    ## CLASSIFY SPECTROGRAMS
    genres = list()
    for i, data in enumerate(data_chunks):
        data    = torch.FloatTensor(data).view(1, 1, 128, 128)
        preds   = net(data)
        pred_val, pred_index    = preds.max(1)
        pred_index              = pred_index.data.numpy()
        pred_val                = np.exp(pred_val.data.numpy()[0])
        pred_genre              = le.inverse_transform(pred_index).item()
        #print(f"{i},{pred_genre},{pred_val}")
        if pred_val >= 0.5:
            genres.append(pred_genre)
    # ------------------------------- #
    s           = float(sum([v for k,v in dict(Counter(genres)).items()]))
    pos_genre   = sorted([(k, v/s*100 ) for k,v in dict(Counter(genres)).items()], key=lambda x:x[1], reverse=True)
    output = json.dumps(dict(pos_genre))
    print(output)
    return

if __name__ == '__main__':
    main(sys.argv[1:])
