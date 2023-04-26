from config import GENRES, DATAPATH, MODELPATH
from data import Data
from set import Set


def main():
    # ------------------------------------------------------------------------------------------- #
    ## DATA
    data = Data(GENRES, DATAPATH)
    data.make_raw_data()
    data.save()
    data = Data(GENRES, DATAPATH)
    data.load()
    # ------------------------------------------------------------------------------------------- #
    ## SET
    set_ = Set(data)
    set_.make_dataset()
    set_.save()
    set_ = Set(data)
    set_.load()
    return

if __name__ == '__main__':
    main()
