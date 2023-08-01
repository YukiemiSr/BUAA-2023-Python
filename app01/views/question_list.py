from django.db.models import Q
from django.shortcuts import render
from app01.models import QuestInfo, QuestBank, ChapterInfo, GroupToUser, GroupToQuest, ListInfo, GroupToList, \
    ListToQuest, UserInfo
from app01.utils.pagination import Pagination
import json


def question_list(request):
    list_id = request.GET.get("lid")
    user_id = request.session.get("info").get("id")
    now_list = ListInfo.objects.filter(id=list_id).first()
    user_session = request.session.get("info")
    user_id = user_session.get("id")
    # 获取用户信息数据
    user_infos = UserInfo.objects.filter(id=user_id)
    user_info = user_infos.first()
    # 编辑题单信息
    could_edit = False
    if request.method == "POST":
        new_name = request.POST.get("change_name")
        new_intro = request.POST.get("change_text")
        new_auth = request.POST.get("change_authority")
        old_auth = now_list.authority
        group_id = request.POST.get("group_id")
        ListInfo.objects.filter(id=list_id) \
            .update(name=new_name, introduction=new_intro, authority=new_auth)
        print(new_auth)
        if old_auth == 1:
            GroupToList.objects.filter(list_id=list_id).delete()
            print("删除成功")
        if new_auth == "1":
            GroupToList.objects.get_or_create(group_id=group_id, list_id=list_id)

    # 获取同组分享的题单
    user_groups = GroupToUser.objects.filter(user_id=user_id).values_list("group_id", flat=True)
    share_lid = GroupToList.objects.filter(group_id__in=user_groups).values_list("list_id", flat=True).distinct()
    share_lid = list(share_lid)
    # 获取自己的和分享给所有人的题单
    user_lid = ListInfo.objects.filter(Q(user_id=user_id) | Q(authority=2)).values_list("id", flat=True)
    user_lid = list(user_lid)
    # 用户可见的所有题单
    all_lists = list(set(share_lid + user_lid))
    all_lists = ListInfo.objects.filter(id__in=all_lists).order_by("name")

    # 显示当前list的题目
    question_rest = QuestInfo.objects.filter(id__in=[])
    if list_id:
        if ListInfo.objects.filter(id=list_id):
            now_list = ListInfo.objects.get(id=list_id)
            if now_list.user.id == user_id:
                could_edit = True
            qid_list = ListToQuest.objects.filter(list_id=list_id).values_list("quest_id", flat=True).distinct()
            question_rest = QuestInfo.objects.filter(id__in=qid_list).order_by("id")
        else:
            return render(request, "qlist.html", {"err_name": 1})

    # 分页相关
    page_object1 = Pagination(request, question_rest, 10)
    page_object2 = Pagination(request, all_lists, 10)

    context = {
        "err_name": 0 if list_id else -1,
        "could_edit": could_edit,
        "now_list": now_list,
        "user_groups": GroupToUser.objects.filter(user_id=user_id),
        "qlist": page_object1.page_queryset,
        "llist": page_object2.page_queryset,
        "all_lists": ListInfo.objects.filter(id__in=all_lists).order_by("name"),
        "page_string1": page_object1.html(),
        "page_string2": page_object2.html(),
        "user_info": user_info
    }

    return render(request, "qlist.html", context)
