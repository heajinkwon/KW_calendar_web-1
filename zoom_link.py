from selenium import webdriver
import time
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.support.select import Select
from bs4 import BeautifulSoup
from urllib.request import urlopen

def zoom_link_find():
    browser = webdriver.Chrome()
    with open("secret.txt", "r") as f:
        line = f.readline()
        loginId = line.split(':')[-1].replace('\n', '').strip()
        line = f.readline()
        loginPwd = line.split(':')[-1].replace('\n', '').strip()
    url = "https://klas.kw.ac.kr/std/lis/sport/d052b8f845784c639f036b102fdc3023/BoardListStdPage.do"
    browser.get(url)

    delay = 1

    # id 입력
    elem = browser.find_element_by_id("loginId")
    elem.clear()
    elem.send_keys(loginId)
    # pwd 입력
    elem = browser.find_element_by_id("loginPwd")
    elem.clear()
    elem.send_keys(loginPwd)
    time.sleep(delay)
    # login 버튼 누르기
    browser.find_element_by_class_name("btn").click()
    browser.implicitly_wait(delay)
    time.sleep(3)

    # zoomlink 담을 dictionary 생성
    zoom_link = {}
    # 과목수 불러오기
    elem = browser.find_element_by_class_name("col-md-7")
    elem = elem.find_element_by_class_name("form-control-sm")
    select = Select(elem)

    subject_index = len(select.options)

    sub = "/html/body/section/div[2]/div/div[1]/div/div[2]/div/div[2]/select/option["
    ject = "]"
    for i in range(1, subject_index + 1):
        subject_index = i
        # xpath 이용
        subject_url = sub + str(i) + ject
        # 과목이름 저장
        subject = browser.find_element_by_xpath(subject_url).text
        zoom_link[subject] = []
        browser.find_element_by_xpath(subject_url).click()
        time.sleep(1)

        tbodys = browser.find_element_by_xpath("/html/body/section/div[2]/div/div[2]/table/tbody")
        tr = tbodys.find_elements_by_tag_name("tr")
        tr_count = 0
        time.sleep(1)

        # 각 과목의 공지사항 tr의 갯수 알아내기
        for td in tr:
            row = td.text
            row_list = row.split("\n")
            tr_count = tr_count + 1
            if (row == "글이 없습니다."):
                tr_count = 0

        tr_con = "/html/body/section/div[2]/div/div[2]/table/tbody/tr["
        tr_tent = "]/td[2]"

        for i in range(1, tr_count + 1):
            # 빠른 처리(zoomlink를 찾으면 더이상 읽지 않고 종료)를 위한 count 변수
            count = 0
            # xpath 이용
            tr_content = tr_con + str(i) + tr_tent
            # 공지사항 항목들 클릭
            notice_title = browser.find_element_by_xpath(tr_content).text
            if (
                    "webex" in notice_title or "수업 운영 방식 공지" in notice_title or "실시간 비대면" in notice_title or "비대면" in notice_title
                    or "실시간" in notice_title or "Zoom" in notice_title or "줌수업" in notice_title or "주소" in notice_title):
                elem = browser.find_element_by_xpath(tr_content)
                browser.execute_script("arguments[0].scrollIntoView(true);", elem)
                browser.find_element_by_xpath(tr_content).click()

                time.sleep(1)
                # 공지사항 내용 content에 저장
                content = browser.find_element_by_xpath(
                    "/html/body/section/div[2]/div/div[2]/div[2]/div[3]/div/div").text
                # back 할 경우 과목 목록이 첫번째목록 (선형대수)로 지정.
                browser.back()
                # 다시 과목 목록 선택
                # subject_index 는 기존의 과목 목록을 불러오기 위한 index 지역변수
                subject_url = sub + str(subject_index) + ject
                subject = browser.find_element_by_xpath(subject_url).text
                browser.find_element_by_xpath(subject_url).click()
                time.sleep(1)
                with open("notice_content.txt", "w", encoding='utf-8') as f:
                    f.write(content)
                f.close()

                with open("notice_content.txt", "r", encoding='utf-8') as f:
                    for line in f:
                        line = line.rstrip("\n")
                        if (line == "Zoom 회의 참가" or line == "미팅 정보" or "* zoom 수업" in line):
                            link = f.readline().rstrip("\n")
                            zoom_link[subject] = link
                            count = 1
                            break
                        elif ("미팅 링크" in line):
                            zoom_link[subject] = line[6:]
                            count = 1
                        else:
                            continue

                if (count == 1):
                    break

    print(zoom_link)

    open("zoomlink.txt", "w", encoding='utf-8')

    for i in zoom_link.items():
        with open("zoomlink.txt", "a", encoding='utf-8') as f:
            f.write(str(i))
            f.write("\n")

def checkId():
    try:
        with open("secret.txt", "r") as f:
            loginId = f.readline()
            loginPwd = f.readline()
            # id 검사 -> 학번이 10자이고 숫자로 구성되어 있는지 확인
            studentNumCheck = re.compile(r'\d{10}')
            findId = studentNumCheck.search(loginId)
            if len(findId.group()) != 10:
                return False
    except Exception as error:
        print(error)
        return False
    return True
