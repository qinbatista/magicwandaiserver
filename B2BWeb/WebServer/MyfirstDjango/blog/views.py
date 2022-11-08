from django.http import HttpResponse
from django.shortcuts import render, redirect
from blog.models import UserInfo

# Create your views here.
def index(request):
    # # 1,加载模板文件
    # temp = loader.get_template('test1/index.html')
    # # 2,定义模板上下文：给模板传递数据
    # context = RequestContext(request, {})
    # # 3,渲染模板产生标准的html文件内容
    # reshtml=temp.render()
    # # 4,返回给浏览器
    # return HttpResponse(reshtml)
    return render(request,'index.html')
def login(request):
    '''显示登陆页面'''
    return render(request,'../static/pages/examples/sign-in.html')#显示登陆页面
def login_check(request):
    '''登陆校验'''
    #1、获取提交得用户名和密码
    username=request.POST.get("username")
    password=request.POST.get("password")
    print(username+":"+password)
    user = UserInfo.objects.get(UserName=username)
    if user.PassWord==password:
        return redirect('/index')
    else:
        return redirect('/login')