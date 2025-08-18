from django.db import models
from sqlalchemy.orm import relationship
import et.models as MetaModel


# Create your models here.
class LabelCategory(MetaModel.LabelCategoryBase):
    labels = relationship('et_document.label.relationship_def.Label',
                          back_populates='on_category',
                          order_by="et.models.LabelBae.name",
                          lazy="joined")


class Label(MetaModel.LabelBae):
    on_category = relationship('et_document.label.relationship_def.LabelCategory', back_populates='labels')
