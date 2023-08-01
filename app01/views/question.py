from django.shortcuts import render
from django.db.models import F
from app01.models import QuestInfo, UserRecord, UserToQuest, ListInfo, ListToQuest, UserInfo


def question(request):
    user_session = request.session.get("info")
    user_id = user_session.get("id")
    # 获取用户信息数据
    user_infos = UserInfo.objects.filter(id=user_id)
    user_info = user_infos.first()
    show_ans = False 
    qid = request.GET.get("qid")
    user_id = request.session.get("info").get("id")
    q_now = QuestInfo.objects.filter(id=qid).first()
    ans_input = request.POST.get("ans_input")
    correct = 0
    if request.method == "POST" and ans_input != "":
        show_ans = True
        ans_input = ans_input.lower()
        ans_input = "".join(ans_input.split())
        correct = 1 if ans_input == q_now.answer else 0
        UserRecord.objects.create(user_id=user_id, quest_id=qid, correct=correct)
        # 增加rightcnt和cnt
        UserToQuest.objects.get_or_create(user_id=user_id, quest_id=qid)
        UserToQuest.objects.filter(user_id=user_id, quest_id=qid).update(rightCnt=F('rightCnt') + correct,
                                                                         cnt=F('cnt') + 1)
    # 上一题、下一题
    qid = int(qid)
    qid_last = "/question/?qid=" + str(qid - 1 if qid > 1 else 1)
    qid_next = "/question/?qid=" + str(qid + 1 if qid < QuestInfo.objects.all().count() else qid)
    lid = request.GET.get("lid")
    if lid:
        order_list = ListToQuest.objects.filter(list_id=lid).order_by("quest_id").values_list("quest_id", flat=True)
        order_list = list(order_list)
        no = order_list.index(qid)
        id_last = qid if no == 0 else order_list[no - 1]
        id_next = qid if no == len(order_list)-1 else order_list[no+1]
        qid_last = "/question/?qid=" + str(id_last) + "&lid=" + lid
        qid_next = "/question/?qid=" + str(id_next) + "&lid=" + lid

    context = {
        "qid": qid,
        "q_now": q_now,
        "show_ans": show_ans,
        "ans_input": ans_input,
        "correct": correct,
        "last": qid_last,
        "next": qid_next,
        "user_info":user_info
    }
    return render(request, "question.html", context)
