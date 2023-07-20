from django.db import models
from UserApp.models import User
# Create your models here.


class Category(models.Model):
    category_ID = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)

class Tag(models.Model):
    tag_ID = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)


class Question(models.Model):
    question_ID = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    content = models.CharField(max_length=1000)
    status = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag)
    created_date = models.DateTimeField()
    updated_date = models.DateTimeField()

    def __str__(self):
        return self.title


class Answer(models.Model):
    answer_ID = models.AutoField(primary_key=True)
    content = models.CharField(max_length=50)
    status = models.CharField(max_length=50)
    created_date = models.DateTimeField()
    updated_date = models.DateTimeField()
    question_ID = models.ForeignKey(Question, on_delete=models.CASCADE)
    user_ID = models.ForeignKey(User, on_delete=models.CASCADE)


class Review(models.Model):
    review_ID = models.AutoField(primary_key=True)
    rating = models.IntegerField()
    report = models.CharField(max_length=50)
    created_date = models.DateTimeField()
    updated_date = models.DateTimeField()
    user_ID = models.ForeignKey(User, on_delete=models.CASCADE)
    question_ID = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer_ID = models.ForeignKey(Answer, on_delete=models.CASCADE)


class ReferenceLink(models.Model):
    ref_ID = models.AutoField(primary_key=True)
    content = models.CharField(max_length=500)
    question_ID = models.ForeignKey(Question, on_delete=models.CASCADE)


# class Image(models.Model):
