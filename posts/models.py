from django.db import models
from django.core.validators import MinLengthValidator
from django.db.models.deletion import CASCADE, DO_NOTHING
from django.db.models.fields.files import ImageField
from .validators import validate_symbols
from django.contrib.auth.models import AbstractUser


# Create your models here.
class Class(models.Model):
  title = models.CharField(max_length=50, unique=True, error_messages={'unique': "이미 있는 클레스이군요!"})
  dt_created = models.DateTimeField(verbose_name="Date Created", auto_now_add=True)
  
  def __str__(self):
    return self.title

class Lesson(models.Model):
  title = models.CharField(max_length=50)
  dt_created = models.DateTimeField(verbose_name="Date Created", auto_now_add=True)
  
  upclass = models.ForeignKey(Class, on_delete=CASCADE)


  def __str__(self):
    return self.title

class User(AbstractUser):
  pass

class Post(models.Model):
  title = models.CharField(max_length=50)
  content = models.TextField(validators=[
      MinLengthValidator(10, '너무 짧군요! 10자 이상 적어주세요.')
  ])

  image1 = models.ImageField(upload_to="post_pics", blank=True)
  image2 = models.ImageField(upload_to="post_pics", blank=True)
  image3 = models.ImageField(upload_to="post_pics", blank=True)

  dt_created = models.DateTimeField(verbose_name="Date Created", auto_now_add=True)
  
  uplesson = models.ForeignKey(Lesson, on_delete=CASCADE)

  author = models.ForeignKey(User, on_delete=DO_NOTHING)

  def __str__(self):
    return self.title


class Comment(models.Model):
  comment = models.CharField(max_length=50)
  dt_created = models.DateTimeField(verbose_name="Date Created", auto_now_add=True)

  uppost = models.ForeignKey(Post, on_delete=CASCADE)

  author = models.ForeignKey(User, on_delete=DO_NOTHING)

  def __str__(self):
    return self.comment