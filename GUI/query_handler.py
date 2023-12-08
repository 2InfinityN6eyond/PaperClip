import mysql.connector

# local import
from containers import Paper, Author

class QueryHandler :
    '''
    Connects GUI and database, and handle all queries to database,
    so the GUI does not need to know about database. 
    Offers methods to query data from database,
    and convert them to GUI-friendly data structures
    Every instance of Paper, Author class has a reference to this class,
    and when GUI askes for data, they will ask this class.
    '''
    def __init__(
        self,
        host    = 'localhost',
        user    = 'root',
        passwd  = 'wonhs120415',
        db_use  = 'relation_db_project'
    ) :
        '''
        initialize connection to database
        '''
        self.mydb = mysql.connector.connect(
            host    = host,
            user    = user,
            passwd  = passwd,
            database= db_use
        )
        self.cursor = self.mydb.cursor(prepared=True)

    def queryPaperBy(self, by, value) :
        '''
        Main method to query paper from database.
        args :
            by : str
                table, column name to query
                ex) "p.title", "p.DOI", "p.keywords", "p.clip" where p is abbreviation of paper table
            value : str
                value to query
        returns :
            list of Paper object
        '''
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
                    )) if author_name is not None else None,
                    keywords        = list(map(
                        lambda x : x.strip(),
                        keywords.split(', ')
                    )) if keywords is not None else None,
                    conference_acronym = conference_name,
                    referenced_num  = refernced_num,
                    reference_list = [],
                    # reference_list feild cannot be filled here, because the query does not join related_works table due to performance issue.
                    # so the reference_list will be filled when paper.reference_list is called.
                    # GUI will expect Paper instance to have reference_list feild, which the item of reference_list is Paper instance.
                    # when GUI accesses paper.reference_list, it is actually calling paper.reference_paper_list property.
                    # property will call this.query_handler.fillReferenceList(self) to fill reference_list. 
                    # so the GUI does not aware of the existence of query_handler.
                    abstract=abstract,
                    is_in_favorite  = is_in_favorite,
                    query_handler=self
                )
        return list(paper_dict.values())

    def paperByDOI(self, doi) :
        '''
        query paper by DOI
        args :
            doi : str
                DOI to query
        returns :
            tuple of (bool, Paper)
            bool :
                True if doi exists inside paper table. (which means the paper has been crawled)
                False otherwise (which means the paper has not been crawled, thus empty paper object will be returned)
            Paper : Paper object
                if doi exists inside paper table, then Paper object with full information will be returned.
                otherwise, Paper object which contains only title and doi field will returned.
        '''
        paper_list = self.queryPaperBy("p.DOI", doi)
        if len(paper_list) == 0 : # paper with that doi not crawled yet
            paper = Paper(DOI=doi, title=doi)
            return False, paper
        else :
            return True, paper_list[0]

    def fillReferenceList(self, paper) :
        '''
        
        '''
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
