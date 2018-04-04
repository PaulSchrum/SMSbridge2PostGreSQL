

class FrfObjectBase:
    def _cleanUpNAs(self):
        for aKey in self.__dict__.keys():
            if self.__dict__[aKey] == 'N/A':
                self.__dict__[aKey] = None

    def prettyPrint(self):
        d = self.__dict__
        for aKey in d.keys():
            print "    {0} : {1}".format(aKey, d[aKey])
