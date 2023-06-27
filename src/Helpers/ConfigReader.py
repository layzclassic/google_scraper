import configparser

def ReadConfig():
    config = configparser.ConfigParser()
    config.read('config.ini')

    return config
