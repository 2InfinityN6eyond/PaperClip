# Paper Metadata Crawler

## Architecture
- containers.py
    - contains data classes of paper, author, expertise (we use this as keyword), journal/conference
    - each data classes has serialize-to-json method, and deserialize-from-json method.
    - fields of each data classes are not well-organized.
        - Paper
            - represents academic paper
            - we use DOI as key. DOI is obtained by querying to crossref API
            - main fields
                - google_schorlar_metadata
                    - filled by gschorlar_crawler
                    - contains title of paper, autor name list
                - crossref_json
                    - filled by crossref_fetcher
                    - contains reference_list, doi, author name list, ISSN of conference/journal
        - Author
            - represents author
            - We cannot found something to use as key.
            - some papers can give ORCID of authors from crossref API, but it was not typical.
        - Expertise
            - represents author's expertise academic field.
            - name of expertise can serve as key.
            - used google schorlar label as expertise
        - JournalConference
            - represents journal/conference.
            - ISSN is used as key
            - we failed to distinguish between journal and conference

        - Institution
            - representing institution.

- authors_from_label.ipynb
    - google schorlar offers label property, which lists authors of following academic field
        - ex) https://scholar.google.com/citations?view_op=search_authors&hl=ko&mauthors=label:machine_learning
    - this notebook will collect user names of following field
    - user should get URL of label search result, and put it to TARGET_LABEL_URL.
        - user could get label search result URL from expertise_dict.json which is generated/updated by gschorlar_crawler_without_captha_avoidance.ipynb

- gschorlar_crawler_without_captcha_avoidance.ipynb
    - using author name from author_name_list.json acquired by authors_from_label.ipynb, collect author profile and papers that corresponding author wrote.
    - 
    - this file does not contains reCAPTCHA avoidance feature, but it will pause crawling and wait for user input when reCAPTCHA is detected.
    - user can manually solve captcha and continue. google won't ask for verification friquently if user execute the program not so much.

- fetch_from_crossref.ipynb
    - read whole_paper_dict.json file saved by gschorlar_crawler, and fill advanced information about papers by querying to crossref API
    
- issn_crawler.ipynb
    - read processed_paper_dict.json file saved by fetch_from_crossref.ipynb, get set of issn, then crawl issn portal to get information of corresponding conference/journal

- preprocessing.ipynb
    - read the json files saved from the crawler, and preprocess the data by combining information in each website, refining the data, and dropping the null / duplicate datas.