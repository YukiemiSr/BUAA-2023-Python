from django.shortcuts import render
from django.db.models import Q
from app01.models import QuestInfo, QuestBank, ChapterInfo, ListInfo, ListToQuest, UserInfo
from app01.utils.pagination import Pagination


def question_bank(request):
    user_session = request.session.get("info")
    user_id = user_session.get("id")
    # 获取用户信息数据
    user_infos = UserInfo.objects.filter(id=user_id)
    user_info = user_infos.first()
    user_id = request.session.get("info").get("id")
    reuse = 0

    # 添加题目到表单
    if request.method == "POST":
        checkboxes = request.POST.getlist("checkboxes")
        list_name = request.POST.get("list_name")
        # 若无该表单，则创建
        ListInfo.objects.get_or_create(name=list_name, defaults={"user_id": user_id})
        if ListInfo.objects.get(name=list_name).user_id != user_id:
            reuse = 1
        list_id = ListInfo.objects.get(name=list_name).id
        for qid in checkboxes:
            ListToQuest.objects.get_or_create(list_id=list_id, quest_id=qid)
    list_rest = ListInfo.objects.filter(user_id=user_id).order_by("name")

    # 搜索相关
    data_str = request.GET.get("search_text")
    data_s1 = request.GET.get("question_type")
    data_s2 = request.GET.get("question_chapter")
    data_s1 = data_s1 if data_s1 else "0"
    data_s2 = data_s2 if data_s2 else "0"

    qid_rest = QuestInfo.objects.all().values_list("id", flat=True)
    if data_str:
        qid_rest = QuestInfo.objects.filter(Q(title__contains=data_str) | Q(context__contains=data_str)) \
            .values_list("id", flat=True)
    if data_s1 != "0":
        qid_rest = QuestInfo.objects.filter(type=data_s1, id__in=qid_rest).values_list("id", flat=True)
    if data_s2 != "0":
        qid_rest = QuestBank.objects.filter(chapter_id=data_s2, quest_id__in=qid_rest).values_list("quest_id", flat=True)

    question_rest = QuestInfo.objects.filter(id__in=qid_rest)

    # 分页相关
    page_object = Pagination(request, question_rest, 10)
    # 提取题库通知，如果失败则赋一个默认值
    now_chapter = ChapterInfo.objects.filter(id=data_s2).first()
    notice = now_chapter.context if now_chapter else ""

    context = {
        "reuse": reuse,
        "type_id": int(data_s1),
        "cid": int(data_s2),
        "cname": now_chapter.name if data_s2 != "0" else "0",
        "c_notice": notice,
        "clist": ChapterInfo.objects.all(),
        "qlist": page_object.page_queryset,
        "list_lists": list_rest,
        "page_string": page_object.html(),
        "user_info": user_info
    }

    return render(request, "qbank.html", context)
