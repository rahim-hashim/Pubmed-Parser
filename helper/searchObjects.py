import datetime

# Class Instantiation
### Called within SalzmanParser to instantiate class objects and attributes
class SearchParameters:
    def __init__(self, parameters):
        
        self.database = parameters['database']
        self.searchTerms = parameters['searchTerms']
        self.searchLimit = parameters['searchLimit']
        self.startIndex = parameters['startIndex']

class Affiliation:
    def __init__(self):

        self.department = []
        self.university = []
        self.institute = []
        self.zipcode = []
        self.city = []
        self.state = []
        self.country = []
        self.email = []

class Author:
    def __init__(self):
        
        self.name = 'No Author Listed'
        self.listed_order = 0
        self.affiliations = {}