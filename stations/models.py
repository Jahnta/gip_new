from django.db import models

class Station(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField(max_length=300, null=True, blank=True)

    def __str__(self):
        return self.name

# Create your models here.
