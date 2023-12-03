import json
from dataclasses import dataclass


class QueryHandler :
    def __init__(
        self,
        whole_paper_dict,
        whole_author_dict,
        whole_institution_dict,
        whole_expertise_dict,
    ) :
        self.whole_paper_dict = whole_paper_dict
        self.whole_author_dict = whole_author_dict
        self.whole_institution_dict = whole_institution_dict
        self.whole_expertise_dict = whole_expertise_dict

    def paperByDOI(self, doi) :

        for paper in self.whole_paper_dict.values() :
            if paper.DOI == doi :
                print("paperByDOI", paper.DOI)
                return True, paper
        paper = Paper(DOI=doi, title=doi, query_handler=self)
        return False, paper
    
 
        return

        if doi not in list(map(lambda x: x.DOI, self.whole_paper_dict.values())) :
            return False, Paper(DOI=doi, title=doi, query_handler=self)
        
        paper = self.whole_paper_dict[doi]
        if paper.abstract is None :
            if paper.google_schorlar_metadata is not None and "설명" in paper.google_schorlar_metadata :
                paper.abstract = paper.google_schorlar_metadata["설명"]
        
        return True, self.whole_paper_dict[doi]
    

    
    def authorByName(self, name) :
        if name not in self.whole_author_dict :
            return Author(name=name, query_handler=self)
        return self.whole_author_dict[name]
    

@dataclass
class JournalConference :
    type : str = None
    name : str = None
    ISSN : str = None
    eissn : str = None
    publisher : str = None
    URL : str = None
    Country : str = None
    Status : str = None
    
    query_handler : QueryHandler = None

    def toJSON(self) :
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)
    def toDict(self) :
        return json.loads(self.toJSON())


@dataclass
class Institution :
    name :str
    google_scholar_url : str
    homepage_url : str = None

    query_handler : QueryHandler = None

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

    query_handler : QueryHandler = None

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
    google_schorlar_profile_url : str = None 
    affiliation : str = None
    expertise_list : list[str] = None
    homepage_url : str = None
    paper_list : list = None
    paper_title_list : list = None

    query_handler : QueryHandler = None 

    @property
    def paper_item_list(self) :
        return list(map(lambda x: self.query_handler.paperByDOI(x)[1], self._paper_list))

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
    issn_type : dict = None
    url : str = None
    is_in_favorite : bool = False

    conference_acronym : str = None
    publisher : str = None

    query_handler : QueryHandler = None

    def toggleFavorite(self) :
        self.is_in_favorite = not self.is_in_favorite

    @property
    def reference_paper_list(self) :
        pre_existed_paper_list = []
        new_paper_list = []

        for doi in self.reference_list :
            is_existed, paper = self.query_handler.paperByDOI(doi)
            if is_existed :
                pre_existed_paper_list.append(paper)
            else :
                new_paper_list.append(paper)
        print(self.title, len(pre_existed_paper_list), len(new_paper_list))
        print(
            list(map(lambda x: x.title, pre_existed_paper_list)) + \
            list(map(lambda x: x.title, new_paper_list))
        )


        return pre_existed_paper_list + new_paper_list

        return list(map(lambda x: self.query_handler.paperByDOI(x), self.reference_list))
    
    @property
    def author_list(self) :
        author_name_list = [] if self.authors is None else self.authors
        if self.google_schorlar_metadata is not None and  "저자" in self.google_schorlar_metadata :
            author_name_list = self.google_schorlar_metadata["저자"].split(", ")

        return list(map(lambda x: self.query_handler.authorByName(x), author_name_list))

    @property
    def abstract_text(self) :
        if self.abstract is None :
            if self.google_schorlar_metadata is not None and "설명" in self.google_schorlar_metadata :
                self.abstract = self.google_schorlar_metadata["설명"]
        return self.abstract
        

    def toJSON(self):
        '''convert to JSON recursively'''
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)
    def toDict(self):
        '''convert to dict recursively'''
        return json.loads(self.toJSON())
