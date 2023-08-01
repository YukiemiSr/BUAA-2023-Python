import os

from django.shortcuts import render, redirect
from PIL import Image
from app01.models import UserInfo, GroupToUser
from django.http import JsonResponse


def user(request):
    # 获取用户session
    user_session = request.session.get("info")
    user_id = user_session.get("id")
    # 获取用户信息数据
    user_info = UserInfo.objects.filter(id=user_id).first()
    # 获取用户群组信息
    groupLinks = GroupToUser.objects.filter(user_id=user_id)
    # 测试上传头像
    return render(request, "user.html", {"user_info": user_info, "groupLinks": groupLinks})


def user_delete(request):
    nid = request.GET.get('nid')
    UserInfo.objects.filter(id=nid).delete()
    return redirect("/user/list/")


def user_list(request):
    data_list = UserInfo.objects.all()
    is_null = True if len(data_list) == 0 else False
    return render(request, "user_list.html", {"data_list": data_list, "is_null": is_null})


def user_edit(request):
    # 得到用户信息
    user_session = request.session.get("info")
    user_id = user_session.get("id")

    # 获取用户信息数据
    user_infos = UserInfo.objects.filter(id=user_id)
    user_info = user_infos.first()
    # get方法访问时--未提交表单的状态
    if request.method == 'GET':
        return render(request, "user_edit.html", {"user_info": user_info})

    # 取得输入信息
    # 对输入的年龄进行判断
    ageStr = str(request.POST.get("age"))
    age = None
    if ageStr.isdigit():
        age = int(ageStr)
    elif ageStr == '':
        age = None
    else:
        return render(request, "user_edit.html", {"err": 1})
    # 处理性别选项
    sex = request.POST.get("sex")
    # 处理其他输入信息
    input_img = request.FILES.get("img")
    if user_info.age == "":
        user_infos.update(age=0)
    age = user_info.age if request.POST.get("age") == "" else request.POST.get("age")
    email = user_info.email if request.POST.get("email") == ""  else request.POST.get("email")
    home = user_info.home if request.POST.get("home") == "" else request.POST.get("home")
    school = user_info.school if request.POST.get("school") == "" else request.POST.get("school")
    sign =user_info.sign if request.POST.get("sign") == "" else request.POST.get("sign")
    name = user_info.name if request.POST.get("name") == "" else request.POST.get("name")
    # 根据是否上传了头像分别处理
    if input_img is None:
        user_infos.update(name=name, email=email, school=school, home=home, sex=sex, sign=sign,age=age)
    else:
        img = Image.open(input_img)
        img.save(os.getcwd() + '/app01/static/user_img/' + str(user_id) + '.png')
        user_infos.update(name=name, email=email, school=school, home=home, sex=sex, sign=sign, age=age,
                          profile=str(user_id) + '.png')
    return render(request, "user_edit.html", {"user_info": user_info, "err": 0})


def user_ChartInfo(request):
    # 取得用户信息
    user_id = request.session.get("info").get("id")
    user_info = UserInfo.objects.filter(id=user_id).first()
    # 构造雷达图的数据
    value = [user_info.questCnt, 100 - user_info.wrongCnt if user_info.questCnt > 0 else 0,
             user_info.loginCnt, user_info.uploadCnt, user_info.answerCnt, user_info.developCnt]
    result = {
        "status": True,
        "series": [
            {
                "name": '成长之路',
                "type": 'radar',
                "data": [
                    {
                        "value": value,
                        "name": '成长之路'
                    }
                ]
            }
        ]
    }
    return JsonResponse(result)
