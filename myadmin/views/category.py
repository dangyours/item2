from django.shortcuts import render
from django.http import HttpResponse
from myadmin.models import Category,Shop 
import random
from datetime import datetime
from django.core.paginator import Paginator
from django.http import JsonResponse
def index(request,pIndex = 0):
    ob = Category.objects.filter(status__lt = 9)

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
        u.shopname = sob.name
    context = {"categorylist":clist,"mywhere":mywhere,"pIndex":pIndex,"plist":prange}
    return render(request,"myadmin/category/index.html",context)

def add(request):
    ob = Shop.objects.filter(status__lt = 9)
    context = {"shoplist":ob}
    return render(request,"myadmin/category/addcategory.html",context)


def insert(request):
    try:
        ob = Category()
        ob.shop_id = request.POST['shop_id']
        ob.name = request.POST['name']
        ob.status = 1
        ob.create_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.save()
        context = {"info":"添加成功"}
    except Exception as err:
        print(err)
        context = {"info":"添加失败"}
    return render(request,"myadmin/index/info.html",context)
    
def loadCategory(request,sid):
    clist = Category.objects.filter(status__lt=9,shop_id=sid).values("id","name")
    #返回QuerySet对象，使用list强转成对应的菜品分类列表信息
    print(clist)
    return JsonResponse({'data':list(clist)})

def edit(request,cid = 0):
    cob = Category.objects.get(id=cid)
    sob = Shop.objects.filter(status__lt = 9)
    context = {"shoplist":sob,"category":cob}
    return render(request,"myadmin/category/editcategory.html",context)

def update(request,cid = 0):
    cob = Category.objects.get(id=cid)
    cob.name = request.POST['name']
    cob.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cob.save()
    context={"info":"编辑成功"}
    return render(request,"myadmin/index/info.html",context)

def delete(request,cid = 0):
    cob = Category.objects.get(id=cid)
    cob.status = 9
    cob.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cob.save()
    context={"info":"删除成功"}
    return render(request,"myadmin/index/info.html",context)