from django.shortcuts import render

from app01.models import UserRecord, UserInfo, UserToQuest,QuestInfo
from app01.models import Announcement

import datetime
import calendar
from django.http import JsonResponse
from app01.utils.recommend import recommend
# 主页信息
def index(request):
    user_session = request.session.get("info")
    user_id = user_session.get("id")
    # 获取用户信息数据
    user_infos = UserInfo.objects.filter(id=user_id)
    user_info = user_infos.first()
    # 获取用户信息
    user_id = request.session.get("info").get("id")
    nowUser = UserInfo.objects.filter(id=user_id).first()
    user_quest_record = UserToQuest.objects.filter(user_id = user_id)
    lists = []
    err = 0 #还没做够10个题没有推荐
    if user_quest_record.count() < 10:
        err = 1
    else:
        # rec为推荐的列表id
        rec_list = recommend(data_pre(), int(user_id))
        # 获得推荐题
        lists = []
        for i in rec_list:
            lists.append(QuestInfo.objects.filter(id=i).first().title)
    announcements = Announcement.objects.all()[:3]
    number = announcements.count()

    # 保证没有三个公告的情况
    f1 = open("app01/static/context/announce1.txt", encoding='utf-8')
    f2 = open("app01/static/context/announce2.txt", encoding='utf-8')
    f3 = open("app01/static/context/announce3.txt", encoding='utf-8')

    first = f1.readlines()
    second = f2.readlines()
    third = f3.readlines()

    # todo 这里要将context解析成lines
    if number >= 1:
        first = announcements[0].context
    if number >= 2:
        second = announcements[1].context
    if number >= 3:
        third = announcements[2].context

    # 日期对照表
    dict1 = {'0': '零', '1': '一', '2': '二', '3': '三', '4': '四',
             '5': '五', '6': '六', '7': '七', '8': '八', '9': '九',
             "Monday": '星期一', "Tuesday": "星期二", "Wednesday": "星期三",
             "Thursday": '星期四', "Friday": '星期五', "Saturday": "星期六",
             "Sunday": "星期日"}
    now = datetime.datetime.now()
    month = now.month
    day = now.day
    month = dict1[str(month)] + "月"
    if day > 20:
        month = month + "下"
    elif 10 <= day <= 20:
        month = month + "中"
    else:
        month = month + "上"

    fortuneList = ['上上签', '上签', '中签', '下签', '下下签']

    confirm = {
        "first": first,
        "second": second,
        "third": third,
        "month": month,
        "day": day,
        "weekday": dict1[calendar.day_name[now.weekday()]],
        "fortune": fortuneList[nowUser.fortune],
        "list":lists,
        "err":err,
        "user_info":user_info
    }

    return render(request, "index.html", confirm)


# 表格信息更新
def index_chartInfo(request):
    # 取得用户信息
    user_id = request.session.get("info").get("id")
    user_records = UserRecord.objects.filter(user_id=user_id)

    # 构造曲线图的数据
    data = []
    # 选择起始时间，获取现在时间
    base = datetime.date(2023, 6, 30)
    today = datetime.date.today()
    tmpDate = base
    # 构造一天的时间间隔
    oneDay = datetime.timedelta(days=1)

    while tmpDate < today:
        amount = len(user_records.filter(time__year=tmpDate.year, time__month=tmpDate.month, time__day=tmpDate.day))
        data.append([tmpDate, amount])
        tmpDate += oneDay

    result = {
        "status": True,
        "series": [
            {
                "name": '做题数',
                "type": 'line',
                "smooth": True,
                "symbol": 'none',
                "areaStyle": {},
                "data": data
            },
        ]
    }

    return JsonResponse(result)

def data_pre():
    dic_list = {}
    data_list = UserToQuest.objects.all()
    for data in data_list:
        user = data.user_id
        if user not in dic_list:
            dic_list[user] = {}
        questlist = dic_list[user]
        quest = data.quest.id
        accuracy = 100-int((data.rightCnt / data.cnt) * 100)
        # 大于两次的做题记录才会被统计
        if data.cnt > 2:
            questlist[quest] = accuracy
    return dic_list
