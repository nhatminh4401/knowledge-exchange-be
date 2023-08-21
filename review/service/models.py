from django.db import models


class Review(models.Model):
    review_ID = models.AutoField(primary_key=True)
    like = models.BooleanField()
    rating = models.IntegerField()
    report = models.CharField(max_length=1000)
    user = models.IntegerField()
    question_ID = models.IntegerField(null=True)
    answer_ID = models.IntegerField(null=True)

    def __str__(self):
        return self.report

    class Meta:
        db_table = "review"
        verbose_name = "Review"
        verbose_name_plural = "Review"
