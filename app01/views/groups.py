from django.shortcuts import render, redirect

from app01.models import GroupInfo, GroupToQuest, GroupToUser, UserInfo, GroupToList, ListInfo
from app01.utils.pagination import Pagination


def groups(request):
    # 取得用户信息
    user_info = request.session.get("info")
    user_id = user_info.get('id')
    now_user = UserInfo.objects.filter(id=user_id).first()
    now_group_id = request.session.get("nowGroupId")

    user_session = request.session.get("info")
    user_id = user_session.get("id")
    # 获取用户信息数据
    user_infos = UserInfo.objects.filter(id=user_id)
    user_info = user_infos.first()

    # 获取用户所在的群组
    # --注意此处的user_groups是一条GroupToUser记录
    user_groups = GroupToUser.objects.filter(user_id=user_id)

    # 确认用户当前锁定的群组页面
    now_group = None
    if now_group_id:
        now_group = GroupInfo.objects.filter(id=now_group_id).first()

    # 当用户没有选定当前群组时直接返回
    if now_group is None:
        context = {
            "unselected": 1,
            "user_groups": user_groups,
            "privilege": now_user.privilege,
            "user_info": user_info,
        }
        return render(request, "groups.html", context)

    # 获取同组分享的题单
    share_lid = GroupToList.objects.filter(group_id=now_group_id).values_list("list_id", flat=True).distinct()
    share_lid = list(share_lid)
    all_lists = ListInfo.objects.filter(id__in=share_lid).order_by("name")
    # 分页相关
    page_object = Pagination(request, all_lists, 10)

    # 解析公告
    notices = []
    user_list = []
    is_adm = 1
    if now_group:
        context = str(now_group.notice)
        notices = context.split('\n')
        user_list = GroupToUser.objects.filter(group_id=now_group.id)
        if now_group.adm_id == user_id:
            is_adm = 2
            user_session = request.session.get("info")
            user_id = user_session.get("id")
            # 获取用户信息数据
            user_infos = UserInfo.objects.filter(id=user_id)
            user_info = user_infos.first()
    # 传入内容
    context = {
        "unselected": 0 if len(share_lid) > 0 else 1,
        "llist": page_object.page_queryset,
        "page_string": page_object.html(),
        "user_groups": user_groups,
        "now_group": now_group,
        "notices": notices,
        "user_list": user_list,
        "is_adm": is_adm,
        "privilege": now_user.privilege,
        "user_info": user_info
    }
    return render(request, "groups.html", context)


def toGroup(request, group_id):
    request.session["nowGroupId"] = group_id
    return redirect("/groups/")


def group_Manage(request):
    # 获取用户信息
    user_id = request.session.get("info").get("id")
    now_group_id = request.session.get("nowGroupId")

    # 到数据库中取值
    now_group = GroupInfo.objects.filter(id=now_group_id).first()

    if now_group is None:
        return render(request, "groupManage.html", {"err": 1})
    elif now_group.adm_id == user_id:
        userList = GroupToUser.objects.filter(group_id=now_group_id)
        page_object = Pagination(request, userList, pagesize=15)
        context = {
            "userList": page_object.page_queryset,
            "page_string": page_object.html(),
            "now_group": now_group,
            "err": 0
        }
        return render(request, "groupManage.html", context)
    else:
        return render(request, "groupManage.html", {"err": 2})


def group_MemberDelete(request, group_id, user_id):
    # 到数据库中寻找组
    group = GroupInfo.objects.filter(id=group_id)
    if user_id == group.first().adm_id:
        # 若是管理员则删除群
        group.delete()
        return redirect("/groups/")
    else:
        # 若不是管理员则删除用户
        GroupToUser.objects.filter(user_id=user_id, group_id=group_id).delete()
        return redirect("/groups/manage/")


# 管理员删除群
def deleteAll(request, group_id):
    GroupInfo.objects.filter(id=group_id).delete()
    return redirect("/groups/")


def addToGroup(request):
    # 获取用户信息
    user_id = request.session.get("info").get("id")
    # 进行加入群组操作
    add_group = str(request.POST.get("name"))
    # 解析加入群组信息
    groupLinks = GroupInfo.objects.filter(name=add_group)
    if groupLinks.count() == 0:
        return render(request, "groups.html", {"err": 1})
    else:
        group = groupLinks.first()
        GroupToUser.objects.create(user_id=user_id, group=group)
    return render(request, "groups.html", {"err": -1})


def addGroup(request):
    # 获取用户信息
    user_id = request.session.get("info").get("id")
    # 进行创建群组操作
    groupName = str(request.POST.get("name"))
    # 判断当前名字的群组是否存在
    if GroupInfo.objects.filter(name=groupName).count() > 0:
        return render(request, "groups.html", {"err": 2})
    else:
        GroupInfo.objects.create(name=groupName, adm_id=user_id)
        groupLinks = GroupInfo.objects.filter(name=groupName)
        group = groupLinks.first()
        GroupToUser.objects.create(user_id=user_id, group=group)
        return render(request, "groups.html", {"err": -2})
