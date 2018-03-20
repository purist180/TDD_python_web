# Django在urls.py文件中定义如何把URL映射到视图函数上。
# 这个文件应用于整个网站


from django.conf.urls import include, url
from django.contrib import admin


urlpatterns = [
    # Examples:
    url(r'^$', 'lists.views.home_page', name='home'),
    url(r'^123/','lists.views.test_view', name='test_view')
    # url(r'^blog/', include('blog.urls')),

    # url(r'^admin/', include(admin.site.urls)),


]
