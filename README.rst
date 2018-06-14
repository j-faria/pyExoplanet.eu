pyExoplaneteu
==============
 
A pure-Python package to download data from the `Extrasolar Planets Encyclopaedia`_

This small package downloads all the data from the *exoplanet.eu* online catalogue of exoplanets 
and builds a (custom) dictionary with each column. 
It is a pure-Python package with no extra dependencies (see below).


|License MIT| |Travis build| |PyPI version|

How to use
----------

Install it from pip (**pyExoplaneteu** has no extra depencies)

::

    pip install pyExoplaneteu

and it's ready to use from Python

.. code:: python

    import pyexoplaneteu


**pyExoplaneteu** has one simple function, ``get_data()``,
which downloads the data from the online archive and returns it in a dictionary.

.. code:: python

    >>> data = pysweetcat.get_data()

.. code::

    Downloading exoplanet.eu data
    Saved exoplanet.eu data to $HOME/.pyexoplaneteu/exoplanetEU.csv
    Data in `exoplanetEU.csv` is recent.
    There are 98 columns with 3793 entries each in `exoplanetEU.csv`

where ``$HOME`` will  be your home directory.
The second time you call ``get_data()`` it will check if the data was downloaded recently, 
and only conditionally download it again.

.. code:: python

    >>> data = pysweetcat.get_data()

.. code::

    Data in `exoplanetEU.csv` is recent.
    There are 98 columns with 3793 entries each in `exoplanetEU.csv`

Now, `data` is (basically) a Python dictionary with the each column as keys.
But it has a couple extra methods and properties. For example

.. code:: python

    >>> data.size
    3793
    
returns the number of values in each column. The ``columns()`` method

.. code:: python

    >>> data.columns()
    ['name', 'planet_status', 'mass', 'mass_error_min', 'mass_error_max',
     'mass_sini', 'mass_sini_error_min', 'mass_sini_error_max', 'radius',
      'radius_error_min', 'radius_error_max', 'orbital_period',
      ...
 
will print the available columns.

The columns can be accessed as in a normal dictionary, with 

.. code:: python

    data['name']  # the name of the planet
    data['mass']  # the mass of the planet
    data['star_radius']  # the radius of the host star

    
Also, to drop the NaN values in a column (for some columns there will be quite a few)
we can use

.. code:: python

    data['mass_nonan']
    
    np.isnan(data['mass']).any()       # True
    np.isnan(data['mass_nonan']).any() # False
    

which allows us to more easily do histograms of the values.

Finnally, the ``.to_numpy(inplace=True)`` method converts all the columns to numpy arrays, 
either in place or not (this is the only function in **pyExoplaneteu** that requires numpy).


License
-------

Copyright 2018 João Faria.

**pyExoplaneteu** is free software made available under the MIT License. For
details see the LICENSE_ file.

.. _`Extrasolar Planets Encyclopaedia`: http://exoplanet.eu
.. _License: https://github.com/j-faria/pyExoplanet.eu/blob/master/LICENSE
.. |License MIT| image:: http://img.shields.io/badge/license-MIT-blue.svg?style=flat
   :target: https://github.com/j-faria/pyExoplanet.eu/blob/master/LICENSE
.. |Travis build| image:: https://travis-ci.org/j-faria/pyExoplanet.eu.svg?branch=master
    :target: https://travis-ci.org/j-faria/pyExoplanet.eu
.. |PyPI version| image:: https://badge.fury.io/py/pyExoplanet.eu.svg
    :target: https://badge.fury.io/py/pyExoplanet.eu
