from sqlalchemy.orm import relationship

import et.models as MetaModel


class Document(MetaModel.DocumentBase):
    pages = relationship('document.models.Page',
                         back_populates='parent_doc',
                         order_by="document.models.Page.id")
    labels = relationship('document.models.DocumentLabel',
                          back_populates='parent_doc',
                          order_by="document.models.DocumentLabel.id")
    snapshots = relationship('document.models.SnapshotDocument',
                             back_populates='base_doc')
    audits = relationship('document.models.DocumentAudit',
                          back_populates='parent_doc')


class DocumentAudit(MetaModel.DocumentAuditBase):
    parent_doc = relationship('document.models.Document',
                              back_populates='audits')


class Page(MetaModel.PageBase):
    parent_doc = relationship('document.models.Document',
                              back_populates='pages')
    paragraphs = relationship('document.models.Paragraph',
                              back_populates='parent_page', lazy="joined",
                              order_by="et.models.ParagraphBase.order")


class Paragraph(MetaModel.ParagraphBase):
    parent_page = relationship('document.models.Page',
                               back_populates='paragraphs')
    his_contents = relationship('document.models.HisContent',
                                back_populates='paragraph', uselist=True)


class HisContent(MetaModel.HisContentBase):
    paragraph = relationship('document.models.Paragraph',
                             back_populates='his_contents')


class DocumentLabel(MetaModel.DocumentLabelBase):
    parent_doc = relationship('document.models.Document',
                              back_populates='labels')
    detail = relationship('document.models.Label',
                          back_populates='ref_doc_label', uselist=False, lazy="joined")


class Label(MetaModel.LabelBae):
    parent_cat = relationship('document.models.LabelCategory',
                              back_populates='labels')
    ref_doc_label = relationship('document.models.DocumentLabel',
                                 back_populates='detail')


class LabelCategory(MetaModel.LabelCategoryBase):
    labels = relationship('document.models.Label',
                          back_populates='parent_cat',
                          order_by="et.models.LabelBae.name")


class SnapshotDocument(MetaModel.SnapshotDocumentBase):
    pages = relationship('document.models.SnapshotPage',
                         back_populates='parent_doc', lazy="joined")
    base_doc = relationship('document.models.Document',
                            back_populates='snapshots')


class SnapshotPage(MetaModel.SnapshotPageBase):
    parent_doc = relationship('document.models.SnapshotDocument',
                              back_populates='pages')
    paragraphs = relationship('document.models.SnapshotParagraph',
                              back_populates='parent_page')


class SnapshotParagraph(MetaModel.SnapshotParagraphBase):
    parent_page = relationship('document.models.SnapshotPage',
                               back_populates="paragraphs")
