from django.shortcuts import render, redirect

from app01.models import UserRecord, QuestInfo, UserInfo
from app01.utils.pagination import Pagination


def record(request):
    user_session = request.session.get("info")
    user_id = user_session.get("id")
    # 获取用户信息数据
    user_infos = UserInfo.objects.filter(id=user_id)
    user_info1 = user_infos.first()
    # 得到缓存信息
    user_info = request.session.get("info")
    # 得到用户id
    user_id = user_info.get("id")
    # 从用户-记录链接表中查找问题列表
    record_list = UserRecord.objects.filter(user_id=user_id).order_by("-time")
    # 分页相关
    page_object = Pagination(request, record_list, pagesize=15)
    # 传入内容
    context = {
        "record_list": page_object.page_queryset,
        "user_id": user_id,
        "page_string": page_object.html(),
        "user_info":user_info1
    }
    return render(request, "record.html", context)


def record_delete(request, record_id):
    UserRecord.objects.filter(id=record_id).delete()
    return redirect("/record/")


def record_deleteAll(request, user_id):
    UserRecord.objects.filter(user_id=user_id).delete()
    return redirect("/record/")
