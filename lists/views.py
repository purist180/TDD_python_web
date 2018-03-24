from django.shortcuts import render, redirect
from lists.models import Item

# Create your views here.


def home_page(request):
    if request.method == 'POST':
        Item.objects.create(text=request.POST['item_text'])
        return redirect('/lists/the-only-list-in-the-world/')
        # 在视图函数处理完POST请求后重定向，是习惯性做法

        # objects.create()是创建新Item对象的简化方法，无需再调用.save()方法。
    return render(request, 'home.html')

def view_list(request):
    items = Item.objects.all()
    return render(request, 'list.html',{'items':items})