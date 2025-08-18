# from django.db import models
# from sqlalchemy.orm import relationship, validates
#
# from et.exceptions.business_error import InValidUserInfoError
# from et.models import UserBase, UserFingerPrintBase
#
#
# # Create your models here.
#
#
# class User(UserBase):
#     finger_prints = relationship("user.models.UserFingerPrint", back_populates="ref_user")
#
#
# class UserFingerPrint(UserFingerPrintBase):
#     ref_user = relationship("user.models.User", back_populates="finger_prints")
