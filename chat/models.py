# from django.db import models
# from django.utils.six import python_2_unicode_compatible
#
#
# @python_2_unicode_compatible
# class Room(models.Model):
#     """
#     A room for people to chat in.
#     """
#
#     # Room title
#     title = models.CharField(max_length=255)
#
#     # If only "staff" users are allowed (is_staff on django's User)
#     staff_only = models.BooleanField(default=False)
#
#     def str(self):
#         return self.title
