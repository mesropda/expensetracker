from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Contact(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    emial = models.EmailField()
    message = models.TextField()
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.first_name+"-"+self.last_name


PROFESSION_CHOICES = [
    ("Employee", "Employee"),
    ("Business", "Business"),
    ("Student", "Student"),
    ("Other", "Other")
]


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profession = models.CharField(max_length=20, choices=PROFESSION_CHOICES)
    pic = models.ImageField(upload_to='profile_pic', blank=True)
    savings = models.IntegerField(null=True, blank=True)
    income = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.user.username
