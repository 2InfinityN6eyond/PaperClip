import json
from dataclasses import dataclass
import Levenshtein
import mysql.connector


class QueryHandler :
    def __init__(
        self,
        host    = None,
        user    = None,
        passwd  = None,
        db_use  = None
    ) :
        self.mydb = mysql.connector.connect(
            host    = host,
            user    = user,
            passwd  = passwd,
            database= db_use
        )
        self.cursor = self.mydb.cursor(prepared=True)

    def paperByDOI(self, doi) :
        paper_list = self.queryPaperBy("p.DOI", doi)
        if len(paper_list) == 0 :
            paper = Paper(DOI=doi, title=doi)
            return False, paper
        else :
            return True, paper_list[0]

    def queryPaperBy(self, by, value) :
        self.cursor.execute(f"""
            select p.DOI, p.title,  p.referenced_num, GROUP_CONCAT(' ', apr.author_name) as author_name, p.keywords, c.`name` as conference_name, p.clip, p.abstract
            from paper p
            Left join author_paper_relationship apr on p.DOI = apr.DOI
            left join conference c on p.issn = c.issn
            where {by} like '%{value}%'
            GROUP BY p.DOI, p.title,  p.referenced_num, p.keywords, c.`name`
            order by p.referenced_num desc
            limit 100;
        """)
        paper_dict = {}
        for row in self.cursor :
            doi, title, refernced_num, author_name, keywords, conference_name, is_in_favorite, abstract = row
            if doi not in paper_dict :
                paper_dict[doi] = Paper(
                    DOI             = doi,
                    title           = title,
                    authors         = list(map(
                        lambda x : x.strip(),
                        author_name.split(', ')
                    )) if author_name is not None else None, #[''],
                    keywords        = list(map(
                        lambda x : x.strip(),
                        keywords.split(', ')
                    )) if keywords is not None else None, # [''],
                    conference_acronym = conference_name,
                    referenced_num  = refernced_num,
                    reference_list = [],
                    abstract=abstract,
                    is_in_favorite  = is_in_favorite,
                    query_handler=self
                )
        return list(paper_dict.values())

    def fillReferenceList(self, paper) :
        self.cursor.execute(f"""
            select ref_doi
            from referenced_paper
            where DOI like '%{paper.DOI}%'
            ;
        """)
        for row in self.cursor :
            paper.reference_list.append(row[0])

    def getRelatedPaperList(self, paper) :

        self.fillReferenceList(paper)

        # paper table has doi, title, referenced_num, keywords, journal, clip
        # author_paper_relationship has doi, author_name, DOI is foreign key of paper table
        # referenced_paper table has DOI, ref_doi, DOI is foreign key of paper table
        self.cursor.execute(f"""
            select p.DOI, p.title,  p.referenced_num, GROUP_CONCAT(' ', apr.author_name) as author_name, p.keywords, c.`name` as conference_name, p.clip, rp.ref_doi, p.abstract
            from paper p
            Left join author_paper_relationship apr on p.DOI = apr.DOI
            left join referenced_paper rp on p.DOI = rp.DOI
            left join conference c on p.issn = c.issn
            where rp.ref_doi in ({','.join(map(lambda x: f"'{x}'", paper.reference_list))})
            GROUP BY p.DOI, p.title,  p.referenced_num, p.keywords,  c.`name`, rp.ref_doi
            order by p.referenced_num desc
            ;
        """)
        paper_dict = {}
        for row in self.cursor :
            doi, title, refernced_num, author_name, keywords, conference_name, is_in_favorite, reference, abstract = row
            if doi not in paper_dict :
                paper_dict[doi] = Paper(
                    DOI             = doi,
                    title           = title,
                    authors         = list(map(
                        lambda x : x.strip(),
                        author_name.split(', ')
                    )) if author_name is not None else None, #[''],
                    keywords        = list(map(
                        lambda x : x.strip(),
                        keywords.split(', ')
                    )) if keywords is not None else None, # [''],
                    conference_acronym = conference_name,
                    referenced_num  = refernced_num,
                    reference_list = [reference],
                    abstract=abstract,
                    is_in_favorite  = True if is_in_favorite else False,
                    query_handler=self
                )            
            else :
                paper_dict[doi].reference_list.append(reference)
        return list(paper_dict.values())

    def updatePaper(self, paper) :
        # set clip column of paper table to paper.is_in_favorite
        self.cursor.execute(f"""
            UPDATE paper
            SET clip = {paper.is_in_favorite}
            WHERE DOI LIKE "%{paper.DOI}%"
            ;
        """)
        self.mydb.commit()


    def fetchTopKeywords(self, n = 50) :
        self.cursor.execute("DROP TEMPORARY TABLE IF EXISTS keyword_table;")
        self.cursor.execute("""
            CREATE TEMPORARY TABLE keyword_table AS
            SELECT TRIM(SUBSTRING_INDEX(SUBSTRING_INDEX(keywords, ', ', n.digit + 1), ',', -1)) AS keyword
            FROM paper,
                (SELECT 0 AS digit UNION ALL SELECT 1 UNION ALL SELECT 2 UNION ALL SELECT 3) AS n
            WHERE LENGTH(keywords) - LENGTH(REPLACE(keywords, ',', '')) >= n.digit;
        """)
        self.cursor.execute("DROP TEMPORARY TABLE IF EXISTS keyword_table;")
        self.cursor.execute("""
            CREATE TEMPORARY TABLE keyword_table AS
            SELECT TRIM(SUBSTRING_INDEX(SUBSTRING_INDEX(keywords, ', ', n.digit + 1), ',', -1)) AS keyword
            FROM paper,
                (SELECT 0 AS digit UNION ALL SELECT 1 UNION ALL SELECT 2 UNION ALL SELECT 3) AS n
            WHERE LENGTH(keywords) - LENGTH(REPLACE(keywords, ',', '')) >= n.digit;
        """)
        self.cursor.execute("""SET SQL_SAFE_UPDATES = 0;""")
        self.cursor.execute("""DELETE FROM keyword_table WHERE keyword = '';""")
        self.cursor.execute(f"""
            SELECT keyword, COUNT(*) AS keyword_count
            FROM keyword_table
            GROUP BY keyword
            ORDER BY keyword_count DESC
            LIMIT {n};
        """)
        keyword_count_list = []
        for row in self.cursor :
            keyword_count_list.append(row)
        return keyword_count_list

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
    url_list : list = None

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
        return list(map(
            lambda x: self.query_handler.paperByDOI(x)[1],
            self._paper_list
        ))

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
    referenced_num : int = None
    cite_bibtex : str = None
    issn_type : dict = None
    url : str = None
    is_in_favorite : bool = False
    keywords : list[str] = None

    conference_acronym : str = None
    publisher : str = None

    query_handler : QueryHandler = None

    def toggleFavorite(self) :
        self.is_in_favorite = not self.is_in_favorite
        self.query_handler.updatePaper(self)

    @property
    def reference_count(self) :
        return len(self.reference_list) if self.reference_list is not None else 0

    @property
    def reference_paper_list(self) :
        
        self.query_handler.fillReferenceList(self)

        pre_existed_paper_list = []
        new_paper_list = []

        for doi in self.reference_list :
            is_existed, paper = self.query_handler.paperByDOI(doi)
            if is_existed :
                pre_existed_paper_list.append(paper)
            else :
                new_paper_list.append(paper)
        return pre_existed_paper_list + new_paper_list

    @property
    def author_list(self) :
        author_name_list = [] if self.authors is None else self.authors
        return list(map(
            #lambda x: self.query_handler.authorByName(x),
            lambda x : self.query_handler.queryPaperBy(
                by = "apr.author_name", value = x
            ),
            author_name_list
        ))

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
