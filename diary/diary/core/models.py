from django.db import models

# Create your models here.

from django.db import models

class Entry(models.Model):
    
    """ Model for diary entry """
    
    class meta:
        verbose_name = "Diary Entry"
        verbose_name_plural = "Diary Entries"
    
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE)
    
    def __str__(self):
        return self.title


