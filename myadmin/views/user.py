from django.shortcuts import render
from django.http import HttpResponse
from myadmin.models import User 
from django.core.paginator import Paginator
from django.db.models import Q
import random
from datetime import datetime
def index(request,pIndex=1):
    ob = User.objects
    kw = request.GET.get("keyword",None)
    # username = ob.username
    # nickname = ob.nickname
    mywhere = []
    ulist = ob.filter(status__lt=9)
    if kw:
        ulist = ob.filter(Q(username__contains=kw)|Q(nickname__contains=kw))
        mywhere.append("keyword="+kw)
    
    #分页操作
    p = Paginator(ulist,5)
    pagelist = p.page_range
    pagenum = p.num_pages
    if pIndex>pagenum:
        pIndex = pagenum
    if pIndex<1:
        pIndex = 1
    plist = p.page(pIndex)

    context = {"userlist":plist,"pagelist":pagelist,"pIndex":pIndex,"mywhere":mywhere}
    return render(request,'myadmin/index/user.html',context)

def add(request):
    return render(request,'myadmin/index/adduser.html')

def insert(request):
    try:
        ob = User()
        ob.username = request.POST['username']
        ob.nickname = request.POST['nickname']
        import hashlib
        md5 = hashlib.md5()
        n = random.randint(100000, 999999)
        s = request.POST['password']+str(n) 
        md5.update(s.encode('utf-8'))
        ob.password_hash = md5.hexdigest()
        ob.password_salt = n 
        ob.status = 1
        ob.create_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.save()
        context={"info":"添加成功"}
        return render(request,'myadmin/index/info.html',context)
    except Exception as err:
        print(err)
        context = {"info":"添加失败"}
        return render(request,'myadmin/index/info.html',context)


def delete(request,uid=0):
    try:
        ob = User.objects.get(id=uid)
        ob.status = 9
        ob.update_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.save()
        context = {"info":"删除成功"}
    except Exception as err:
        print(err)
        context = {"info":"删除失败"}
    return render(request,"myadmin/index/info.html",context)
    # return JsonResponse(context)

def edit(request,uid=0):
    try:
        ob = User.objects.get(id=uid)
        context = {"user":ob}
        return render(request,"myadmin/index/edituser.html",context)
    except Exception as err:
        print(err)
        context={"info":"不存在该用户"}
        return render(request,"myadmin/index/index.html",context)

def update(request,uid):
    try:
        ob = User.objects.get(id=uid)
        ob.nickname = request.POST['username']
        ob.status = request.POST['status']
        ob.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.save()
        context = {"info":"编辑成功"}
    except Exception as err:
        print(err)
        context = {"info":"编辑失败"}
    return render(request,"myadmin/index/info.html",context)