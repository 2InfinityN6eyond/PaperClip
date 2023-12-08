

## Bridging the gap between database and GUI
When designing program architecture, we found following problems.
- informtion inside database is organized as property-centered (column-centered, or tabular) form, as we use relational database.
    - ex) 'paper' table has title, doi, author, abstract, etc  columns.
    - we could think that information inside db is managed as column-centered way
- however, the GUI needs object - centered form. 
    - when plotting information about certain paper, we need every information of corresponding paper which is spreaded across records, across many tables.
- so we have to aggregate information for each paper/author from db and serve it to GUI when needed.
- it is tedious to manage db connection across every parts of GUI that need information.  

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