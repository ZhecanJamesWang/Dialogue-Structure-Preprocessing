import os

class DocReader(object):
    """ class of large text reader"""
    def __init__(self, dirname):
        self.dirname = dirname
 
    def __iter__(self):
        for fname in os.listdir(self.dirname):
            if os.path.isfile(os.path.join(self.dirname, fname)):
                print "reading file from: ", fname
                for line in open(os.path.join(self.dirname, fname)):
                    yield line.split()
