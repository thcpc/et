from sqlalchemy.orm import relationship
import et.models as MetaModel


class User(MetaModel.UserBase):
    finger_prints = relationship("user.relationship_def.UserFingerPrint", back_populates="ref_user")


class UserFingerPrint(MetaModel.UserFingerPrintBase):
    ref_user = relationship("user.relationship_def.User", back_populates="finger_prints")
