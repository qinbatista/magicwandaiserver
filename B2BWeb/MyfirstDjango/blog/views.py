from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import View
from django.contrib.auth import authenticate, login
from blog.models import User
from itsdangerous import TimedJSONWebSignatureSerializer as  Serializer
from itsdangerous import SignatureExpired
from django.conf import settings
from django.http import HttpResponse
from django.core.mail import send_mail
import re
# Create your views here.
def jquery_datable(request):
    #进行登陆验证
    if request.session.has_key('islogin'):
        #已经登陆跳转
        return render(request,'../static/pages/tables/jquery-datatable.html')
    else:
        #没有登陆跳转到登陆页面
        return render(request, '../static/pages/examples/sign-in.html')

class registerView(View):
    '''注册'''
    def get(self,request):
        # 显示注册页面
        return render(request, '../static/pages/examples/sign-up.html')
    def post(self,request):
        # 注册处理
        # 数据接收
        username = request.POST.get('namesurname')
        password = request.POST.get('password')
        confirpassword = request.POST.get('confirm')
        email = request.POST.get('email')
        allow = request.POST.get('terms')
        # 数据校验
        if not all([username, password, email]):
            # 数据不完整
            return render(request, '../static/pages/examples/sign-up.html', {'errmsg': '数据不完整'})
        # 邮箱校验
        if not re.match(r'^[a-z0-9][\w.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
            return render(request, '../static/pages/examples/sign-up.html', {'errmsg': '邮箱不合法'})
        # 隐私条约
        if allow != 'on':
            return render(request, '../static/pages/examples/sign-up.html', {'errmsg': '请同意相关协议'})
        if password != confirpassword:
            return render(request, '../static/pages/examples/sign-up.html', {'errmsg': '两次输入的密码不一致'})
        # 业务处理
        try:
            Newuser = User.objects.get(username=username)
        except User.DoesNotExist:
            # 用不户存在可以注册
            Newuser = None
        if Newuser:
            return render(request, '../static/pages/examples/sign-up.html', {'errmsg': '用户名已经被使用！'})
        user = User.objects.create_user(username, email, password)
        #默认没有激活
        user.is_active = 0
        user.save()
        #发送激活邮件,包含激活链接
        #加密用户的身份信息
        serializer=Serializer(settings.SECRET_KEY,600)
        info={'confirm':user.id}
        token=serializer.dumps(info)
        token=token.decode('utf-8')
        #发邮件
        object='重庆魔法棒智能科技有限公司用户注册'
        message=''
        sender=settings.DEFAULT_FROM_EMAIL
        reciver=[email]
        htmlmessage='<h1>%s,欢迎您成为魔法棒的注册会员</h1>请点击下面的链接激活您的账户<br/><a href="http://127.0.0.1:8000/active/%s">http://127.0.0.1:8000/active/%s</a>'%(username,token,token)
        send_mail(object,message,sender,reciver,html_message=htmlmessage)
        # 返回应答
        return redirect(reverse('blog:login'))

class LoginView(View):
    '''显示登陆页面'''
    # get请求
    def get(self,request):
        return render(request, '../static/pages/examples/sign-in.html')  # 显示登陆页面
    def post(self,request):
        '''登陆校验'''
        # 1、获取提交得用户名和密码
        username = request.POST.get("username")
        password = request.POST.get("password")
        print(username)
        print(password)
        # 数据校验
        if not all([username, password]):
            return render(request, '../static/pages/examples/sign-in.html', {'errmsg': '数据不完整'})
        try:
            user = User.objects.get(username=username)
            if user.check_password(password):
                print("验证成功！")
                if user.is_active:
                    login(request, user)
                    response= redirect(reverse('blog:jquery_datale'))
                    response.set_cookie('username', username, max_age=24 * 3600)#记住用户登陆状态
                    request.session['islogin'] = True
                    return response
                else:
                    return render(request, '../static/pages/examples/sign-in.html', {'errmsg': '您的账户还未激活'})
            else:
                return render(request, '../static/pages/examples/sign-in.html', {'errmsg': '密码错误'})
        except:
            return render(request, '../static/pages/examples/sign-in.html', {'errmsg': '用户名不存在'})


        # if user:
        #     return redirect(reverse('blog:jquery_datale'))
        # else:
        #     return render(request, '../static/pages/examples/sign-in.html', {'errmsg': '账户名或者密码错误'})
        # print("测试：")
        # print(user)
            #     login(request, user)
            #
            #     return redirect(reverse('blog:jquery_datale'))
            #
            #     return render(request, '../static/pages/examples/sign-in.html', {'errmsg': '账户未激活'})
            #
            # return render(request, '../static/pages/examples/sign-in.html', {'errmsg': '账户名或者密码错误'})


#激活视图
class ActiveView(View):
    '''用户激活'''
    def get(self,request,token):
        '''进行用户激活'''
        #解密
        serializer = Serializer(settings.SECRET_KEY, 600)
        try:
            info=serializer.loads(token)
            #获取激活用户的iD
            user_id=info['confirm']
            #根基ID获取用户信息
            user=User.objects.get(id=user_id)
            user.is_active=1
            user.save()
            #返回应答跳转到登陆页面
            return redirect(reverse('blog:login'))
        except SignatureExpired as e:
            #激活链接已经过期
            return  HttpResponse("激活链接已经过期！")
