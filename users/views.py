from django.shortcuts import render, redirect
from django.http import Http404
from .forms import RegisterForm
from .models import student,time_record
from django import template
from .models import User
import time
from datetime import datetime



def register(request):
    # 从 get 或者 post 请求中获取 next 参数值
    # get 请求中，next 通过 url 传递，即 /?next=value
    # post 请求中，next 通过表单传递，即 <input type="hidden" name="next" value="{{ next }}"/>
    redirect_to = request.POST.get('next', request.GET.get('next', ''))

    # 只有当请求为 POST 时，才表示用户提交了注册信息
    if request.method == 'POST':
        # request.POST 是一个类字典数据结构，记录了用户提交的注册信息
        # 这里提交的就是用户名（username）、密码（password）、确认密码、邮箱（email）
        # 用这些数据实例化一个用户注册表单
        form = RegisterForm(request.POST)

        # 验证数据的合法性
        if form.is_valid():
            # 如果提交数据合法，调用表单的 save 方法将用户数据保存到数据库
            form.save()

            if redirect_to:
                return redirect(redirect_to)
            else:
                return redirect('/')
    else:
        # 请求不是 POST，表明用户正在访问注册页面，展示一个空的注册表单给用户
        form = RegisterForm()

    # 渲染模板
    # 如果用户正在访问注册页面，则渲染的是一个空的注册表单
    # 如果用户通过表单提交注册信息，但是数据验证不合法，则渲染的是一个带有错误信息的表单
    # 将记录用户注册前页面的 redirect_to 传给模板，以维持 next 参数在整个注册流程中的传递
    return render(request, 'users/register.html', context={'form': form, 'next': redirect_to})


def index(request):
    try:
        post_list = student.objects.all()
        register = template.Library()
        count = {}
        for v in post_list:
            #if v.student_id in User.student_id:
                count[v.student_id] = v.time*v.work_pay

    except student.DoesNotExist:
        raise Http404
    #return render(request, 'archives.html', {'post_list': post_list, 'error': False})
    return render(request, 'index.html',{'post_list': post_list,'count':count, 'error': False})

#没有卵用的方法
def calculate(request):
    try:
        student_info = student.objects.get(student_id=request.user.student_id)
        time1 = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        #time1 = datetime.strptime(time1, '%Y-%m-%d %H:%M:%S')
        time_record.objects.create(time = time1,student=student_info,type = '开始时间')
    except student.DoesNotExist:
        raise Http404
    return render(request,'test.html',{'time1': time1})

def calculate_end(request):
    try:
        time2 = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

        #计算时间差
        record_list = time_record.objects.all()
        student_info = student.objects.get(student_id=request.user.student_id)
        time_list = []
        for record in record_list:
            if record.student_id == request.user.student_id:
                if record.type == '开始时间':
                    time_list.append(record.time)
        time1 = max(time_list)
        #cal = (time2 - time1).days
        time3 = datetime.strptime(time2,'%Y-%m-%d %H:%M:%S')
        cal = time3-time1
        cal2 = (time3-time1).seconds/3600
        if cal2>=0.5 and cal2 <=1:
            cal2 = 1
        elif cal2 >1.5 and cal2 <=2:
            cal2 =2
        else:
            cal2 = 0.5
        sum_time = cal2 + student_info.time
        student_info.time = sum_time
        student_info.save()
        #向时间表中插入用户点击结束的时间
        time_record.objects.create(time = time2,student=student_info,type = '结束时间')

    except student.DoesNotExist:
        raise Http404
    return render(request,'time_end.html',{'time2': time2,'cal':cal})


