import json
from dataclasses import dataclass

@dataclass
class Institution :
    name :str
    google_scholar_url : str
    homepage_url : str = None

    def toJSON(self) :
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)
    def toDict(self):
        return json.loads(self.toJSON())

    def fromDict(self, dic):
        self.name = dic['name']
        self.google_scholar_url = dic['google_scholar_url']
        self.homepage_url = dic['homepage_url']

@dataclass
class Expertise :
    name : str
    url : str

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)
    def toDict(self):
        return json.loads(self.toJSON())
    def fromDict(self, dic):
        self.name = dic['name']
        self.url = dic['url']

@dataclass
class Author :
    name : str
    google_schorlar_profile_url : str
    affiliation : str = None
    expertise_list : list[str] = None
    homepage_url : str = None
    paper_list : list = None
    paper_title_list : list = None

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)
    def toDict(self):
        return json.loads(self.toJSON())
    def fromDict(self, dic):
        self.name = dic['name']
        self.google_schorlar_profile_url = dic['google_schorlar_profile_url']
        self.affiliation = dic['affiliation']
        self.expertise_list = dic['expertise_list']
        self.homepage_url = dic['homepage_url']
        self.paper_list = dic['paper_list']
        self.paper_title_list = dic['paper_title_list']
        
@dataclass
class Paper :
    # After search paper title using Google Schorlar,
    # fill in basic metadata (abstract) from Google Schorlar
    # fill in other metadata from Crossref
    DOI : str = None
    crossref_json : dict = None
    google_schorlar_metadata : dict = None
    title : str = None
    authors : list = None
    abstract : str = None
    conference : str = None
    journal : str = None
    year : int = None
    reference_list : list[str] = None
    referenced_list : list[str] = None
    cite_bibtex : str = None

    conference_acronym : str = None
    publisher : str = None

    def toJSON(self):
        '''convert to JSON recursively'''
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)
    def toDict(self):
        '''convert to dict recursively'''
        return json.loads(self.toJSON())
    def fromDict(self, dic) :
        '''convert from dict recursively'''
        self.DOI = dic['DOI']
        self.crossref_json = dic['crossref_json']
        self.google_schorlar_metadata = dic['google_schorlar_metadata']
        self.title = dic['title']
        self.authors = dic['authors']
        self.abstract = dic['abstract']
        self.conference = dic['conference']
        self.journal = dic['journal']
        self.year = dic['year']
        self.reference_list = dic['reference_list']
        self.referenced_list = dic['referenced_list']
        self.cite_bibtex = dic['cite_bibtex']