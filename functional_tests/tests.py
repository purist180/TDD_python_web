from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from django.test import LiveServerTestCase

# 关于功能测试
# 使用Selenium实现的测试可以驱动真正的网页浏览器，让我们能从用户的角度查看应用是如何运作的。
# 这类测试称为“功能测试”。

# 功能测试在某种程度上可以作为应用的说明书。功能测试的作用是跟踪“用户故事”（User Story）,
# 模拟用户使用某个功能的过程，以及如何响应用户的操作。

# 功能测试有时也称之为验收测试（Acceptance Test）或端到端测试（End-to-End Test)
# 这类测试的最重要作用是从外部观察真个应用是如何运作的。

# 另一种属于是黑箱测试（Black Box Test)，因为这种测试对所要测试的系统内部一无所知。


# 编写新功能测试时，可以先写注释，勾勒出用户故事的重点。

# “最简可用的应用”，即我们能开发出来的最简单的而且可以使用的应用。
# 尽早试水


# browser = webdriver.Chrome()

# # 去看了应用的首页
# browser.get('http://localhost:8000')

#       # 启动一个Selenium webdriver，打开一个真正的Chrome浏览器窗口；
#       # 在这个浏览器窗口中打开期望的本地电脑伺服的网页；
#       # 检查（做一个 测试断言）这个网页的标题中是否包含单词'Django'

# # 注意到网页的标题和头部都包含“To-Do"这个词

# assert 'To-Do' in browser.title, 'Browser title was ' + browser.title


# browser.quit()


class NewVisitorTest(LiveServerTestCase):
    # 测试组织成类的形式，继承自unittest.Testcase

    def setUp(self):
        self.browser = webdriver.Chrome()
        # self.browser.implicitly_wait(3)
        # 隐式等待

    def tearDown(self):
        self.browser.quit()

    '''
    setUp和tearDown是特殊的方法，分别在测试方法之前和之后运行，
    这里使用这两个方法打开和关闭浏览器。
    这两个方法有点类似try/except语句，就算测试中出错了，也会运行tearDown方法
    测试结束后，浏览器窗口就不会一直停留在桌面上了。
    '''

    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])

    def test_can_start_a_list_and_retrieve_it_later(self):
        # 测试的主要代码写在名为test_can_start_a_list_and_retrieve_it_later的方法中。
        # 名字以test_开头的方法都是测试方法，由测试运行程序运行。
        # 类中可以定义多个测试方法。
        # print(type(self))

        # 打开应用的首页
        self.browser.get(self.live_server_url)
        # 访问网站是，不用硬编码的本地地址（localhost:8000),使用LiveServerTestCase提供的live_server_url属性
        # print(self.live_server_url)

        # 她注意到网页的标题和头部都包含“To-Do"这个词
        self.assertIn('To-Do', self.browser.title)
        # 使用self.assertIn代替assert编写断言。
        # unittest提供了很多这种用于编写断言测试的辅助函数
        # 如assertEqual, assertTrue, assertFalse等，具体可以看下unittest的文档

        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        # 应用邀请他输入一个待办事项
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a to-do item'
        )

        # 在文本框中输入'Buy peacock feathers',
        inputbox.send_keys('Buy peacock feathers')

        # 按回车键后被带到了一个新URL
        # 在新页面的待办事项清单中显示了'1: Buy peacocks feathers'
        inputbox.send_keys(Keys.ENTER)
        edith_list_url = self.browser.current_url
        self.assertRegex(edith_list_url, '/lists/.+')
        self.check_for_row_in_list_table('1: Buy peacock feathers')
        # assertRegex是unittest中的辅助函数，检查字符串是否和正则表达式匹配。


        # 页面有显示了一个文本框，可以输入其他的待办事项
        # 他输入了'Use peacock feathers to make a fly'
        # 把拉巴拉
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Use peacock feathers to make a fly')
        inputbox.send_keys(Keys.ENTER)

        # 页面更新，清单中显示这两个待办事项
        self.check_for_row_in_list_table('1: Buy peacock feathers')
        self.check_for_row_in_list_table('2: Use peacock feathers to make a fly')

        # 现在有个叫弗朗西斯的家伙访问了网站

        ## 使用一个新的浏览器会话
        ## 确保伊迪丝的信息不会从cookie中泄露出来
        self.browser.quit()
        self.browser = webdriver.Chrome()

        # 弗朗西斯访问首页
        # 页面中看不到伊迪丝的清单
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertNotIn('make a fly', page_text)

        # 弗朗西斯输入了一个待办事项，新建一个清单
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy milk')
        inputbox.send_keys(Keys.ENTER)

        # 弗朗西斯获得了他唯一的URL
        francis_list_url = self.browser.current_url
        self.assertRegex(francis_list_url, '/lists/.+')
        self.assertNotEqual(francis_list_url, edith_list_url)

        # 这个页面还是没有伊迪丝的清单
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertNotIn('make a fly', page_text)

        # 暂时完事了









