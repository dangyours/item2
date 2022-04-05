from django.shortcuts import render
from django.http import HttpResponse
from myadmin.models import User 
# Create your views here.

def index(request):
    return render(request,'myadmin/index/index.html')

def user_index(request,uid=1):
    return HttpResponse("etes")

def login(request):
    return render(request,'myadmin/index/login.html')

def dologin(request):
    try:
        user = User.objects.get(username=request.POST['username'])
        import hashlib
        md5 = hashlib.md5()
        n = user.password_salt
        s = request.POST['pass']+str(n)
        md5.update(s.encode('utf-8'))
        if user.password_hash == md5.hexdigest():
            request.session['adminuser'] = user.toDict()
            context = {"info":"登陆成功"}
            return render(request,"myadmin/index/index.html")
        context = {"info":"登录失败"}
    except Exception as err:
        print(err)
        context = {"info":"登录失败"}
    return render(request,"myadmin/index/login.html",context)

def logout(request):
    del request.session['adminuser']
    return render(request,"myadmin/index/login.html")