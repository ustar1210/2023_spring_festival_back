from django.db import models

# Create your models here.
class Notification(models.Model):
    title=models.CharField(max_length=30)
    TYPE_CHOICES=(
        ('main','주요'),
        ('festival','축제'),
        ('event','이벤트'),
        ('etc','기타'),
    )
    type=models.CharField(max_length=10, choices=TYPE_CHOICES)
    content=models.TextField()
    created_at=models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.title
    