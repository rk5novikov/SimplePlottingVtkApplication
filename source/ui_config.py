import os


## Application configuration class
class ConfigObject(object):

    def __init__(self,):
        super(ConfigObject, self).__init__()
        self.dir_outil = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        self.dir_tests = os.path.join(self.dir_outil, 'tests')
        self.dir_pics = os.path.join(self.dir_outil, 'pics')
        self.dir_bin = os.path.join(self.dir_outil, 'bin')


config = ConfigObject()
