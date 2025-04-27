from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class ward_no(models.Model):
    name = models.CharField(max_length=3)

    def __str__(self):
        return self.name
    
class dept(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class status(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Post(models.Model):
    host = models.ForeignKey(User, on_delete = models.SET_NULL, null = True)
    dept = models.ForeignKey(dept, on_delete = models.SET_NULL, null = True)
    ward_no = models.ForeignKey(ward_no, on_delete = models.SET_NULL, null=True)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(null=True, blank=True, upload_to='images/')
    created = models.DateTimeField(auto_now_add=True)
    status = models.ForeignKey(status, on_delete= models.SET_NULL, null=True, default="Pending")

    class Meta:
        ordering = ['-created']
    