from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^index/$', views.index, name='index'),
    url(r'^article/page/(?P<pk>\d+)/$', views.article, name='article'),
    # url(r'^contact/$', views.contact, name='contact'),
    url(r'^about/$', views.about, name='about'),
    url(r'^captcha/', views.captcha, name='captcha'),
    url(r'^timeline/$', views.timeline, name='timeline'),
    url(r'^search/', views.search, name='search'),
    url(r'^login/', views.login, name='login'),
    url(r'^comment/', views.comment, name='comment'),
    url(r'^type/(?P<pk>[\S]*)$', views.labelcloud, name="labeltype"),
    # url(r'^staymessage/', views.staymessage, name='staymessage'),
]
# handler404 = views.page_not_found