"""学生选课管理系统 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from login import views


urlpatterns = [

    #测试用链接
    url(r'^error',views.error,name='error'),

    #登录链接
    url(r'^$', views.loginPage, name='login'),
    url(r'^log/', views.loginPage),
    url(r'^teacherlogin/',views.teacherlogin,name='teacherlogin'),
    url(r'^studentlogin/',views.studentlogin,name='studentlogin'),
    #注册链接
    url(r'^tearegister/',views.tearegister,name='tearegister'),
    url(r'^sturegister/',views.sturegister,name='sturegister'),

    #教师操作处理链接
    url(r'^teacherPage/(?P<operation>[\w-]+)/',views.teaOption,name='teacherPage'),
    url(r'^teacherPage/',views.teaOption,name='teacherPage'),
    url(r'^view/(?P<operation>[\w]+)/(?P<arg>[\w]+)/',views.teacherPage_view,name='view'),
    url(r'^grading/',views.grading,name='grading'),

    #学生操作处理链接
    url(r'^studentPage/(?P<operation>[\w-]+)/',views.stuOption,name='studentPage'),
    url(r'^select_course/(?P<operation>[\w]+)/(?P<arg>[\w]+)/',views.select_course,name='select_course'),
    url(r'^stu_updatePasswd/(?P<operation>[\w]+)/(?P<arg>[\w]+)/',views.stu_updatePasswd,name='stu_updatePasswd'),
    url(r'^delete_course/(?P<operation>[\w]+)/(?P<arg>[\w]+)/',views.delete_course,name='delete_course'),

    #查询课程链接
    url(r'^course_finding/',views.course_finding,name='course_finding'),
]
