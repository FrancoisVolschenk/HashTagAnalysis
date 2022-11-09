from django.db import models

# Create your models here.
class Person(models.Model):
    Name = models.TextField()
    Age = models.IntegerField()
    Active = models.BooleanField()

    def __str__(self):
        return self.Name