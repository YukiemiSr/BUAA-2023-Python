from django.shortcuts import render

from app01.models import UserInfo
from app01.utils.encrypt import encrypt


def register(request):
    # err: is_null:1 ; same_name 2; not_same:3 ; code_err 4 ; ok -1
    if request.method == 'GET':
        return render(request, "register.html", {"err": 0})

    user_account = request.POST.get("account")
    pwd = request.POST.get("pwd")
    confirm_pwd = request.POST.get("confirm_pwd")
    is_adm = request.POST.get("is_adm")
    invitation_code = request.POST.get("invitation_code")
    userinfo = UserInfo.objects.filter(account=user_account)

    if user_account == "" or pwd == "":
        return render(request, "register.html", {"err": 1})
    elif userinfo.exists():
        return render(request, "register.html", {"err": 2})
    elif pwd != confirm_pwd:
        return render(request, "register.html", {"err": 3})
    elif is_adm and int(invitation_code) != 123456:
        return render(request, "register.html", {"err": 4})
    else:
        UserInfo.objects.create(account=str(user_account), password=encrypt(pwd),
                                privilege=1 if is_adm else 2)
        return render(request, "register.html", {"err": -1})

