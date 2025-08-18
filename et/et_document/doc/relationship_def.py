from sqlalchemy.orm import relationship

import et.models as MetaModel


class Document(MetaModel.DocumentBase):
    pages = relationship('et_document.doc.relationship_def.Page',
                         back_populates='parent_doc',
                         order_by="et_document.doc.relationship_def.Page.id")
    labels = relationship('et_document.doc.relationship_def.DocumentLabel',
                          back_populates='parent_doc',
                          order_by="et_document.doc.relationship_def.DocumentLabel.id")
    snapshots = relationship('et_document.doc.relationship_def.SnapshotDocument',
                             back_populates='base_doc')
    audits = relationship('et_document.doc.relationship_def.DocumentAudit',
                          back_populates='parent_doc')


class DocumentAudit(MetaModel.DocumentAuditBase):
    parent_doc = relationship('et_document.doc.relationship_def.Document',
                              back_populates='audits')


class Page(MetaModel.PageBase):
    parent_doc = relationship('et_document.doc.relationship_def.Document',
                              back_populates='pages')
    paragraphs = relationship('et_document.doc.relationship_def.Paragraph',
                              back_populates='parent_page', lazy="joined",
                              order_by="et.models.ParagraphBase.order")


class Paragraph(MetaModel.ParagraphBase):
    parent_page = relationship('et_document.doc.relationship_def.Page',
                               back_populates='paragraphs')
    his_contents = relationship('et_document.doc.relationship_def.HisContent',
                                back_populates='paragraph', uselist=True)


class HisContent(MetaModel.HisContentBase):
    paragraph = relationship('et_document.doc.relationship_def.Paragraph',
                             back_populates='his_contents')


class DocumentLabel(MetaModel.DocumentLabelBase):
    parent_doc = relationship('et_document.doc.relationship_def.Document',
                              back_populates='labels')
    detail = relationship('et_document.doc.relationship_def.Label',
                          back_populates='ref_doc_label', uselist=False, lazy="joined")


class Label(MetaModel.LabelBae):
    parent_cat = relationship('et_document.doc.relationship_def.LabelCategory',
                              back_populates='labels')
    ref_doc_label = relationship('et_document.doc.relationship_def.DocumentLabel',
                                 back_populates='detail')


class LabelCategory(MetaModel.LabelCategoryBase):
    labels = relationship('et_document.doc.relationship_def.Label',
                          back_populates='parent_cat',
                          order_by="et.models.LabelBae.name")


class SnapshotDocument(MetaModel.SnapshotDocumentBase):
    pages = relationship('et_document.doc.relationship_def.SnapshotPage',
                         back_populates='parent_doc', lazy="joined")
    base_doc = relationship('et_document.doc.relationship_def.Document',
                            back_populates='snapshots')


class SnapshotPage(MetaModel.SnapshotPageBase):
    parent_doc = relationship('et_document.doc.relationship_def.SnapshotDocument',
                              back_populates='pages')
    paragraphs = relationship('et_document.doc.relationship_def.SnapshotParagraph',
                              back_populates='parent_page')


class SnapshotParagraph(MetaModel.SnapshotParagraphBase):
    parent_page = relationship('et_document.doc.relationship_def.SnapshotPage',
                               back_populates="paragraphs")


