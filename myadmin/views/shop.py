from django.shortcuts import render
from django.http import HttpResponse
from myadmin.models import Shop
from datetime import datetime
from django.shortcuts import redirect
from django.urls import reverse
import time 
def index(request,pIndex=1):
    ob = Shop.objects
    slist = ob.filter(status__lt=9)
    
    context = {"shoplist":slist}
    return render(request,'myadmin/shop/index.html',context)

def add(request):
    return render(request,"myadmin/shop/addshop.html")

def insert(request):
    try:
        myfile = request.FILES.get("cover_pic",None)
        if None == myfile:
            return HttpResponse("未上传zhaop")
        else:
            cover_pic = str(time.time()) + "." + myfile.name.split('.').pop()
            destination = open("./static/uploads/shop/"+cover_pic,"wb+")
            for chunk in myfile.chunks():      # 分块写入文件  
                destination.write(chunk)  
            destination.close()

        myfile = request.FILES.get("banner_pic",None)
        if None == myfile:
            return HttpResponse("未上传zhaop")
        else:
            banner_pic = str(time.time()) + "." + myfile.name.split('.').pop()
            destination = open("./static/uploads/shop/"+banner_pic,"wb+")
            for chunk in myfile.chunks():
                destination.write(chunk)
            destination.close

        ob = Shop()
        ob.name = request.POST['name']
        ob.cover_pic = cover_pic
        ob.banner_pic = banner_pic
        ob.address = request.POST['address']
        ob.phone = request.POST['phone']
        ob.status = 1
        ob.create_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.save()
        context = {"info" : "添加成功"}
    except Exception as err:
        print(err)
        context = {"info":"添加失败"}
    return render(request,"myadmin/index/info.html",context)


def edit(request,sid=0):
    ob = Shop.objects.get(id = sid)
    context = {"shop":ob}
    return render(request,"myadmin/shop/shopedit.html",context)

def update(request,sid=0):
    ob = Shop.objects.get(id = sid)
    ob.name = request.POST['name']
    ob.phone = request.POST['phone']
    ob.address = request.POST['address']
    ob.status = request.POST['status']
    myfile = request.FILES.get("cover_pic",None)
    myfile = request.FILES.get("cover_pic",None)
    if None != myfile:
        cover_pic = str(time.time()) + "." + myfile.name.split('.').pop()
        destination = open("./static/uploads/shop/"+cover_pic,"wb+")
        for chunk in myfile.chunks():      # 分块写入文件  
            destination.write(chunk)  
        ob.cover_pic = cover_pic
        destination.close()

    myfile = request.FILES.get("banner_pic",None)
    if None != myfile:
        banner_pic = str(time.time()) + "." + myfile.name.split('.').pop()
        destination = open("./static/uploads/shop/"+banner_pic,"wb+")
        for chunk in myfile.chunks():
            destination.write(chunk)
        ob.banner_pic = banner_pic
        destination.close
    ob.save()
    context = {"info":"编辑成功"}
    return render(request,'myadmin/index/info.html',context)
 

def delete(request,sid=0):
    ob = Shop.objects.get(id = sid)
    ob.status = 9
    ob.save()
    return redirect(reverse("myadmin_shop_index",args = "1"))