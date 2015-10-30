# Create your models here.
from django.db import models



class Skills(models.Model):
    skill_name = models.CharField(max_length=300, null=False)

    def __str__(self):
        return self.skill_name

class Profile(models.Model):
    name = models.CharField(max_length=300)
    title = models.CharField(max_length=300, default=None, null=True)
    email = models.CharField(max_length=300, default=None, null=True)
    phone = models.CharField(max_length=300, default=None, null=True)
    im = models.CharField(max_length=300, default=None, null=True)
    summary = models.TextField(default=None, null=True)
    skills = models.ManyToManyField(Skills)
    url = models.TextField(unique=True)
    address = models.CharField(max_length=300, default=None, null=True)
    advice_to_connect = models.TextField(default=None, null=True)

    def __str__(self):
        return self.name


