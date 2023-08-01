# BUAA-2023-Python
北航2023暑期Python程序设计大作业。
# 食用指南：
  本项目基于Django框架搭建，连接本地数据库进行数据处理。所以首先您需要安装django和mysql。然后在pythonWork/settings.py的83行，password那里改成自己本地数据库的密码。在pycharm里安装mysql和django等插件。数据库新建py_hw数据库，安装sklearn依赖。其他的请按照pycharm的提示进行安装项目中有数据生成器，进行首次登录后可以在网址处输入http://127.0.0.1:8000/test/进行数据生成，如果要检验推荐功能的话，输入http://127.0.0.1:8000/test/rightRate进行推荐数据生成。生成后重新登录即可。用户1密码1是管理员，用户5密码5是普通用户。具体可以通过DBeaver查看账号信息。为了便于测试，用户名和密码相同。
