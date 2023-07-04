from django.db import models

class identity(models.Model):
    cin = models.IntegerField()

class keyword(models.Model):
    keyword = models.CharField(max_length=50)

# class payment(models.Model):
#     value = models.IntegerField()
#     # username = cin = models.CharField(max_length=50)

