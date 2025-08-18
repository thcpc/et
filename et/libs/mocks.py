


class Mock:
    _paragraphs = {
        "1": dict(id=1, order=1, contents="paragraphs1", paragraphType="FullText"),
        "2": dict(id=2, order=2, contents="""@startuml
        Bob -> Alice2 : hello
        @enduml""", paragraphType="PlantUml"),
        "3": dict(id=3, order=3, contents="paragraphs3", paragraphType="FullText"),
        "4": dict(id=4, order=1, contents="""@startuml
        Bob -> Alice4 : hello
        @enduml""", paragraphType="PlantUml"),
        "5": dict(id=5, order=2, contents="paragraphs5", paragraphType="FullText"),
        "6": dict(id=6, order=1, contents="paragraphs6", paragraphType="FullText"),
        "7": dict(id=7, order=2, contents="""@startuml
        Bob -> Alice7 : hello
        @enduml""", paragraphType="PlantUml"),
        "8": dict(id=8, order=3, contents="paragraphs8", paragraphType="FullText"),
        "9": dict(id=9, order=1, contents="paragraphs9", paragraphType="FullText"),
        "10": dict(id=10, order=2, contents="""@startuml
        Bob -> Alice10 : hello
        @enduml""", paragraphType="PlantUml"),
        "11": dict(id=11, order=1, contents="paragraphs11", paragraphType="FullText"),
        "12": dict(id=12, order=2, contents="""@startuml
        Bob -> Alice12 : hello
        @enduml""", paragraphType="PlantUml"),
        "13": dict(id=13, order=3, contents="paragraphs13", paragraphType="FullText"),
        "14": dict(id=14, order=4, contents="paragraphs14", paragraphType="FullText")
    }
    _pages = {
        "1": dict(id=1, order=1, name="pages1"),
        "2": dict(id=2, order=2, name="pages2"),
        "3": dict(id=3, order=3, name="pages3"),
        "4": dict(id=4, order=1, name="pages4"),
        "5": dict(id=5, order=1, name="pages5")
    }

    _documents = {
        "1": dict(id=1, name="文档1"),
        "2": dict(id=2, name="文档2")
    }

    _document_with_pages = {
        "1": [1, 2, 3],
        "2": [4, 5]
    }

    _page_with_paragraphs = {
        "1": [1, 2, 3],
        "2": [4, 5],
        "3": [6, 7, 8],
        "4": [9, 10],
        # "4": [9],
        "5": [11, 12, 13, 14]
    }

    @classmethod
    def get_documents(cls):
        mock_data = cls._documents
        return list(mock_data.keys())

    @classmethod
    def get_paragraphs(cls, page_id):
        _paragraphs_id = cls._page_with_paragraphs.get(page_id)
        mock_data = [cls._paragraphs.get(str(paragraph_id)) for paragraph_id in _paragraphs_id]
        mock_data.sort(key=lambda x: x.get("order"))
        return mock_data

    @classmethod
    def get_pages(cls, doc_id):
        _pages_id = cls._document_with_pages.get(doc_id)
        mock_data = [cls._pages.get(str(page_id)) for page_id in _pages_id]
        return mock_data

    @classmethod
    def get_document(cls, doc_id):
        mock_data = cls._documents
        return mock_data.get(doc_id)

    @classmethod
    def get_paragraph(cls, paragraph_id):
        mock_data = cls._paragraphs
        return mock_data.get(paragraph_id)

    @classmethod
    def get_page(cls, page_id):
        mock_data = cls._pages
        return mock_data.get(page_id)

    @classmethod
    def new_paragraph(cls, page_id, contents, paragraph_type):
        last_id = int(list(cls._paragraphs.keys())[-1])
        new_id = last_id + 1
        last_order = len(cls._page_with_paragraphs[str(page_id)])
        new_order = last_order + 1
        cls._paragraphs[str(new_id)] = dict(id=new_id, order=new_order, contents=contents, paragraphType=paragraph_type)
        cls._page_with_paragraphs[str(page_id)].append(new_id)
        return new_id, new_order

    @classmethod
    def update_paragraph(cls, paragraph_id, contents):
        cls._paragraphs[str(paragraph_id)]["contents"] = contents
        print(cls._paragraphs[str(paragraph_id)])

    @classmethod
    def move_paragraph(cls, change_orders: list):
        for change_order in change_orders:
            cls._paragraphs[str(change_order.get("id"))]["order"] = change_order.get("order")

    @classmethod
    def delete_paragraph(cls, paragraph_id):
        cls._paragraphs.pop(str(paragraph_id))
        for page, paragraphs in cls._page_with_paragraphs.items():
            if int(paragraph_id) in paragraphs:
                paragraphs.remove(int(paragraph_id))
