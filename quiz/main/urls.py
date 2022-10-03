from django.urls import path,include
from .views import attempt_limet, category_questions, home, register,all_categories, result,submit_answer

urlpatterns = [
    path('',home,name='home'),
    path('accounts/register/',register,name='register'),
    path('all-categories/',all_categories,name='all-categories'),
    path('category-questions/<int:cat_id>/',category_questions,name='category_questions'),
    path('submit-answer/<int:cat_id>/<int:quest_id>/',submit_answer,name='submit_answer'),
    path('attempty_limet/',attempt_limet,name="attempty-limet"),
    path('result/',result,name='result')


]
