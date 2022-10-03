from django.contrib import admin

from main.models import QuizCategory, QuizQuestion, UserCategoryAttempts, UserSubmittedAnswer

# Register your models here.

admin.site.register(QuizCategory)

class QuizQuestionAdmin(admin.ModelAdmin):
    list_display = ['question','level']
admin.site.register(QuizQuestion,QuizQuestionAdmin)

class UserSubmittedAnswerAdmin(admin.ModelAdmin):
    list_display = ['id','question','user','right_answer']
admin.site.register(UserSubmittedAnswer,UserSubmittedAnswerAdmin)

class UserCategoryAttemptsAdmin(admin.ModelAdmin):
    list_display = ['category','user','attempt_time']
admin.site.register(UserCategoryAttempts ,UserCategoryAttemptsAdmin)

