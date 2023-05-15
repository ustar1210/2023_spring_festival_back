from django.db import models
from booth.models import *
from notification.models import *

# Create your models here.
class Comment(models.Model):
    booth=models.ForeignKey(Booth, on_delete=models.CASCADE)
    writer=models.CharField(max_length=30)
    content=models.TextField()
    password=models.PositiveSmallIntegerField(null=False, blank=False)
    ip_address=models.CharField()
    is_deleted=models.BooleanField(default=True)
    created_at=models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f'{self.booth}|{self.content[:10]}'

class CommentReply(models.Model):
    comment=models.ForeignKey(Comment, on_delete=models.CASCADE)
    writer=models.CharField(max_length=30)
    content=models.TextField()
    password=models.PositiveSmallIntegerField(null=False, blank=False)
    ip_address=models.CharField()
    is_deleted=models.BooleanField(default=True)
    created_at=models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f'{self.comment[:10]}|{self.content[:10]}'