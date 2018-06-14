import os

def _create_data_dir():
    """ Create empty directory where exoplanetEU.csv will be stored """
    home = os.path.expanduser("~")
    directory = os.path.join(home, '.pyexoplaneteu')
    if not os.path.exists(directory):
        os.makedirs(directory)


def _check_data_dir():
    home = os.path.expanduser("~")
    directory = os.path.join(home, '.pyexoplaneteu')
    return os.path.exists(directory)


def get_data_dir():
    """ Return directory where exoplanetEU.csv is stored """
    if not _check_data_dir():
        _create_data_dir()
        
    home = os.path.expanduser("~")
    return os.path.join(home, '.pyexoplaneteu')



