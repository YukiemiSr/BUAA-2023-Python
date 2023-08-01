# Generated by Django 4.2.1 on 2023-07-30 21:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Announcement",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("context", models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name="ChapterInfo",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=64)),
                ("context", models.TextField(max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name="GroupInfo",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=64)),
                ("notice", models.TextField(max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name="ListInfo",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(blank=True, max_length=16)),
                (
                    "authority",
                    models.SmallIntegerField(
                        choices=[(0, "仅自己"), (1, "群组内共享"), (2, "所有人")], default=0
                    ),
                ),
                ("introduction", models.CharField(default="", max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name="QuestInfo",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(blank=True, max_length=16)),
                ("context", models.CharField(max_length=1000)),
                ("answer", models.CharField(default="", max_length=1000)),
                (
                    "type",
                    models.SmallIntegerField(
                        choices=[(2, "填空题"), (3, "简答题"), (0, "暂无"), (1, "选择题")],
                        default=0,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="UserInfo",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("account", models.CharField(max_length=16)),
                ("password", models.CharField(max_length=64)),
                (
                    "privilege",
                    models.SmallIntegerField(choices=[(1, "管理员"), (2, "普通用户")]),
                ),
                ("name", models.CharField(blank=True, max_length=64)),
                (
                    "sex",
                    models.SmallIntegerField(
                        choices=[(2, "女"), (1, "男"), (0, "不详")], default=0
                    ),
                ),
                ("school", models.CharField(blank=True, max_length=64)),
                ("age", models.IntegerField(blank=True, null=True)),
                ("home", models.CharField(blank=True, max_length=64)),
                ("sign", models.CharField(blank=True, max_length=64)),
                ("email", models.CharField(blank=True, max_length=64)),
                ("profile", models.CharField(default="/user.png", max_length=64)),
                ("lastLoginTime", models.DateTimeField(auto_now_add=True)),
                (
                    "fortune",
                    models.SmallIntegerField(
                        choices=[
                            (4, "下下签"),
                            (2, "中签"),
                            (3, "下签"),
                            (1, "上签"),
                            (0, "上上签"),
                        ],
                        default=0,
                    ),
                ),
                ("questCnt", models.IntegerField(default=0)),
                ("wrongCnt", models.IntegerField(default=0)),
                ("loginCnt", models.IntegerField(default=0)),
                ("uploadCnt", models.IntegerField(default=0)),
                ("developCnt", models.IntegerField(default=0)),
                ("answerCnt", models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name="UserToQuest",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("cnt", models.IntegerField(default=0)),
                ("rightCnt", models.IntegerField(default=0)),
                (
                    "quest",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="app01.questinfo",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="app01.userinfo"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="UserRecord",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("time", models.DateTimeField(auto_now_add=True)),
                (
                    "correct",
                    models.SmallIntegerField(choices=[(1, "正确"), (0, "错误")], default=1),
                ),
                (
                    "quest",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="app01.questinfo",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="app01.userinfo"
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="questinfo",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="app01.userinfo"
            ),
        ),
        migrations.CreateModel(
            name="QuestBank",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "chapter",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="app01.chapterinfo",
                    ),
                ),
                (
                    "quest",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="app01.questinfo",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="ListToQuest",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "list",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="app01.listinfo"
                    ),
                ),
                (
                    "quest",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="app01.questinfo",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="listinfo",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="app01.userinfo"
            ),
        ),
        migrations.CreateModel(
            name="GroupToUser",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "group",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="app01.groupinfo",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="app01.userinfo"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="GroupToQuest",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "group",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="app01.groupinfo",
                    ),
                ),
                (
                    "quest",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="app01.questinfo",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="GroupToList",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "group",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="app01.groupinfo",
                    ),
                ),
                (
                    "list",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="app01.listinfo"
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="groupinfo",
            name="adm",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="app01.userinfo"
            ),
        ),
    ]