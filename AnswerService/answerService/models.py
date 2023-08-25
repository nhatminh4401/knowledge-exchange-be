from django.db import models

# Create your models here.


class Answer(models.Model):
    answer_ID = models.AutoField(primary_key=True)
    content = models.CharField(max_length=1000)
    user = models.IntegerField()
    preAnswer_ID = models.IntegerField(null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(null=True)
    question_ID = models.IntegerField()

    def __str__(self):
        return self.title

    class Meta:
        db_table = "answer"
        verbose_name = 'Answer'
        verbose_name_plural = 'Answers'


class ReferenceLink(models.Model):
    ref_ID = models.AutoField(primary_key=True)
    content = models.CharField(max_length=500)
    answer_ID = models.ForeignKey(Answer, on_delete=models.CASCADE)

    class Meta:
        db_table = "referencelink"
        verbose_name = 'Reference link'
        verbose_name_plural = 'Reference links'


class Image(models.Model):
    img_ID = models.AutoField(primary_key=True)
    content = models.CharField(max_length=500)
    answer_ID = models.ForeignKey(Answer, on_delete=models.CASCADE)

    class Meta:
        db_table = "image"
        verbose_name = 'Image'
        verbose_name_plural = 'Images'
