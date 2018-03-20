from django.test import TestCase

# Create your tests here.
# Django建议使用TestCase的一个特殊版本，这个版本由Django提供
# 是标准版TestCase的增强版，添加了一些Django专用的功能


class SmokeTest(TestCase):
    def test_bad_matchs(self):
        self.assertEqual(1 + 1, 3)
