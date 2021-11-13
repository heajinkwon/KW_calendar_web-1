from django.shortcuts import render
from django.shortcuts import redirect

# Create your views here.
from evaluation import evaluation_find
from zoom_link import zoom_link_find
from major import major_find
import kw
from kw import kw_scraping
from django.views.decorators.csrf import csrf_exempt


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

    with open("zoomlink.txt", "r", encoding='utf-8') as f:
        zoom_link_url = f.read()
    content = {'zoom_link_url': zoom_link_url}
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
    with open("evaluation_rate.txt", "r", encoding='utf-8') as f:
        evalutaion_rate = f.read()
    content = {'evalutaion_rate': evalutaion_rate}
    return render(request, 'evaluation.html', content)
