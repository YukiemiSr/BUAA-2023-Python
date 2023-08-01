"""
URL configuration for pythonWork project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from app01.views import index
from app01.views import register
from app01.views import user
from app01.views import head
from app01.views import login
from app01.views import question_bank, question_list
from app01.views import question
from app01.views import groups
from app01.views import about
from app01.views import record
from app01.views import upload
from app01.views import test

urlpatterns = [
    # 登录
    path('login/', login.login),
    # 注册
    path('register/', register.register),
    # 主页
    path('index/', index.index),
    path('index/chartInfo/', index.index_chartInfo),
    # 用户
    path('user/', user.user),
    path('user/list/', user.user_list),
    path('user/delete/', user.user_delete),
    path('user_edit/', user.user_edit),
    path('user/chartInfo/', user.user_ChartInfo),
    # 问题
    path('bank/', question_bank.question_bank),
    path('question/', question.question),
    path('list/', question_list.question_list),
    # 群组
    path('groups/', groups.groups),
    path('groups/<int:group_id>/toGroup', groups.toGroup),
    path('groups/manage/', groups.group_Manage),
    path('groups/<int:group_id>/<int:user_id>/delete', groups.group_MemberDelete),
    path('groups/<int:group_id>/deleteAll', groups.deleteAll),
    path('groups/add',groups.addToGroup),
    path('groups/create',groups.addGroup),
    # 关于
    path('about/', about.about),
    # 记录
    path('record/', record.record),
    path('record/<int:record_id>/delete', record.record_delete),
    path('record/<int:user_id>/deleteAll', record.record_deleteAll),
    # 上传
    path('upload/', upload.upload),
    # 放置测试代码，用于生成数据
    path('test/', test.test),
    path('test/time', test.timeChart),
    path('test/rightRate', test.rightRate),
    # 放置导航栏，测试用
    path('head/', head.head),
]
