from django.db import models
import random, string
from notification.models import Notification

# Create your models here.
class Booth(models.Model):
    name=models.CharField(max_length=30)
    TYPE_CHOICES=(
        ('',''),
        ('',''),
        ('',''),
        ('',''),
    )
    type=models.CharField(max_length=4, choices=TYPE_CHOICES)
    operator=models.CharField(max_length=20)
    start_at=models.DateTimeField(null=True, blank=True)
    end_at=models.DateTimeField(null=True, blank=True)
    LOCATION_CHOICES=(
        ('',''),
        ('',''),
        ('',''),
        ('',''),
        ('',''),
        ('',''),
        ('',''),
        ('',''),
        ('',''),
        ('',''),
        ('',''),
        ('',''),
    )
    location=models.CharField(max_length=4, choices=LOCATION_CHOICES)
    description=models.CharField(max_length=30)
    menu=models.JSONField(default=dict)
    concept=models.CharField(max_length=100)

    def __str__(self):
        return self.title

def create_random_number(self):    
    _LENGTH=10
    string_pool=string.ascii_letters+string.digits+string.punctuation
    result=""
    for i in range(_LENGTH):
        result += random.choice(string_pool)
    return result


class Like(models.Model):
    booth=models.ForeignKey(Booth, on_delete=models.CASCADE)
    key=models.CharField(
        max_length=10,
        blank=True,
        editable=False,
        default=create_random_number
    )

    def __str__(self):
        return self.key
    
def image_upload_path(instance, filename):
    return f'{instance.pk}/{filename}'


# 실제 테이블 생성 안되는 Abstract 모델입니다.
class BaseImage(models.Model):
    image=models.ImageField(upload_to=image_upload_path, blank=True, null=True)


# MenuImage (BaseImage 상속)
class MenuImage(models.Model):
    booth=models.ForeignKey(Booth, on_delete=models.CASCADE)


# LogoImage 부스 포스터 (BaseImage 상속)
class LogoImage(models.Model):
    booth=models.ForeignKey(Booth, on_delete=models.CASCADE)


# NotificationImage 공지 이미지 (BaseImage 상속)
class NotificationImage(models.Model):
    notification=models.ForeignKey(Notification, on_delete=models.CASCADE)
