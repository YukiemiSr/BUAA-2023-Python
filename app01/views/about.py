from django.shortcuts import render

from app01.models import *
from app01.utils.encrypt import encrypt


def about(request):
    user_session = request.session.get("info")
    user_id = user_session.get("id")
    # 获取用户信息数据
    user_infos = UserInfo.objects.filter(id=user_id)
    user_info = user_infos.first()
    return render(request, "about.html",{"user_info":user_info})
