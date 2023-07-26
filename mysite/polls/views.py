from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from .models import Question, Choice


def index(request):
    latest_question_list = Question.objects.order_by("-pub_date")[:5]
    context = {"latest_question_list": latest_question_list}
    return render(request, "polls/index.html", context)


def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/detail.html", {"question": question})


def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/results.html", {"question": question})


def vote(request, question_id):
    # 1.使用get_object_or_404再Question数据库中查找是否存在主键为：question_id值得字段，案例中是1
    #       如果不存在则直接返回404
    #       1.1如果存在则将models中question内得值赋予给question
    question = get_object_or_404(Question, pk=question_id)
    print(fr'{question}')
    try:
        '''
        choice_set 是一个由 Django 自动生成的关联管理器（related manager），它用于管理 Question 和 Choice 之间的一对多关系。在这个例子中，
        每个 Question 对象都有一个 choice_set 属性，它可以用来获取与这个问题相关联的所有选项。

        例如，如果你有一个 Question 对象 q，你可以使用 q.choice_set.all() 来获取与这个问题相关联的所有选项。你也可以使用其他的查询方法，
        如 q.choice_set.filter(...) 或 q.choice_set.get(...) 来获取特定的选项。

        choice_set 的名称是根据模型类的名称自动生成的。在这个例子中，因为关联的模型类是 Choice，所以关联管理器的名称是 choice_set。
        如果你想使用不同的名称，你可以在模型定义中使用 related_name 选项来指定。
        '''
        # 2. 通过"pk=request.POST["choice"]"查找表单中choice得参数，并且通过参数
        #    question.choice_set.get(1) 获取choice表中主键ID为1得列
        selected_choice = question.choice_set.get(pk=request.POST["choice"])

        #print(f"{selected_choice}hhh")
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(
            request,
            "polls/detail.html",
            {
                "question": question,
                "error_message": "You didn't select a choice.",
            },
        )
    else:
        # 3. selected_choice中得votes += 1
        selected_choice.votes += 1
        selected_choice.save()

        '''
        4.函数：reverse("polls:results", args=(question.id,)) 得出：/polls/1/results/ 
               4.1"polls:results"：是视图得名称，指定了要生成得url视图。 此处会限跳转到urls.py中引用name="results"得url
               4.2 results又指向视图 "views.results",result函数接收一个入参 def results(request, question_id):
               4.3 最后调用views.results返回 return HttpResponse(response % question_id) 
               4.4 最后拼接出  http://127.0.0.1:8000/polls/1/results/
        '''

        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))