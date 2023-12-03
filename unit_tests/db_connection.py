import mysql.connector


class QueryHandle_ :
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

    def paperByDOI(self, doi, exact=True) :

        self.cursor.execute()

        for paper in self.whole_paper_dict.values() :
            if paper.DOI == doi :
                print("paperByDOI", paper.DOI)
                return True, paper
        paper = Paper(DOI=doi, title=doi, query_handler=self)
        return False, paper
    
    def paperByTitle(self, title, exact=False, similarity_threshold=0.4) :
        result_list = []
        for paper in self.whole_paper_dict.values() :
            similarity = self.calculate_similarity(paper.title, title)
            if similarity >= similarity_threshold :
                result_list.append((similarity, paper))
        result_list.sort(key=lambda x: x[0], reverse=True)
        return list(map(lambda x: x[1], result_list))
    
    def paperByAuthor(self, author, similarity_threshold=0.4) :
        result_list = []
        for paper in self.whole_paper_dict.values() :
            for author_name in paper.authors :
                similarity = self.calculate_similarity(author_name, author)
                if similarity >= similarity_threshold :
                    result_list.append((similarity, paper))
                    break
        result_list.sort(key=lambda x: x[0], reverse=True)
        return list(map(lambda x: x[1], result_list))

    def paperByKeywords(self, keywords, similarity_threshold=0.6) :
        result_list = []
        for paper in self.whole_paper_dict.values() :
            if paper.keywords is None :
                continue
            for keyword in paper.keywords :
                similarity = self.calculate_similarity(keyword, keywords)
                if similarity >= similarity_threshold :
                    result_list.append((similarity, paper))
                    break
        result_list.sort(key=lambda x: x[0], reverse=True)
        return list(map(lambda x: x[1], result_list))

    def paperByConference(self, conference, similarity_threshold=0.4) :
        result_list = []
        for paper in self.whole_paper_dict.values() :
            similarity = self.calculate_similarity(paper.conference_acronym, conference)
            if similarity >= similarity_threshold :
                result_list.append((similarity, paper))
        result_list.sort(key=lambda x: x[0], reverse=True)
        return list(map(lambda x: x[1], result_list))

    def authorByName(self, name) :
        if name not in self.whole_author_dict :
            return Author(name=name, query_handler=self)
        return self.whole_author_dict[name]

    def calculate_similarity(self, name1, name2):
        return Levenshtein.ratio(name1, name2)

