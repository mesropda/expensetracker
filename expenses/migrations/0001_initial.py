# Generated by Django 5.0.2 on 2024-02-22 14:35

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('tracker', '0002_userprofile'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transactions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction_type', models.CharField(choices=[('Deposit', 'Deposit'), ('Withdrawal', 'Withdrawal')], max_length=20)),
                ('amount', models.IntegerField()),
                ('category', models.CharField(choices=[('House', 'House'), ('Food', 'Food'), ('Transport', 'Transport'), ('Shopping', 'Shopping'), ('Necessities', 'Necessities'), ('Bills', 'Bills'), ('Leisure', 'Leisure'), ('Other', 'Other')], max_length=20)),
                ('source', models.CharField(choices=[('My account', 'My account'), ('Salary', 'Salary'), ('Gov_Social', 'Gov_Social'), ('Business_Profit', 'Business_Profit'), ('Other', 'Other')], max_length=20)),
                ('date', models.DateField(auto_now=True)),
                ('user', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='User_transactions', to='tracker.userprofile')),
            ],
        ),
    ]
