from django.shortcuts import render

# Create your views here.

import xlwt
from django.http import HttpResponse
from django.contrib.auth.models import User
from core.models import Team


def home(request):
    return render(request,'test.html')

def getExelFile(request):
    response = HttpResponse(content_type = 'application/ms-excel')
    response['Content-Disposition']= 'attachment ; filename = "users.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Users Data')

    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    columns = ['Username','First Name','Last Name','Email Address']

    for col_num in range(len(columns)):
        ws.write(row_num,col_num,columns[col_num],font_style)

    font_style = xlwt.XFStyle()

    rows = User.objects.all().values_list('username','first_name','last_name','email')

    for row in rows:
        row_num +=1
        for col_num in range(len(row)):
            ws.write(row_num,col_num,row[col_num],font_style)

    wb.save(response)

    return response


def getLeaderboard(request):
    response = HttpResponse(content_type = 'application/ms-excel')
    response['Content-Disposition']= 'attachment ; filename = "leaderborad.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Users Data')

    
    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    row_num = 0
    
    ws.write(row_num,0,'Junior Leaderboard',font_style)
    
    columns = ['TeamId','User1','User1','Score','isJunior','Rank']

    row_num +=2 
    for col_num in range(len(columns)):
        ws.write(row_num,col_num,columns[col_num],font_style)

    font_style = xlwt.XFStyle()

    junior_query = Team.objects.filter(isJunior=True).order_by("-score", "lastUpdate").values_list('teamId','user1__username','user2__username','score','isJunior','lastUpdate')

    row_num +=1
    rank = 1
    for row in junior_query:
        row_num +=1
        for col_num in range(len(row)-1):
            ws.write(row_num,col_num,row[col_num],font_style)
        ws.write(row_num,len(row)-1,rank,font_style)
        rank +=1


# Senior

    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    
    row_num +=3
    ws.write(row_num,0,'Senior Leaderboard',font_style)
    
    columns = ['TeamId','User1','User1','Score','isJunior','Rank']

    row_num +=2
    for col_num in range(len(columns)):
        ws.write(row_num,col_num,columns[col_num],font_style)

    font_style = xlwt.XFStyle()
    senior_query = Team.objects.filter(isJunior=False).order_by("-score", "lastUpdate").values_list('teamId','user1__username','user2__username','score','isJunior','lastUpdate')


    row_num +=1
    rank = 1
    for row in senior_query:
        row_num +=1
        for col_num in range(len(row)-1):
            ws.write(row_num,col_num,row[col_num],font_style)
        ws.write(row_num,len(row)-1,rank,font_style)
        rank +=1
    
    
    
    wb.save(response)

    return response
