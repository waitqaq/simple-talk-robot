class AbstractPlugin(object):

    def __init__(self,con):
        self.con = con

    def handle(self, query):
        pass

    def isValid(self, query):

        return False