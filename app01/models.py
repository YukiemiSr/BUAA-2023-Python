from django.db import models


# 首页公告
class Announcement(models.Model):
    context = models.CharField(max_length=64)  # 公告内容


class UserInfo(models.Model):
    # 必需信息
    account = models.CharField(max_length=16)
    password = models.CharField(max_length=64)
    # 权限的对照关系
    privilege_table = {
        (1, "管理员"),
        (2, "普通用户")
    }
    privilege = models.SmallIntegerField(choices=privilege_table)

    # 非必需信息
    name = models.CharField(max_length=64, blank=True)
    sex_table = {
        (0, "不详"),
        (1, "男"),
        (2, "女")
    }
    sex = models.SmallIntegerField(choices=sex_table, default=0)
    school = models.CharField(max_length=64, blank=True)
    age = models.IntegerField(blank=True, null=True)
    home = models.CharField(max_length=64, blank=True)
    sign = models.CharField(max_length=64, blank=True)
    email = models.CharField(max_length=64, blank=True)
    profile = models.CharField(max_length=64, default="/user.png")

    # 上次登录时间
    lastLoginTime = models.DateTimeField(auto_now_add=True)
    # 每日运势暂存处
    fortune_table = {
        (0, "上上签"),
        (1, "上签"),
        (2, "中签"),
        (3, "下签"),
        (4, "下下签")
    }
    fortune = models.SmallIntegerField(choices=fortune_table, default=0)

    # 能力指标
    questCnt = models.IntegerField(default=0)
    wrongCnt = models.IntegerField(default=0)
    loginCnt = models.IntegerField(default=0)
    uploadCnt = models.IntegerField(default=0)
    developCnt = models.IntegerField(default=0)
    answerCnt = models.IntegerField(default=0)


class QuestInfo(models.Model):
    # 问题的名称
    title = models.CharField(max_length=16, blank=True)
    # 问题的上传者(作者)
    user = models.ForeignKey(to="UserInfo", to_field="id", on_delete=models.CASCADE)
    # 问题的内容
    context = models.CharField(max_length=1000)
    # 问题的答案
    answer = models.CharField(max_length=1000, default='')
    # 问题的类型
    type_table = {
        (0, "暂无"),
        (1, "选择题"),
        (2, "填空题"),
        (3, "简答题")
    }
    type = models.SmallIntegerField(choices=type_table, default=0)


class ListInfo(models.Model):
    # 题单的名称
    name = models.CharField(max_length=16, blank=True)
    # 题单的创建者(作者)，拥有最初权限
    #   -django自动生成链接--写的是user，但生成列名为user_id
    user = models.ForeignKey(to="UserInfo", to_field="id", on_delete=models.CASCADE)
    # 题单的权限
    authority_table = {
        (0, "仅自己"),
        (1, "群组内共享"),
        (2, "所有人")
    }
    authority = models.SmallIntegerField(choices=authority_table, default=0)
    # 题单的简介
    introduction = models.CharField(max_length=1000, default='')


# 存放组信息
class GroupInfo(models.Model):
    # 这是群组的名字
    name = models.CharField(max_length=64)
    # 链接到管理员
    #   -django自动生成链接--写的是adm，但生成列名为adm_id
    #   -若身为管理员的用户被删除，此表中的管理员信息也会删除
    adm = models.ForeignKey(to="UserInfo", to_field="id", on_delete=models.CASCADE)
    # 这是这个群组的通知
    notice = models.TextField(max_length=1000)


# 用户-群组关系对照表
class GroupToUser(models.Model):
    # 链接到用户
    #   -django自动生成链接--写的是user，但生成列名为user_id
    #   -若在表QuestInfo中删除问题，此表中的问题也会自动删除
    user = models.ForeignKey(to="UserInfo", to_field="id", on_delete=models.CASCADE)
    # 链接到群组
    #   -django自动生成链接--写的是group，但生成列名为group_id
    #   -若在表GroupInfo中删除问题，此表中的群组也会自动删除
    group = models.ForeignKey(to="GroupInfo", to_field="id", on_delete=models.CASCADE)


# 问题-群组关系对照表
class GroupToQuest(models.Model):
    # 链接到问题
    #   -django自动生成链接--写的是quest，但生成列名为quest_id
    #   -若在表QuestInfo中删除问题，此表中的问题也会自动删除
    quest = models.ForeignKey(to="QuestInfo", to_field="id", on_delete=models.CASCADE)
    # 链接到群组
    #   -django自动生成链接--写的是group，但生成列名为group_id
    #   -若在表GroupInfo中删除问题，此表中的群组也会自动删除
    group = models.ForeignKey(to="GroupInfo", to_field="id", on_delete=models.CASCADE)


# 用户历史记录关系对照表
class UserRecord(models.Model):
    # 链接到用户
    #   -django自动生成链接--写的是user，但生成列名为user_id
    #   -若在表QuestInfo中删除问题，此表中的问题也会自动删除
    user = models.ForeignKey(to="UserInfo", to_field="id", on_delete=models.CASCADE)
    # 链接到问题
    #   -django自动生成链接--写的是quest，但生成列名为quest_id
    #   -若在表QuestInfo中删除问题，此表中的问题也会自动删除
    quest = models.ForeignKey(to="QuestInfo", to_field="id", on_delete=models.CASCADE)
    # 最近访问时间
    time = models.DateTimeField(auto_now_add=True)
    # 该次是否答对
    record_table = {
        (0, "错误"),
        (1, "正确")
    }
    correct = models.SmallIntegerField(choices=record_table, default=1)


# 章节信息
class ChapterInfo(models.Model):
    # 章节名称
    name = models.CharField(max_length=64)
    # 章节描述
    context = models.TextField(max_length=1000)


# 题库索引表
class QuestBank(models.Model):
    # 链接到章节
    #   -django自动生成链接--写的是chapter，但生成列名为chapter_id
    #   -若在表QuestInfo中删除问题，此表中的问题也会自动删除
    chapter = models.ForeignKey(to="ChapterInfo", to_field="id", on_delete=models.CASCADE)
    # 链接到问题
    #   -django自动生成链接--写的是quest，但生成列名为quest_id
    #   -若在表QuestInfo中删除问题，此表中的问题也会自动删除
    quest = models.ForeignKey(to="QuestInfo", to_field="id", on_delete=models.CASCADE)


# 用户和题的映射表，用于计算正确率
class UserToQuest(models.Model):
    # 链接到用户
    #   -django自动生成链接--写的是user，但生成列名为user_id
    #   -若在表QuestInfo中删除问题，此表中的问题也会自动删除
    user = models.ForeignKey(to="UserInfo", to_field="id", on_delete=models.CASCADE)
    # 链接到问题
    #   -django自动生成链接--写的是quest，但生成列名为quest_id
    #   -若在表QuestInfo中删除问题，此表中的问题也会自动删除
    quest = models.ForeignKey(to="QuestInfo", to_field="id", on_delete=models.CASCADE)
    # 总次数
    cnt = models.IntegerField(default=0)
    # 正确次数
    rightCnt = models.IntegerField(default=0)


# 题单中含有的题目
class ListToQuest(models.Model):
    list = models.ForeignKey(to="ListInfo", to_field="id", on_delete=models.CASCADE)
    quest = models.ForeignKey(to="QuestInfo", to_field="id", on_delete=models.CASCADE)


# 群组中共享的题单
class GroupToList(models.Model):
    group = models.ForeignKey(to="GroupInfo", to_field="id", on_delete=models.CASCADE)
    list = models.ForeignKey(to="ListInfo", to_field="id", on_delete=models.CASCADE)
