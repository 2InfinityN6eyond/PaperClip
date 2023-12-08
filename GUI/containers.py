from dataclasses import dataclass

# Define data Structure of Author & function
@dataclass
class Author :
    name : str
    #google_schorlar_profile_url : str = None 
    affiliation : str = None
    expertise_list : list[str] = None
    homepage_url : str = None
    paper_list : list = None
    paper_title_list : list = None

    query_handler : None  = None 

    # Define properties of class
    @property
    def paper_item_list(self) : # get data from DB by following sql query, paperByDOI
        return list(map(
            lambda x: self.query_handler.paperByDOI(x)[1],
            self._paper_list
        ))

# Define data Structure of Paper & function
@dataclass
class Paper :
    '''
    Class representing paper.
    this class serves for viewpoint of GUI.
    
    '''
    DOI : str = None
    title : str = None
    authors : list = None
    abstract : str = None
    conference : str = None
    journal : str = None
    reference_list : list[str] = None
    referenced_num : int = None
    is_in_favorite : bool = False
    keywords : list[str] = None
    conference_acronym : str = None
    query_handler : None = None

    def toggleFavorite(self) : # update clip icon
        self.is_in_favorite = not self.is_in_favorite
        self.query_handler.updatePaper(self)

    @property
    def reference_count(self) : # return number of reference paper
        return len(self.reference_list) if self.reference_list is not None else 0

    @property
    def reference_paper_list(self) :
        '''
        GUI does not care about initializing Paper class by DOI.
        When Paper class of reference paper is needed, 
        Gui just call this property.
        then this methed will initialize Paper class by DOI.
        so the GUI does not aware of the existence of query_handler.
        '''
        self.query_handler.fillReferenceList(self)

        pre_existed_paper_list = [] # stores paper object which were parsed
        new_paper_list = [] # stores paper object which were not parsed, so DOI doesn't exist in paper table

        for doi in self.reference_list :
            is_existed, paper = self.query_handler.paperByDOI(doi)
            if is_existed :
                pre_existed_paper_list.append(paper)
            else :
                new_paper_list.append(paper)
        return pre_existed_paper_list + new_paper_list

    @property
    def author_list(self) : # get data from DB by following sql query, queryPaperBy author_name
        author_name_list = [] if self.authors is None else self.authors
        return list(map(
            #lambda x: self.query_handler.authorByName(x),
            lambda x : self.query_handler.queryPaperBy(
                by = "apr.author_name", value = x
            ),
            author_name_list
        ))

    @property
    def abstract_text(self) : # get abstract text from google_schorlar_metadata
        if self.abstract is None :
            if self.google_schorlar_metadata is not None and "설명" in self.google_schorlar_metadata :
                self.abstract = self.google_schorlar_metadata["설명"]
        return self.abstract
    
