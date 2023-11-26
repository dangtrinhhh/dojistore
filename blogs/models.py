from django.db import models
from datetime import datetime
from ckeditor.fields import RichTextField 

# Create your models here.
class Blog(models.Model):
    image = models.ImageField(upload_to='images/blogs', null=True, blank=True, max_length=50000)
    title = models.CharField(max_length=500)
    content = RichTextField()
    createdAt = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
        return self.title
    