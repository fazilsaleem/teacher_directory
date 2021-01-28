from django.db import models
from django.contrib.auth.models import User


# Create your models here.


GENDER_MALE = 'Male'
GENDER_FEMALE = 'Female'
GENDER_OTHER = 'Other'
GENDER = [(GENDER_MALE,'Male'),
            (GENDER_FEMALE,'Female'),
            (GENDER_OTHER,'Other')]


class AbstractBase(models.Model):
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True

class Role(AbstractBase):
    """
    User roles can be used to categoris users Eg, admin, staff etc.
    """
    role_name = models.CharField(max_length=250)
    is_active = models.BooleanField(default=True)
    role_priority = models.PositiveIntegerField(null=True,blank=True)


    def __str__(self):
        return self.role_name

class UserProfile(AbstractBase):

    """
    Holds fields for users account details who can login to our system.
    """
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name="user_profile",null=True,blank=True)
    email = models.CharField(max_length=100,null=True,blank=True)
    country_code = models.CharField(max_length=10,null=True,blank=True,default='+91')
    phone_number = models.CharField(max_length=50,null=True,blank=True)
    first_name = models.CharField(max_length=50,null=True,blank=True)
    last_name = models.CharField(max_length=50,null=True,blank=True)
    gender = models.CharField(max_length=10, choices=GENDER)
    date_of_birth = models.DateField(null=True,blank=True)
    role = models.ForeignKey(Role,related_name="user_role",on_delete=models.CASCADE,null=True,blank=True)



    def __str__(self):
        return self.email
    

    def get_full_name(self):
        if self.first_name and self.last_name:
            return f'{self.first_name} {self.last_name}'
        else:
            return 'User'
    
