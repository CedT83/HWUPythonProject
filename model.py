#!/usr/bin/python3
# -*- coding: iso-8859-1 -*-

################################## Imports
#Our file containing functions for the features
import func


################################## Class
class Model(object):
    #This is the constructor for this class
    #In case no argument is provided for filename, we have a default one
    def __init__(self, filename='issuu.json', pandas=False):
        #We declare some variables, even if we don't need them now, we are sure they exist'
        self.data = None
        self.docUuid = None
        self.UserUuid = None
        self.pandas = pandas
        self.dataSource = filename

    #The following functions are wrappers for other methods.
    #It is usefull to call them within our handmade swith 
    def getBrowsers(self):
        return func.getBrowsersForDoc(filename=self.dataSource)

    def getCountries(self):
        return func.getCountriesForDoc(self.docUuid, filename=self.dataSource, method=self.pandas)

    def getUsersThatReadDoc(self):
        return func.getUsersForDoc(self.docUuid, filename=self.dataSource)
    
    def getDocsThatUserRead(self):
        return func.getDocsForUser(self.UserUuid, filename=self.dataSource)

    def getContinents(self):
        return func.getContinentsForDoc(self.docUuid, filename=self.dataSource)

    def getAlsoLike(self):
        users = list()
        docs = list()
        users = func.getUsersForDoc(self.docUuid, filename=self.dataSource)
        users = list(filter((self.UserUuid).__ne__, users))
        for user in users:
            docs_temp = func.getDocsForUser(user, filename=self.dataSource)
            #Python2.X
            #filter(lambda x: x != arguments['<doc_uuid>'], docs_temp)
            #Python 3.X
            docs_temp = list(filter((self.docUuid).__ne__, docs_temp))
            docs.extend(docs_temp)
        #we sort the list using the number of occurences (second argument in the tuple)
        print(users)
        return [x[0] for x in sorted(func.cleanup(docs), key=lambda x: x[1], reverse=True)[:10]]
        #return docs

    def getAlsoLikeReadership(self):
        #we get the list of the document that could interest the user
        documents = self.getAlsoLike()
        #we initialize a list for later
        result = list()
        #we get the readership
        readership = func.getReadership(filename=self.dataSource).keys()
        #we delete the actuel user from the readership
        readership = list(filter((self.docUuid).__ne__, readership))
        #for each document obtained from the normal AlsoLike function
        for doc in documents:
            #We get all the readers of the doc
            readers = func.getUsersForDoc(doc, filename=self.dataSource)
            #We want the index of the best reader in all the readers, so the lower index
            index = readership.index(next(i for i in readership if i in readers))
            #we create the tuple
            result.append((doc, index, readership[index]))
        #we sort the list using the second element of the tuple 
        return sorted(result, key=lambda x: x[1], reverse=False)[:10]

    def getAlsoLikePopularity(self):
        #we get the list of the document that could interest the user
        documents = self.getAlsoLike()
        result = list()
        #for each document obtained from the normal AlsoLike function
        for doc in documents:
            #We get all the readers of the doc
            readers = func.getUsersForDoc(doc, filename=self.dataSource)
            #we create the tuple with the number of readers for this document as second value of the tuple
            result.append((doc, len(readers)))
        #we sort the list using the second element of the tuple 
        return sorted(result, key=lambda x: x[1], reverse=False)[:10]

    def getRankedReaders(self):
        return func.getReadership(10, filename=self.dataSource)
    #This is the most important method of the class
    def extractData(self, docUuid, UserUuid, task):
        self.data = None
        self.docUuid = docUuid
        self.UserUuid = UserUuid
        # map the inputs to the function blocks
        #There is no swith in Python, so we create one. We associate values to methods 
        options = {0 : self.getCountries,
           1 : self.getContinents,
           2 : self.getBrowsers,
           3 : self.getRankedReaders,
           4 : self.getUsersThatReadDoc,
           5 : self.getDocsThatUserRead,
           6 : self.getAlsoLike,
           7 : self.getAlsoLikeReadership,
           8 : self.getAlsoLikePopularity,
        }
        #Then using the value
        code = task
        #We call the corresponding method
        try:
            self.data = options[code]()
            #We print the data, just for debugging
            print(self.data)
        except Exception:
            print("This task code is invalid")
            return 

    #Get method to the data variable
    def getData(self):
        return self.data

    #A simple method to represent some data with a histogram
    def draw(self):
        """ variable have to be a dict """
        #We call this method to get a vertical histogram
        func.show_histo(self.data, orient="vert", title="Extracted Data")
        return

