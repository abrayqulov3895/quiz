from datetime import timedelta
from django.http import HttpResponse
from django.shortcuts import redirect, render
from .forms import RegisterUser
from .models import QuizCategory, QuizQuestion, UserCategoryAttempts, UserSubmittedAnswer
from django.contrib.auth.decorators import login_required
# Create your views here.

def home(request):
    return render(request,'home.html')

def login(request):
    return render(request,'registration/login.html')

def register(request):
    msg = None
    form = RegisterUser
    if request.method == "POST":
        form = RegisterUser(request.POST)
        if form.is_valid():
            form.save()
            msg = 'Data has been added'
    context = {
        'form':form,
        'msg':msg
    }
    return render(request,'registration/register.html',context)

def all_categories(request):
    catData = QuizCategory.objects.all()

    context ={
        "data":catData
    }
    return render(request,'all-category.html',context)
@login_required
def category_questions(request,cat_id):
    category = QuizCategory.objects.get(id=cat_id)
    question = QuizQuestion.objects.filter(category=category).order_by('id').first()
    lastAttempt = None
    futuretime = None
    hoursLimit = 24
    countAttempt = UserCategoryAttempts.objects.filter(user=request.user,category=category).count()
    if countAttempt == 0:
        UserCategoryAttempts.objects.create(user=request.user,category=category)
    else:
        lastAttempt = UserCategoryAttempts.objects.filter(user=request.user,category=category).order_by(-id).first()
        futuretime = lastAttempt.attempt_time +timedelta(hours=hoursLimit)

        if lastAttempt and lastAttempt.attempt_time<futuretime:
            return redirect('attempty-limet')
            
        else:
            UserCategoryAttempts.objects.create(user=request.user,category=category)
    context = {
        "category":category,
        "question":question,
        'lastAttempt':lastAttempt
    }
    return render(request,'category-questions.html',context)

@login_required
def submit_answer(request,cat_id,quest_id):
    if request.method == "POST":
        category = QuizCategory.objects.get(id=cat_id)
        question = QuizQuestion.objects.filter(category=category,id__gt=quest_id).exclude(id=quest_id).order_by('id').first()
        if 'skip' in request.POST:
            
            if question:
                quest = QuizQuestion.objects.get(id=quest_id)
                user = request.user
                answer='Not submitted'
                UserSubmittedAnswer.objects.create(user=user,question=quest,right_answer=answer)
                context = {
                    "category":category,
                    "question":question
                }
                return render(request,'category-questions.html',context)
        else:
            quest=QuizQuestion.objects.get(id=quest_id)
            user=request.user
            answer=request.POST['answer']
            UserSubmittedAnswer.objects.create(user=user,question=quest,right_answer=answer)

        
        if question:
            context = {
                "category":category,
                "question":question
            }
            return render(request,'category-questions.html',context)
        else:
            result = UserSubmittedAnswer.objects.filter(user=request.user)
            skipped = UserSubmittedAnswer.objects.filter(user=request.user,right_answer='Not Submitted').count()
            attempted = UserSubmittedAnswer.objects.filter(user=request.user).exclude(right_answer='Not Submitted').count()


            rightAns=0
            percentage=0
            for row in result:
                if row.question.right_opt == row.right_answer:
                    rightAns += 1
            percentage = (rightAns*100)/result.count()
            context = {
                "result":result,
                "total_skipped":skipped,
                "attempted":attempted,
                "rightAns":rightAns,
                "percentage":percentage
            }
            return render(request,'result.html',context)
    else:
        return HttpResponse ("Method not allowed !!")


@login_required
def attempt_limet(request):
    return render(request, 'attempty_limet.html')

@login_required
def result(request):
    result = UserSubmittedAnswer.objects.filter(user=request.user)
    skipped = UserSubmittedAnswer.objects.filter(user=request.user,right_answer='Not Submitted').count()
    attempted = UserSubmittedAnswer.objects.filter(user=request.user).exclude(right_answer='Not Submitted').count()


    rightAns=0
    percentage=0
    for row in result:
        if row.question.right_opt == row.right_answer:
            rightAns += 1
    percentage = (rightAns*100)/result.count()

    context = {
                "result":result,
                "total_skipped":skipped,
                "attempted":attempted,
                "rightAns":rightAns,
                "percentage":percentage
            }

    return render(request,'result.html',context)

