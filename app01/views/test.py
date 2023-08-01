import datetime
import random

from django.shortcuts import render

from app01.models import *
from app01.utils.encrypt import encrypt


# 基础数据
def test(request):
    # 测试数据参数设定
    min_user_id = 1
    max_user_id = 100
    min_group_id = 1
    max_group_id = 5  # 为确保第i个用户在第i个组中group_id的阈值必须包含于user_id
    min_quest_id = 1
    max_quest_id = 100
    min_chapter_id = 1
    max_chapter_id = 8
    rate = 30  # 各种对应关系的随机指数

    # 基础数据
    ## 构造用户数据
    UserInfo.objects.all().delete()
    for i in range(min_user_id, max_user_id):
        UserInfo.objects.create(account=str(i), password=encrypt(str(i)), privilege=2, name="随机用户-" + str(i),
                                questCnt=max_user_id, wrongCnt=random.randint(1, 100), loginCnt=random.randint(1, 100),
                                uploadCnt=random.randint(1, 100), developCnt=random.randint(1, 100),
                                answerCnt=random.randint(1, 100), fortune=random.randint(0, 4))
        ### 修改用户的头像路径来实现头像对齐
        ### 这里头像的随机值要注意与文件储存路径中的阈值匹配
        UserInfo.objects.filter(account=str(i)).update(profile=str(random.randint(1, 10)) + ".png")
    ## 构造问题数据
    QuestInfo.objects.all().delete()
    for user in UserInfo.objects.all():
        QuestInfo.objects.create(title="问题" + str(user.id), user=user, type=random.randint(1, 3))
    ### --读入公告
    f = open("app01/static/context/groupAnnounce.txt", encoding='utf-8')
    announce = f.read()
    f.close()
    ## --构造群组数据
    GroupInfo.objects.all().delete()
    ### --第i个群组的管理员为第i个用户 --在构造对应关系时需要确保这一点
    userIds = []
    for user in UserInfo.objects.all():
        userIds.append(user.id)
    for i in range(min_group_id, max_group_id):
        group = GroupInfo.objects.create(name="群组" + str(i), notice=announce, adm_id=userIds[i - 1])
    ## 构造章节数据
    ChapterInfo.objects.all().delete()
    for i in range(min_chapter_id, max_chapter_id):
        ChapterInfo.objects.create(name='章节' + str(i), context='内容' + str(i))

    # 对应关系
    ## 构造历史记录
    UserRecord.objects.all().delete()
    for user in UserInfo.objects.all():
        for quest in QuestInfo.objects.all():
            if random.randint(1, 100) < rate:
                UserRecord.objects.create(user=user, quest=quest)
    ## 构造用户所在的群组数据
    GroupToUser.objects.all().delete()
    for group in GroupInfo.objects.all():
        for user in UserInfo.objects.all():
            if random.randint(1, 100) < rate:
                GroupToUser.objects.create(user=user, group=group)
        ### 确保管理员在这个群组中
        if GroupToUser.objects.filter(group=group, user=group.adm).count() == 0:
            GroupToUser.objects.create(group=group, user=group.adm)
        ### 确保管理员有全局权限
        UserInfo.objects.filter(id=group.adm_id).update(privilege=1)

    ## 构造群组包含的问题信息
    GroupToQuest.objects.all().delete()
    for group in GroupInfo.objects.all():
        for quest in QuestInfo.objects.all():
            if random.randint(1, 100) < rate:
                GroupToQuest.objects.create(group=group, quest=quest)
    ## 构造章节和题目对应关系
    for chapter in ChapterInfo.objects.all():
        for quest in QuestInfo.objects.all():
            if random.randint(1, 100) < rate:
                QuestBank.objects.create(chapter=chapter, quest=quest)

    return render(request, "test.html", {"info": "基础数据生成完成"})


# 测试日期图表功能
def timeChart(request):
    # 设置起始时间
    base = datetime.datetime(2023, 6, 30, 8, 0, 0, 0)
    # 设置1天的时间间隔
    oneDay = datetime.timedelta(days=1)
    # 设置最大生成天数
    maxDay = 100
    # 设置每天访问题目数量的阈值
    minCnt = 5
    maxCnt = 30

    # 生成数据
    UserInfo.objects.all().delete()
    # --清除原来数据
    tmpDate = base
    user = UserInfo.objects.all().first()
    # --为随机访问问题
    questIds = []
    for quest in QuestInfo.objects.all():
        questIds.append(quest.id)
    for i in range(1, maxDay):
        for j in range(0, random.randint(minCnt, maxCnt)):
            quest_id = questIds[random.randint(0, len(questIds) - 1)]
            quest = QuestInfo.objects.filter(id=quest_id).first()
            obj = UserRecord.objects.create(user=user, quest=quest)
            UserRecord.objects.filter(id=obj.id).update(time=tmpDate)
        tmpDate += oneDay
    return render(request, "test.html", {"info": "日期图表测试数据生成完成"})


# 生成正确率的测试数据
def rightRate(request):
    # 总题目数量限制
    minCnt = 5
    maxCnt = 30
    for user in UserInfo.objects.all():
        for quest in QuestInfo.objects.all():
            cnt = random.randint(minCnt, maxCnt)
            rightCnt = random.randint(0, cnt)
            UserToQuest.objects.create(user=user, quest=quest, cnt=cnt, rightCnt=rightCnt)
    return render(request, "test.html", {"info": "正确率测试数据生成完成"})
