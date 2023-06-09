from config import GENRES, DATAPATH, MODELPATH
from data import Data
from set import Set
import sys

def main():
    if len(sys.argv) != 2:
        raise Exception("Bad args")
    category = sys.argv[1]
    # ------------------------------------------------------------------------------------------- #
    ## DATA
    data = Data(GENRES[category], category, DATAPATH)
    data.make_raw_data()
    data.save()
    data = Data(GENRES[category], category, DATAPATH)
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
