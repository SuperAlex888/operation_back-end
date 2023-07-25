from django.http import HttpResponse, Http404
from .models import Question
from django.template import loader
from django.shortcuts import render, get_object_or_404


def index(request):
    # return HttpResponse("Hello, world. You're at the polls index.")


    # 如何在django中使用自定义网页
    # 1.在数据库中使用order_by方法调用5个Question对象，按发布日期降序排列，存储到"latest_question_list"
    latest_question_list = Question.objects.order_by("-pub_date")[:5]

    # 使用"loader.get_template"加载模板"polls/index.html"
    template = loader.get_template("polls/index.html")
    # 2.创建一个包含 latest_question_list 变量的上下文字典。此上下文字典用于渲染模板，然后作为 HTTP 响应返回。
    context = {
        "latest_question_list": latest_question_list,
    }
    # 3.return出去 http响应，返回一个template.render(context, request)
    '''
     详细解释： template.render()方法，主要是将上下文字典，渲染进网页模板中
                    渲染完成后返回一个html页面
              上下文字典：包含模板变量所需要的所有值
              request：一个请求的对象，它包含了用户信息，请求内容和请求方法等
              
    '''
    #return HttpResponse(template.render(context, request))


    # 4.render简写上面的httpResponse的函数,快捷函数,可以简略掉template定义和
    return render(request, "polls/index.html", context)


# def index(request):
#     latest_question_list = Question.objects.order_by("-pub_date")[:5]
#     output = ", ".join([q.question_text for q in latest_question_list])
#     return HttpResponse(output)

def detail(request, question_id):
    # 正常写法：尝试如果访问不正常则返回http404
    '''
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist -V-")
    return render(request, "polls/detail.html", {"question": question})
    '''

    # 快捷写法：
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/detail.html", {"question": question})


def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)


def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)