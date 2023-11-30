# Paper Metadata Crawler

### 작동 방식 및 사용 방법
- Google Schorlar 에서 저자 이름을 검색하면 그 저자의 분야 (ex: Machine Learning, Computer Vision, ...) 가 있다.
- 이를 label이라고 한다.
- label 링크로 들어가면 해당 분야의 저자들이 나열되어 있다.
- authors_from_label.ipynb 로 해당 분야의 저자들의 이름을 읽어와 author_name_list.json 에 저장한다.
- gschorlar_crawler.ipynb 를 이용해 저자들과 논문들에 대한 정보를 읽어온다.