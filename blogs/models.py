from django.db import models
from datetime import datetime

# Create your models here.
class Blog(models.Model):
    image = models.ImageField(upload_to='images/blogs', null=True, blank=True, max_length=50000)
    title = models.CharField(max_length=500)
    content = models.CharField(max_length=100000)
    createdAt = models.DateTimeField(default=datetime.now, blank=True)
    