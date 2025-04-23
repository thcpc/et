from django.db import models
from sqlalchemy.orm import relationship
import et.models as MetaModel


# Create your models here.
class LabelCategory(MetaModel.LabelCategoryBase):
    labels = relationship('label.models.Label',
                          back_populates='on_category',
                          order_by="et.models.LabelBae.name",
                          lazy="joined")


class Label(MetaModel.LabelBae):
    on_category = relationship('label.models.LabelCategory', back_populates='labels')

