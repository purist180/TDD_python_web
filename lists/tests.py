from django.core.urlresolvers import resolve
from django.test import TestCase
from django.http import HttpRequest

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
        request = HttpRequest()
        # 创建一个HttpRequest对象，
        # 用户在浏览器中请求网页时， Django看到的就是HttpRequest对象。
        response = home_page(request)
        # 把这个HttpRequest对象传给home_page视图，得到响应response。
        # 接下来断定相应的.content属性（即发给用户的HTML）中是否有特定内容
        self.assertTrue(response.content.startswith(b'<html>'))
        self.assertIn(b'<title>To-Do lists</title>', response.content)
        self.assertTrue(response.content.endswith(b'</html>'))
