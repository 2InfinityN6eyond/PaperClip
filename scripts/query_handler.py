import os
import multiprocessing as mp

from containers import Paper, Author, Institution, Expertise


class QueryHandler_(mp.Process) :
    def __init__(self, query, ) :
        pass


class QueryHandler :
    def __init__(
        self,
        whole_paper_list,
        whole_author_list,
        whole_institution_list,
        whole_expertise_list,
    ) :
        self.whole_paper_list = whole_paper_list
        self.whole_author_list = whole_author_list
        self.whole_institution_list = whole_institution_list
        self.whole_expertise_list = whole_expertise_list


