from selenium import webdriver
import time
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.support.select import Select

def evaluation_find() :
    browser = webdriver.Chrome()
    evaluation_rate = {}
    count = 0
    delay = 0.5

    with open("secret.txt", "r") as f:
        line = f.readline()
        loginId = line.split(':')[-1].replace('\n', '').strip()
        line = f.readline()
        loginPwd = line.split(':')[-1].replace('\n', '').strip()

        # 학교 홈페이지 주소
        url = "https://klas.kw.ac.kr/std/lis/evltn/TaskStdPage.do"
        browser.get(url)

        # id 입력
        elem = browser.find_element_by_id("loginId")
        elem.clear()
        elem.send_keys(loginId)

        # pwd 입력
        elem = browser.find_element_by_id("loginPwd")
        elem.clear()
        elem.send_keys(loginPwd)

        # login 버튼 누르기
        browser.find_element_by_class_name("btn").click()
        time.sleep(2)
    # 과목수 불러오기
    elem = browser.find_element_by_class_name("col-md-7")
    elem = elem.find_element_by_class_name("form-control-sm")
    select = Select(elem)

    # 과목이름 넣기
    subject_list = []
    professor_list = []

    for i in select.options:
        # 교과목 담기
        subject = i.text
        index_1 = subject.find("(")
        subject_list.append(subject[:index_1 - 1])
        # 교수님 성함 담기
        professor = i.text
        index_2 = professor.find(")")
        professor = professor[index_2 + 1:]
        index_2 = professor.find("-")
        professor_list.append(professor[index_2 + 2:])

    # 왼쪽 상단 목록 이동
    browser.find_element_by_xpath("/html/body/header/div[1]/div/div[1]/button").click()
    time.sleep(delay)
    browser.find_element_by_xpath("/html/body/header/div[2]/div/div/div[1]/ul/li[1]/ul/li[3]/a").click()
    time.sleep(delay)

    for i in range(0, len(subject_list)):
        # 교과목 입력
        elem = browser.find_element_by_xpath(
            "/html/body/main/div/div/div/div[2]/div[2]/table[1]/tbody/tr[2]/td[1]/input")
        elem.clear()
        elem.send_keys(subject_list[i])

        # 교수님 성함 입력
        elem = browser.find_element_by_xpath(
            "/html/body/main/div/div/div/div[2]/div[2]/table[1]/tbody/tr[2]/td[2]/input")
        elem.clear()
        elem.send_keys(professor_list[i])

        # 인증코드 입력
        code = browser.find_element_by_xpath(
            "/html/body/main/div/div/div/div[2]/div[2]/table[1]/tbody/tr[5]/td/span").text
        elem = browser.find_element_by_xpath("/html/body/main/div/div/div/div[2]/div[2]/table[1]/tbody/tr[5]/td/input")
        elem.clear()
        elem.send_keys(code)

        # 조회버튼 클릭
        browser.find_element_by_xpath("/html/body/main/div/div/div/div[2]/div[2]/div/button").click()
        time.sleep(delay)

        # 해당 교과목 클릭
        sub_name = browser.find_element_by_xpath(
            "/html/body/main/div/div/div/div[2]/div[2]/table[2]/tbody/tr/td[2]").text
        error = 0
        error_index = sub_name.find("(미입력)")
        error_check = sub_name[error_index:]
        if ("(미입력)" in error_check):
            error = error + 1
        else:
            browser.find_element_by_xpath("/html/body/main/div/div/div/div[2]/div[2]/table[2]/tbody/tr/td[2]").click()

        time.sleep(2)

        # 학습평가비율 담을 딕셔너리 생성
        evaluation_rate[subject_list[i]] = ""

        # 학습평가비율 표 찾기
        if (error == 1):
            continue
        else:
            tbodys = browser.find_element_by_xpath("/html/body/main/div/div/div/div[2]/div[2]/table[2]/tbody")
            tr = tbodys.find_elements_by_tag_name("tr")

            for td in tr:
                row = td.text
                row = row.split("\n" or " ")
                row = " ".join(row)
                cut_index = row.find("기타평가")
                row = row[:cut_index]
                if ("평가방법 비율" in row):
                    rate = row[8:]

                # 이메일 표 찾기
            tbodys = browser.find_element_by_xpath("/html/body/main/div/div/div/div[2]/div[2]/table[1]/tbody")
            tr = tbodys.find_elements_by_tag_name("tr")

            for td in tr:
                row = td.text
                row = row.split("\n" or " ")
                row = " ".join(row)
                if ("이메일" in row):
                    email = row

            evaluation_rate[subject_list[i]] = rate + email

            browser.back()
            time.sleep(1)

    open("evaluation_rate.txt", "w", encoding='utf-8')
    for key, value in evaluation_rate.items():
        evaluation_items = str(value)[:31] + "\n"
        email_index = str(value).find("이메일")
        evaluation_percent = str(value)[32:email_index] + "\n"
        email_add = str(value)[email_index + 4:] + "\n"

        with open("evaluation_rate.txt", "a", encoding='utf-8') as f:
            f.write(str(key))
            f.write("\n")
            f.write(str(evaluation_items))
            f.write(str(evaluation_percent))
            f.write("이메일")
            f.write("\n")
            f.write(str(email_add))

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