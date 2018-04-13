
requiredFields = []

class FrfObjectBase:
    def _cleanUpNAs(self):
        '''
        The FRF data has strings of 'N/A' where the data is not available.
        For putting these into the PostGres database, this method changes all
        attributes with 'N/A' to be None. This should only be called from a
        child classes __init__ method at the end of it.
        :return: None
        '''
        for aKey in self.__dict__.keys():
            if self.__dict__[aKey] == 'N/A':
                self.__dict__[aKey] = None

    def prettyPrint(self):
        d = self.__dict__
        for aKey in d.keys():
            print "    {0} : {1}".format(aKey, d[aKey])
