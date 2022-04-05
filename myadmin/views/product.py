from django.shortcuts import render
from django.http import HttpResponse
from myadmin.models import Category,Shop,Product
import random
from datetime import datetime
from django.core.paginator import Paginator
import time
def index(request,pIndex = 0):
    ob = Product.objects.filter(status__lt = 9)

    mywhere = []
    #实现分页
    p = Paginator(ob,10)
    if pIndex < 1:
        pIndex = 1
    if pIndex > p.num_pages:
        pIndex = p.num_pages
    prange = p.page_range
    clist = p.page(pIndex)

    for u in clist:
        sob = Shop.objects.get(id=u.shop_id)
        cob = Category.objects.get(id=u.category_id)
        u.categoryname = cob.name
        u.shopname = sob.name
    
    context = {"productlist":clist,"mywhere":mywhere,"pIndex":pIndex,"plist":prange}
    return render(request,"myadmin/product/index.html",context)

def add(request):
    ob = Shop.objects.filter(status__lt = 9)
    context = {"shoplist":ob}
    return render(request,"myadmin/product/addproduct.html",context)


def insert(request):
    try:
        #图片的上传处理
        myfile = request.FILES.get("cover_pic",None)
        if not myfile:
            return HttpResponse("没有封面上传文件信息")
        cover_pic = str(time.time())+"."+myfile.name.split('.').pop()
        destination = open("./static/uploads/product/"+cover_pic,"wb+")
        for chunk in myfile.chunks():      # 分块写入文件  
            destination.write(chunk)  
        destination.close()

        #实例化model，封装信息，并执行添加
        ob = Product()
        ob.shop_id = request.POST['shop_id']
        ob.category_id = request.POST['category_id']
        ob.name = request.POST['name']
        ob.price = request.POST['price']
        ob.cover_pic = cover_pic
        ob.status = 1
        ob.create_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.save()
        context={"info":"添加成功！"}
    except Exception as err:
        print(err)
        context={"info":"添加失败"}
    return render(request,"myadmin/index/info.html",context)
    

def edit(request,pid = 0):
    try:
        ob = Product.objects.get(id=pid)
        slist = Shop.objects.values("id","name")
        context={"product":ob,"shoplist":slist}
        return render(request,"myadmin/product/edit.html",context)
    except Exception as err:
        context={"info":"没有找到要修改的信息！"}
        return render(request,"myadmin/info.html",context)

def update(request,pid = 0):
    try:
        #获取原图片名
        oldpicname = request.POST['oldpicname']
        #判断是否有文件上传
        myfile = request.FILES.get("cover_pic",None)
        if not myfile:
            cover_pic = oldpicname
        else:
          #图片的上传处理
          cover_pic = str(time.time())+"."+myfile.name.split('.').pop()
          destination = open("./static/uploads/product/"+cover_pic,"wb+")
          for chunk in myfile.chunks():      # 分块写入文件  
              destination.write(chunk)  
          destination.close()

        ob = Product.objects.get(id=pid)
        ob.shop_id = request.POST['shop_id']
        ob.category_id = request.POST['category_id']
        ob.name = request.POST['name']
        ob.price = request.POST['price']
        ob.cover_pic = cover_pic
        ob.status = request.POST['status']
        ob.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.save()
        context={"info":"修改成功！"}
        # 判断删除老图片
        if myfile:
            os.remove("./static/uploads/product/"+oldpicname)
    except Exception as err:
        print(err)
        context={"info":"修改失败"}
        #判断删除刚刚上传的图片
        if myfile:
            os.remove("./static/uploads/product/"+cover_pic)

    return render(request,"myadmin/info.html",context)

def delete(request,pid = 0):
    try:
        ob = Product.objects.get(id=pid)
        ob.status = 9
        ob.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.save()
        context={"info":"删除成功！"}
    except Exception as err:
        print(err)
        context={"info":"删除失败"}

    return JsonResponse(context)