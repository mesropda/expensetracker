from django.db import models
from django.contrib.auth.models import User
from tracker.models import UserProfile
# Create your models here.


EXPENSE_CATEGORY_CHOICES = [
    ("House", "House"),
    ("Food", "Food"),
    ("Transport", "Transport"),
    ("Shopping", "Shopping"),
    ("Necessities", "Necessities"),
    ("Bills", "Bills"),
    ("Leisure", "Leisure"),
    ("Other", "Other")
]

SOURCE_CHOICES = [
    ("My account", "My account"),
    ("Salary", "Salary"),
    ("Gov_Social", "Gov_Social"),
    ("Business_Profit", "Business_Profit"),
    ("Other", "Other")
]

TRANSACTION_CHOICES = [
    ("Deposit", "Deposit"),
    ("Withdrawal", "Withdrawal"),
]


class Transactions(models.Model):
    user = models.ForeignKey(
        UserProfile, default=1, related_name="User_transactions", on_delete=models.CASCADE)
    transaction_type = models.CharField(
        max_length=20, choices=TRANSACTION_CHOICES)
    amount = models.IntegerField()
    category = models.CharField(
        max_length=20, choices=EXPENSE_CATEGORY_CHOICES)
    source = models.CharField(max_length=20, choices=SOURCE_CHOICES)
    date = models.DateField(auto_now=True)
