

## General Structure, Architecture

```
GUI
├── README.md
├── scrollable_list.py
│       ScrollableList
│           GUI element scrollable list.
│           Can contains Item class objects
│               example Item classes : PaperItem, PaperClipSearchResultItme
│           When Item inside it 
├── center_section.py
│       CenterSection
├── containers.py
│       Paper
│       Author
├── main.py
│       entry point
├── main_window.py
│       MainWindow
├── paper_clip_search_result_item.py
│       PaperClipSearchResultItem
├── paper_gui.py
│       PaperGUI
├── paper_item.py
│       PaperItem
├── paper_meta_viewer.py
│       PaperMetaViewer
├── popular_papers_window.py
│       PopularPapersWindow
├── query_handler.py
│       
├── related_paper_gui.py
│       RelatedPaperGUI
├── scrap_viewer.py
│       ScrapViewer
└── 
        ScrollableList

```


## Bridging the gap between database and GUI
When designing program architecture, we found following problems.
- Gap between information representation of database and GUI
    - informtion inside database is organized as property-centered (column-centered, or tabular) form, as we use relational database.
        - ex) 'paper' table has title, doi, author, abstract, etc  columns.
        - ex) 'related_works' table has doi, ref_doi, etc columns.
        - we could think that db stores informations as column-centered way.
    - the GUI needs object - centered form. 
        - when plotting information about certain paper, we need every information of corresponding paper, which is spreaded across records and tables.
    - so we have to aggregate information for each paper/author from database to be used in GUI.
- It is tedious to manage db connection across every parts of GUI that need information.  

We created Paper, Author, QureyHander classes to resolve previously mentioned problems, suggesting elegant archiatecture.
- QueryHandler
    - defined at query_handler.py
    - class that takes charge of connecting DB and GUI.
    - every Paper, Author object will have reference to this object when initialized.

- Paper
    - defined at containers.py
    - contains metadata including reference_list, author_list, doi, title of paper
    - contains reference to QueryHandler object.
    - reference_list field
        - GUI expects this field to be a list of Paper objects.
        - however, it is inefficient to instanciate every reference papers and put them inside this field. 
        - So, we used python @property feature.
        - When Paper object is initialized, the reference_list is empty.
        - When GUI accesses Paper.reference_list field, it actually calls getter function, which will get list of Paper object by queriying to QueryHandler object.
        - GUI doesn't care about database at all. It just ask for queryhandler, or accessing field of existing Paper object.

- Author