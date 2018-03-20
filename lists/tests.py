from django.core.urlresolvers import resolve
from django.test import TestCase

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