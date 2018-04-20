
fieldNameMapping = { '_id' : 'mongo_id',
                     'mongo_id' : '_id'}

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

    @classmethod
    def _map(cls, txt):
        '''
        It is necessary to change names between the MongoDB json dump and the
        PostgreSQL RDBMS. Alway call this when getting a field name.
        :param txt:
        :return:
        '''
        try:
            return fieldNameMapping[txt]
        except:
            return txt

    def prettyPrint(self):
        d = self.__dict__
        for aKey in d.keys():
            print "    {0} : {1}".format(aKey, d[aKey])


if __name__ == '__main__':
    print 'testing started'
    assert FrfObjectBase._map('_id') == 'mongo_id'
    assert FrfObjectBase._map('mongo_id') == '_id'
    assert FrfObjectBase._map('station') == 'station'
    print 'testing complete'

