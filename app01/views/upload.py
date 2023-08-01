import os

from django.http import HttpResponse
from django.shortcuts import render

from app01.models import QuestInfo,UserInfo,ChapterInfo,QuestBank


#.txt格式：题目#所属章节#内容#答案#题目类型
def upload(request):
    user_id = request.session.get("info").get("id")
    user = UserInfo.objects.filter(id=user_id).first()
    if request.method == 'GET':
        return render(request, "upload.html",{"user_info":user})
    dirlist = request.FILES.getlist("file2")
    dir = request.FILES.get("file1")
    if not dirlist and not dir:
        return HttpResponse("没有上传内容")
    else:
        if dirlist:
            for file in dirlist:
                s = os.getcwd() + '/app01/media/' +str(file)
                storage = open(s,'wb')
                for chunk in file.chunks():
                    storage.write(chunk)
                storage.close()
                #保存好文件之后，必须用f2以只读形式打开才可以读取内容
                f2 = open(s, 'r', encoding='utf-8')
                content = f2.read()
                ss = content.split("#")
                f2.close()
                QuestInfo.objects.create(title=ss[0], context=ss[2], user=user, answer=ss[3].replace("\n", ""), type=int(ss[4]))
                questinfo = QuestInfo.objects.filter(title=ss[0]).first()
                chapterInfo = ChapterInfo.objects.filter(name=ss[1].replace("\n", "")).first()
                QuestBank.objects.create(chapter_id=chapterInfo.id, quest=questinfo)
                storage.close()
        if dir:#单文件
                s = os.getcwd() + '/app01/media/' + str(dir)
                storage = open(s, 'wb')
                for chunk in dir.chunks():
                    storage.write(chunk)
                storage.close()
                # 保存好文件之后，必须用f2以只读形式打开才可以读取内容
                f2 = open(s, 'r', encoding='utf-8')
                content = f2.read()
                ss = content.split("#")
                f2.close()
                QuestInfo.objects.create(title=ss[0], context=ss[2], user=user, answer=ss[3].replace("\n", ""),type=int(ss[4]))
                questinfo = QuestInfo.objects.filter(title=ss[0]).first()
                chapterInfo = ChapterInfo.objects.filter(name=ss[1].replace("\n", "")).first()
                QuestBank.objects.create(chapter_id=chapterInfo.id,quest=questinfo)
                storage.close()
        return render(request, "upload.html",{"user_info":user})  # 成功提交

