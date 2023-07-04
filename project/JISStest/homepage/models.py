

from django.db import models
from django.contrib.auth.models import AbstractUser



class User(AbstractUser):
    
#     class Role(models.TextChoices):
#         ADMIN = "ADMIN", 'Admin'
#         REGISTRAR = "REGISTRAR", 'Registrar'
#         LAWYER = "LAWYER", 'Lawyer'
#         JUDGE = "JUDGE", 'Judge'
        
#     base_role = Role.ADMIN
    
#     role = models.CharField(max_length=50, choices=Role.choices)
    
#     def save(self, *arg, **kwargs):
#         if not self.pk:
#             self.role = self.base_role
#             return super().save(*arg, **kwargs)

    is_admin = models.BooleanField(default=False) 
    is_judge = models.BooleanField(default=False)    
    is_lawyer = models.BooleanField(default=False)
    is_registrar = models.BooleanField(default=False)
    credits= models.IntegerField(default=0)
    def __str__(self):
        return self.username
    
    def __call__(self):
        return self.credits



class user_details(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)




    