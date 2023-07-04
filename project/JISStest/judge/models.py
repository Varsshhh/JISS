from django.db import models

class identity(models.Model):
    cin = models.IntegerField()


class keyword(models.Model):
    keyword = models.CharField(max_length=50)