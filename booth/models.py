from django.db import models
import random, string

class Booth(models.Model):
    name = models.CharField(max_length=30)
    TYPE_CHOICES=(
        ('주간부스','주간부스'),
        ('야간부스','야간부스'),
        ('플리마켓','플리마켓'),
        ('푸드트럭','푸드트럭'),
    )
    type=models.CharField(max_length=10, choices=TYPE_CHOICES)
    operator=models.CharField(max_length=20)
    start_at=models.DateField(null=True, blank=True)
    end_at=models.DateField(null=True, blank=True)
    LOCATION_CHOICES=(
        ('이해랑예술극장','이해랑예술극장'),
        ('나체밭','나체밭'),
        ('사회과학관','사회과학관'),
        ('혜화관','혜화관'),
        ('혜화별관','혜화별관'),
        ('법학관','법학관'),
        ('명진관','명진관'),
        ('본관','본관'),
        ('만해광장','만해광장'),
        ('학생회관','학생회관'),
        ('학림관','학림관'),
    )
    location=models.CharField(max_length=10, choices=LOCATION_CHOICES)
    description=models.CharField(max_length=30)
    menu=models.JSONField(default=dict)
    concept=models.CharField(max_length=100)

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

class Comment(models.Model):
    booth=models.ForeignKey(Booth, on_delete=models.CASCADE)
    writer=models.CharField(max_length=30)
    content=models.TextField()
    password=models.PositiveSmallIntegerField(null=False, blank=False)
    ip_address=models.CharField(max_length=100)
    is_deleted=models.BooleanField(default=True)
    created_at=models.DateTimeField(null=True, blank=True)

class CommentReply(models.Model):
    comment=models.ForeignKey(Comment, on_delete=models.CASCADE)
    writer=models.CharField(max_length=30)
    content=models.TextField()
    password=models.PositiveSmallIntegerField(null=False, blank=False)
    ip_address=models.CharField(max_length=100)
    is_deleted=models.BooleanField(default=True)
    created_at=models.DateTimeField(null=True, blank=True)