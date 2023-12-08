# Overal Description of GUI

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

## General Structure, Architecture
``` bash
GUI
├── README.md
├── query_handler.py
│       QueryHandler
│           Be In charge of connecting GUI and Database
├── containers.py
│       Paper
│           representing paper. encapsulates information about paper
│           every instance of Paper holds reference to QueryHandler,
│           and make query to db just-in-time, making GUI does not care about DB
│       Author
│           representing author. encapsulates information about paper
│           every instance of Author holds reference to QueryHandler,
├── scrollable_list.py
│       ScrollableList
│           GUI element scrollable list.
│           Used in ScrapViewer, ScrapViewer, PaperGUI, RelatedPaperGUI, CenterSection
│           Can contains Item class objects
│               example Item classes : PaperItem, PaperClipSearchResultItme
│           stores reference to parent widget
│           When Item inside it is clicked, propagete information to parent class
├── paper_item.py
│       PaperItem
│           unit that saved inside ScrollableList
│           contains clip button, representing if the paper is clipped.
│           which changed when clicked.
├── paper_clip_search_result_item.py
│       PaperClipSearchResultItem
│           unit that saved inside ScrollableList
├── scrap_viewer.py
│       ScrapViewer
│           show ScrollableList that contains papers that was clipped as PaperItem
├── center_section.py
│       CenterSection
│           UI component in the middle of main program.
│           contains search bar, option dropdown menu, ScrollableList showing search result as PaperClipSearchResultItem
├── paper_meta_viewer.py
│       PaperMetaViewer
│           Plots metadata about paper including : title, doi, authors, abstracts, ...
├── paper_gui.py
│       PaperGUI
│           Plot information about paper.
│           Consist of :
│               PaperMetaViewer that plots information about corresponding paper
│               ScrollableList  that contains PaperItem instances that plotting each referenced papers
├── related_paper_gui.py
│       RelatedPaperGUI
│           almost same as PaperGUI, but opened in seperate window
├── main_window.py
│       MainWindow
│           main window.
│           combined with three section : ScrapeViewer, CenterSection, PaperGUI
├── popular_papers_window.py
│       PopularPapersWindow
│           shows up when popular_paper_window_button inside CenterSection is clicked
│           query and shows keyword that most appeared
└──  main.py
        entry point
        parse cmd line arguement, initialize QueryHandler, MainWindow
        start PyQt event loop
```
