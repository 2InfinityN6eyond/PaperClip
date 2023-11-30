import os
import json
from containers import Institution, Author, Paper, Expertise


if __name__ == "__main__" :
    institution_dict = {}
    expertise_dict = {}
    whole_author_list = []
    whole_paper_dict = {}

    INSTITUTION_FILE_PATH = "./institution_dict.json"
    if os.path.exists(INSTITUTION_FILE_PATH) :
        with open(INSTITUTION_FILE_PATH, "r") as f :
            institution_dict_raw = json.load(f)
        for k, v in institution_dict_raw.items() :
            institution_dict[k] = Institution(**v)

    EXPERTISE_FILE_PATH = "./expertise_dict.json"
    if os.path.exists(EXPERTISE_FILE_PATH) :
        with open(EXPERTISE_FILE_PATH, "r") as f :
            expertise_dict_raw = json.load(f)
        for k, v in expertise_dict_raw.items() :
            expertise_dict[k] = Expertise(**v)

    AUTHOR_FILE_PATH = "./author_list.json"
    if os.path.exists(AUTHOR_FILE_PATH) :
        with open(AUTHOR_FILE_PATH, "r") as f :
            author_list_raw = json.load(f)
        for author in author_list_raw :
            whole_author_list.append(Author(**author))

    WHOLE_PAPER_FILE_PATH = "./whole_paper_dict.json"
    if os.path.exists(WHOLE_PAPER_FILE_PATH) :
        with open(WHOLE_PAPER_FILE_PATH, "r") as f :
            whole_paper_dict = json.load(f)
        for k, v in whole_paper_dict.items() :
            whole_paper_dict[k] = Paper(**v)

    print(f"number of institution : {len(institution_dict)}")
    print(f"number of expertise : {len(expertise_dict)}")
    print(f"number of author : {len(whole_author_list)}")
    print(f"number of paper : {len(whole_paper_dict)}")
