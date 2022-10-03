from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class QuizCategory(models.Model):
    title = models.CharField(max_length=100)
    detail = models.TextField()
    image = models.ImageField(upload_to='quizcategory')

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self) -> str:
        return self.title

class QuizQuestion(models.Model):
    category = models.ForeignKey(QuizCategory,on_delete=models.CASCADE)
    question = models.TextField()
    opt_1 = models.CharField(max_length=200)
    opt_2 = models.CharField(max_length=200)
    opt_3 = models.CharField(max_length=200)
    opt_4 = models.CharField(max_length=200)
    level = models.CharField(max_length=100)
    time_limit = models.IntegerField()
    right_opt = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = 'Questions'    

    def __str__(self) -> str:
        return self.question 

class UserSubmittedAnswer(models.Model):
    question = models.ForeignKey(QuizQuestion, on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    right_answer = models.CharField(max_length=200)

    class Meta:
        verbose_name_plural = 'User submitted Answer'

class UserCategoryAttempts(models.Model):
    category = models.ForeignKey(QuizCategory,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    attempt_time = models.DateTimeField(auto_now_add = True)

    class Meta:
        verbose_name_plural = 'User Atempts Category'