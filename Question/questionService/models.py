from django.db import models

# Create your models here.
class Category(models.Model):
    category_ID = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    
    class Meta:
        db_table = "category"
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

class Tag(models.Model):
    tag_ID = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    
    class Meta:
        db_table = "tag"
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'


class Question(models.Model):
    question_ID = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    content = models.CharField(max_length=1000)
    status = models.CharField(max_length=50)
    user = models.CharField(max_length=50)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, related_name="questions")
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(null=True)

    def __str__(self):
        return self.title
    
    class Meta:
        db_table = "question"
        verbose_name = 'Question'
        verbose_name_plural = 'Questions'