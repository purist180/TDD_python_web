from selenium import webdriver

browser = webdriver.Chrome()
browser.get('http://localhost:8000')
# 启动一个Selenium webdriver，打开一个真正的Chrome浏览器窗口；
# 在这个浏览器窗口中打开期望的本地电脑伺服的网页；
# 检查（做一个 测试断言）这个网页的标题中是否包含单词'Django'
assert 'Django' in browser.title

