from django.db import models

# Create your models here.
class UserInfo(models.Model):
    '''用户信息模型'''
    UserName=models.CharField(max_length=20)
    PassWord=models.CharField(max_length=20)