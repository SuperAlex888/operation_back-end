from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from .models import Question, Choice


class IndexView(generic.ListView):
    '''
    在这个类中，定义了三个属性和一个方法： 三个属性中没有定义 model = Question，
        1.template_name：指定要使用的模板文件的名称。在这种情况下，它是"polls/index.html"。
        2.context_object_name：指定要在模板中使用的上下文变量的名称。在这种情况下，它是"latest_question_list"。
        3.get_queryset：定义了一个方法，用于获取要显示的对象列表。在这种情况下，它返回最近发布的五个问题，按发布日期降序排列。

    当用户访问与此视图关联的URL时，Django将调用此视图并执行以下操作：
        1.调用get_queryset方法获取要显示的对象列表。
        2.使用指定的模板文件（“polls/index.html”）渲染页面。
        3.将对象列表传递给模板文件，并使用指定的上下文变量名称（“latest_question_list”）。

    '''
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        """
        这段代码是一个名为 get_queryset 的方法，它返回最近发布的五个问题（不包括将来发布的问题）。
        它通过调用 Question 对象的 filter 方法来筛选出发布日期早于或等于当前时间的问题，然后按照发布日期降序排列，最后取前五个。
        这个方法通常用于 Django 框架中的视图类中，用来控制显示在页面上的数据。
        """
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")[
               :5
               ]


class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"

    def get_queryset(self):
        """
        如果URL未发布则禁止访问.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())

class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"



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