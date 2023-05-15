from django.db import models

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

class NotificationImage(models.Model):
    notification=models.ForeignKey(Notification, on_delete=models.CASCADE)