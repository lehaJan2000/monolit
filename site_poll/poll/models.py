from datetime import timezone

from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class User(AbstractUser):
    GENDERS = (
        ('m', 'Мужчина'),
        ('f', 'Женщина')
    )

    fio = models.CharField('ФИО', max_length=150, null=False, blank=False)
    gender = models.CharField('Пол', max_length=1, choices=GENDERS, default=' ')
    username = models.CharField(max_length=150, verbose_name='Никнейм', unique=True, null=False, blank=False)
    birth_date = models.DateField('Дата рождения', default='2004-02-18')
    password = models.CharField(max_length=250, verbose_name='Пароль', null=False, blank=False)
    avatar = models.ImageField(verbose_name='Аватаро4ка', upload_to='photo', blank=False)
    personal_data = models.BooleanField(default=False, blank=False, null=False,
                                        verbose_name='Согласие на обработку персональных данных')

    def __str__(self):
        return f"{self.fio} {self.birth_date}"




class Poll(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь', null=True)
    question = models.TextField(max_length=150)
    option_one = models.CharField(max_length=30)
    option_two = models.CharField(max_length=30)
    option_three = models.CharField(max_length=30)
    option_one_count = models.IntegerField(default=0)
    option_two_count = models.IntegerField(default=0)
    option_three_count = models.IntegerField(default=0)
    startpoll = models.DateTimeField(auto_now_add=True)
    pollcompleted = models.DateTimeField(null=True, blank=True)
    # pub_date = models.DateTimeField(auto_now_add=True)
    # expiration_date = models.DateTimeField(null=True, blank=True)



    def total(self):
        return self.option_one_count + self.option_two_count + self.option_three_count






class Avat(models.Model):
    user = models.ForeignKey(User, verbose_name='ssssssssssss', on_delete=models.CASCADE)
    poll = models.ForeignKey(Poll, verbose_name='sadasfasf', on_delete=models.CASCADE)
