from django.contrib.auth.models import AbstractUser
from django.db import models
from ckeditor.fields import RichTextField

# Create your models here.


class User(AbstractUser):
    class Meta:
        db_table = 'User'
    avatar = models.ImageField(upload_to='uploads/%Y/%m')


class Category(models.Model):
    class Meta:
        db_table = 'Category'
        ordering = ['id']

    name = models.CharField(max_length=100, null=False, unique=True)

    def __str__(self):
        return self.name


class Base(models.Model):
    class Meta:
        abstract = True

    subject = models.CharField(max_length=100, null=False)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.subject


class Course(Base):
    class Meta:
        ordering = ['id']
        db_table = 'Course'
        unique_together = ('subject', 'category')

    description = models.TextField(null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    image = models.ImageField(upload_to='course/%Y/%m', default=None)


class Lesson(Base):
    class Meta:
        ordering = ['id']
        db_table = 'Lesson'
        unique_together = ('subject', 'course')

    # content = models.TextField()
    content = RichTextField()
    image = models.ImageField(upload_to='lessons/%Y/%m', default=None)
    course = models.ForeignKey(Course, related_name='lesson', on_delete=models.CASCADE)
    tags = models.ManyToManyField('Tag', blank=True, null=True)


class Tag(models.Model):
    class Meta:
        db_table = 'Tag'
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
