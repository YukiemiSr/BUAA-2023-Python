from django.shortcuts import render, redirect

from app01.models import UserInfo
from app01.utils.encrypt import encrypt

import datetime
import random


def login(request):
    if request.method == 'GET':
        return render(request, "login.html", {"err": 0})

    # 从前端取出用户名和密码
    user_account = request.POST.get("account")
    pwd = encrypt(request.POST.get("pwd"))
    # 从数据库中取出相关信息
    user_info = UserInfo.objects.filter(account=user_account).first()

    if user_info is None:
        return render(request, "login.html", {"err": 1})
    elif pwd != user_info.password:
        return render(request, "login.html", {"err": 2})
    else:
        # 得到用户id
        user_id = user_info.id
        # 存到session
        # --清除原有session
        request.session.clear()
        request.session["info"] = {'id': user_id, 'account': user_account}

        # 更新用户上次登录时间，登录次数
        nowTime = datetime.datetime.now()
        oldLoginCnt = user_info.loginCnt
        # 如果用户登录时间和上次时间不是同一天则要更新每日运势
        lastLoginTime = user_info.lastLoginTime
        if nowTime.year != lastLoginTime.year or \
                nowTime.month != lastLoginTime.month or nowTime.day != lastLoginTime.day:
            # 注意此处要与models中的fortune_table相匹配
            UserInfo.objects.filter(account=user_account).update(fortune=random.randint(0, 4))
        UserInfo.objects.filter(account=user_account).update(lastLoginTime=nowTime, loginCnt=oldLoginCnt + 1)

        return redirect("/index")
