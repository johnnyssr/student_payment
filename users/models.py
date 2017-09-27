from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    nickname = models.CharField(max_length=50, blank=True)
    student_id  = models.IntegerField(unique=True)

    class Meta(AbstractUser.Meta):
        ordering = ['nickname']

class student(models.Model):
    # 学号，唯一
    student_id = models.IntegerField(primary_key=True)
    student_name = models.CharField(max_length=30)
    register_date = models.DateField()
    work_name =  models.CharField(max_length=30)
    work_pay = models.FloatField(default=10.0)
    time = models.FloatField()
    email = models.EmailField()
    # 逻辑删除，默认不删除
    #idDelete = models.BooleanField(default=False)

    class Meta:
        ordering = ['student_id']

    def __str__(self):
        return self.student_id

class time_record(models.Model):
    student = models.ForeignKey(student)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()