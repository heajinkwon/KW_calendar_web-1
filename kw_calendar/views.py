from django.shortcuts import render
from django.shortcuts import redirect
# Create your views here.
from evaluation import evaluation_find
from zoom_link import zoom_link_find
from major import major_find
import kw
from kw import kw_scraping
from django.views.decorators.csrf import csrf_exempt
import re

def calendar(request):
    # 웹 스크랩핑 중 오류 처리
    if not kw.checkId():
        return render(request, 'login.html')
    NameAndDeadLine = []
    # try:
    kw_hw, subjAndColor = kw_scraping()
    title = []
    for i in kw_hw.keys():
        title.append(i)

    for i in title:
        for j in kw_hw[i]:
            NameAndDeadLine.append(j)

    content = {'subject': title, 'homeworks': NameAndDeadLine, 'subjAndColors': subjAndColor}
    return render(request, 'calendar.html', content)

    # except Exception as error:
    #     print(error)
    #     return render(request, "error.html")


@csrf_exempt
def goToPage(request):
    print(request.method)
    if request.method == "POST":
        value = request.POST.get("pageNum")
        if value == "1":
            # 강의 공지사항 링크로 접속
            kw.goToUrl('https://klas.kw.ac.kr/std/lis/sport/d052b8f845784c639f036b102fdc3023/BoardListStdPage.do')
        elif value == "2":
            # 과제란
            kw.goToUrl('https://klas.kw.ac.kr/std/lis/evltn/TaskStdPage.do')
        elif value == "3":
            # 온라인 강의
            kw.goToUrl('https://klas.kw.ac.kr/std/lis/evltn/OnlineCntntsStdPage.do')
    return render(request, 'running.html')


def test(request):
    return render(request, 'test.html')


def index(request):
    return render(request, 'index.html')


def alarm(request):
    return render(request, 'alarm.html')


def zoom_link(request):
    # 웹 스크랩핑 중 오류 처리
    if not kw.checkId():
        return render(request, 'login.html')

    zoom_link_find()
    zoomlinks = dict()  # key : 과목명, value : 줌링크 , id
    indexs = ""  # 과목명 담는 임시변수
    urls = ""  # 줌링크 담는 임시변수
    zoomid = ""  # 줌 아이디 담는 임시변수
    with open("zoomlink.txt", "r", encoding='utf-8') as k:
        read_line = k.readlines()

    for i in read_line:
        index = i.find(',')
        indexs = i[2:index - 1]  # 과목명들

        un_urls = i[index + 1:].strip(')').replace('\'', '').replace("[]", "줌 링크가 없습니다! ")
        urls = re.sub("\)|\'", "", un_urls).strip()  # 줌링크들

        # 링크에서 줌 아이디 추출하기
        count = 0
        index = -1

        cut_index = urls.find('?')
        while True:
            index = urls.find('/', index + 1)
            if index == -1:
                break
            count = count + 1
            if (count == 4):
                real_index = index

        zoomid = urls[real_index + 1: cut_index].strip(')')
        zoomlinks[indexs] = [urls, zoomid]  # zoomlinks[과목명] = [ 링크 , 줌 아이디 ]
    content = {'zoomlinks': zoomlinks}
    return render(request, 'zoom_link.html', content)


def major_site(request):
    # 웹 스크랩핑 중 오류 처리
    if not kw.checkId():
        return render(request, 'login.html')

    major_find()
    with open("major.txt", "r", encoding='utf-8') as f:
        my_major = f.readline()

    with open("major_url.txt", "r", encoding='utf-8') as f:
        for search_major in f:
            search_major = search_major.rstrip("\n")
            if (search_major in my_major):
                major_url = f.readline()
                major_image = f.readline()
                break
            else:
                major_url = " "
                major_image = " "

    content = {'major': my_major, 'major_url': major_url, 'major_image': major_image}
    return render(request, 'major_site.html', content)


def login(request):
    # id 와 password 입력받을 시,
    if request.method == "POST":
        id = request.POST["id"]
        password = request.POST["password"]

        with open("secret.txt", "w") as f:
            f.write(id)
            f.write("\n")
            f.write(password)
            f.close()

        if id and password:
            return redirect('/kw/calendar/')

    return render(request, 'login.html')


def evaluation(request):
    # 웹 스크랩핑 중 오류 처리
    if not kw.checkId():
        return render(request, 'login.html')

    evaluation_find()
    sub = dict()  # 과목 정보 저장할 딕셔너리 선언
    with open("evaluation_rate.txt", "r", encoding='utf-8') as f:
        lines = f.read().splitlines()
        total_sub = int(len(lines) / 5)
        print("이번 학기 총 수강 과목은 " + str(total_sub) + "과목입니다 \n")  # 총 과목 수

        # 딕셔너리 안에 정보 추가
        title = ""
        evaluate = ""
        scores = ""
        email = ""
        email_url = ""

        for i in range(0, len(lines), 5):
            # 5 개씩 끊기
            title = lines[i]
            evaluate = lines[i + 1]
            scores = lines[i + 2]
            email = lines[i + 3]
            email_url = lines[i + 4]
            # key : 과목 , value : 평가기준, 평가점수, 이메일, 이메일 url
            sub[title] = [evaluate, scores, email, email_url]
            content = {'total_sub': total_sub, 'sub': sub}
    return render(request, 'evaluation.html', content)


