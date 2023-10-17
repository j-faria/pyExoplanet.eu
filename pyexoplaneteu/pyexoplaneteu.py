#!/usr/bin/env python
import os
from urllib import request
import time
import math
import csv
import pprint
from collections import OrderedDict

from .utils import float_cols

# the link in the "Download CSV" button
download_link = 'http://exoplanet.eu/catalog/csv'

# to get the directory where SWEET-Cat data will be stored
from .config import get_data_dir

def download_data():
    """ Download exoplanet.eu data and save it to `exoplanetEU.csv` """

    with request.urlopen(download_link) as response:
       data = response.read()

    local_file = os.path.join(get_data_dir(), 'exoplanetEU.csv')
    with open(local_file, 'wb') as f:
        f.write(data)

    print(f'Saved exoplanet.eu data to {local_file}')


def check_data_age():
    """ How old is `exoplanetEU.csv`, in days """
    local_file = os.path.join(get_data_dir(), 'exoplanetEU.csv')
    age = time.time() - os.path.getmtime(local_file) # in sec
    return age / (60*60*24) # in days


class DataDict(OrderedDict):
    numpy_entries = False

    __doc__ = "exoplanet.eu: a catalog of parameters for known exoplanets.\n" + \
              "The catalog and more information can be found " \
              "at http://exoplanet.eu\n" + \
              "This dictionary has the catalog columns as its keys; " \
              "see the `.columns()` method.\n" + \
              "Entries are lists, see `to_numpy()` to convert them to numpy arrays."
    def __init__(self, *args, **kwargs):
        super(DataDict, self).__init__(self, *args, **kwargs)

    def __getitem__(self, key):
        # allows to do data['key_nonan'] to get data['key'] without NaNs
        if key.endswith('_nonan'):
            val = super().__getitem__(key.replace('_nonan',''))
            try:
                if self.numpy_entries:
                    from numpy import isnan
                    val = val[~isnan(val)]
                else:
                    val = [v for v in val if not math.isnan(v)]
            except TypeError:
                # this column does not have floats
                pass
        else:
            val = super().__getitem__(key)

        return val

    def __str__(self):
        return 'exoplanet.eu data'
    def __repr__(self):
        return f'exoplanet.eu data: dictionary with {self.size} entries. '+\
                'Use .columns() to get the column labels.'
    def _repr_pretty_(self, p, cycle):
        return p.text(self.__repr__())
                
    def __len__(self):
        return len(self.__getitem__('name'))
    
    def columns(self):
        """ List the available columns """
        pprint.pprint(list(self.keys()), compact=True)

    @property
    def size(self):
        return len(self.__getitem__('name'))

    def to_numpy(self, inplace=True):
        """ 
        Convert entries to numpy arrays. If `inplace` is True convert
        the entries in place, else return a new dictionary.
        """
        from numpy import asarray # this assumes numpy is installed
        newself = self if inplace else DataDict()
        for k, v in self.items():
            newself[k] = asarray(v)
        newself.numpy_entries = True
        if not inplace:
            return newself


def read_data():
    def apply_float_to_column(data, key):
        data[key] = [float(v) if v!='' else math.nan for v in data[key]]
    
    # read the file
    local_file = os.path.join(get_data_dir(), 'exoplanetEU.csv')
    with open(local_file) as csvfile:
        reader = csv.DictReader(csvfile)
        lines = [row for row in reader]
    
    # lines is a list of (ordered) dicts; transform it to a (ordered) dict of lists
    data = OrderedDict({k: [dic[k] for dic in lines] for k in lines[0]})

    # column labels were read automatically by the csv.DictReader
    labels = list(data.keys())

    nlab, nlin = len(labels), len(lines)
    print(f'There are {nlab} columns with {nlin} entries each in `exoplanetEU.csv`')

    data = DataDict(**data)
    data.move_to_end('name', last=False) # put this key back at the beginning,
                                         # just for clarity

    # transform some columns to floats
    for col in float_cols:
        apply_float_to_column(data, col)

    return data


def get_data():
    local_file = os.path.join(get_data_dir(), 'exoplanetEU.csv')

    if not os.path.exists(local_file):
        print ('Downloading exoplanet.eu data')
        download_data()
    
    age = check_data_age()
    if age > 5:
        print ('Data in `exoplanetEU.csv` is older than 5 days, downloading.')
        download_data()
    else:
        print ('Data in `exoplanetEU.csv` is recent.')

    data = read_data()
    return data


if __name__ == '__main__':
    data = get_data()