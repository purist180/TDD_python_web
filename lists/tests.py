from django.template.loader import render_to_string
from django.core.urlresolvers import resolve
from django.test import TestCase
from django.http import HttpRequest
from lists.models import Item

# Create your tests here.
# Django建议使用TestCase的一个特殊版本，这个版本由Django提供
# 是标准版TestCase的增强版，添加了一些Django专用的功能

from lists.views import home_page
# home_page这个函数是接下来要定义的视图函数，其作用是返回所需的HTML。
# 从import语句可以看出，这个函数保存在list/views.py中。


class HomePageTest(TestCase):

    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        # resolve是Django内部使用的函数，用于解析URL，并将其映射到相应的视图函数上。
        self.assertEqual(found.func, home_page)
        # 检查解析网站跟路径“/”时，是否能找到名为home_page的函数。

    def test_home_page_returns_correct_html(self):
        # request = HttpRequest()
        # # 创建一个HttpRequest对象，
        # # 用户在浏览器中请求网页时， Django看到的就是HttpRequest对象。
        # response = home_page(request)
        # # 把这个HttpRequest对象传给home_page视图，得到响应response。
        # # 接下来断定相应的.content属性（即发给用户的HTML）中是否有特定内容
        # self.assertTrue(response.content.startswith(b'<html>'))
        # self.assertIn(b'<title>To-Do lists</title>', response.content)
        # self.assertTrue(response.content.endswith(b'</html>'))
        request = HttpRequest()
        response = home_page(request)
        expected_html = render_to_string('home.html')
        self.assertEqual(response.content.decode(), expected_html)
        # 使用.decode()把response.content中的字节转换成Python中的Unicode字符串，这样就可以
        # 对比字符串，不用像之前一样对比字节Bytes。

    def test_home_page_can_save_a_POST_request(self):
        request = HttpRequest()
        request.method = 'POST'
        request.POST['item_text'] = 'A new list item'
        # 用到了HttpRequest的几个特殊性：.method和.POST
        # 阅读Django关于请求和相应的文档。

        response = home_page(request)

        self.assertEqual(Item.objects.count(), 1)
        # 检查是否吧一个新的Item对象存入数据库。objects.count()是objects.all().count()的简化形式。
        new_item = Item.objects.first()  # 等价于Item.objects.all()[0]
        self.assertEqual(new_item.text, 'A new list item')

    def test_home_page_redirects_after_POST(self):
        request = HttpRequest()
        request.method = 'POST'
        request.POST['item_text'] = 'A new list item'

        response = home_page(request)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/')

    def test_home_page_only_saves_items_when_necessary(self):
        request = HttpRequest()
        home_page(request)
        self.assertEqual(Item.objects.count(), 0)

    def test_home_page_can_display_all_list_items(self):
        Item.objects.create(text='itemey 1')
        Item.objects.create(text='itemey 2')

        request = HttpRequest()
        response = home_page(request)

        self.assertIn('itemey 1', response.content.decode())
        self.assertIn('itemey 2', response.content.decode())


class ItemModelTest(TestCase):

    def test_saving_and_retrieving_items(self):
        first_item = Item()
        first_item.text = 'The first (ever) list item'
        first_item.save()

        second_item = Item()
        second_item.text = 'Item the second'
        second_item.save()
        # 数据库中创建新纪录的过程：先创建一个对象，再为一些属性赋值
        # 然后调用.save()。

        saved_items = Item.objects.all()
        # Django提供了一个查询数据库的API，即类属性。objects
        # 使用最简单的方法.all()，取回这个表中的全部记录。
        # 得到的结果是一个类似list的对象，QuerySet。
        # 这个对象可以提取单个对象，然后还可以再调用其他函数，例如.count()。
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, 'The first (ever) list item')
        self.assertEqual(second_saved_item.text, 'Item the second')
