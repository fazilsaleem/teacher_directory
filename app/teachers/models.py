from django.db import models
from administration.models import AbstractBase, UserProfile

# Create your models here.

# class Organization(AbstractBase):
#     organisation_name = models.CharField(max_length=200)
#     is_active=models.BooleanField(default=True)
#     address = models.TextField(blank=True, null=True)

#     def  __str__(self):
#         return self.organisation_name

class Subjects(AbstractBase):
    subject_name = models.CharField(max_length=200)
    is_active=models.BooleanField(default=True)

    def  __str__(self):
        return self.subject_name


class Teachers(AbstractBase):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.CharField(max_length=100,unique=True)
    phone_number = models.CharField(max_length=20,null=True,blank=True)
    room_number = models.CharField(max_length=20, blank=True, null=True)
    profile_picture = models.ImageField(upload_to="teacher_profile", null=True, blank=True)
    subjects_taught = models.ManyToManyField(Subjects,blank=True, related_name='subjects')
    organisation = models.CharField(blank=True, null=True, max_length=100)
    is_active=models.BooleanField(default=True)

    def  __str__(self):
        return self.email


