from selenium import webdriver
import time, re
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.support.select import Select

def major_find() :
    browser = webdriver.Chrome()

    with open("secret.txt", "r") as f:
        line = f.readline()
        loginId = line.split(':')[-1].replace('\n', '').strip()
        line = f.readline()
        loginPwd = line.split(':')[-1].replace('\n', '').strip()

    url = "https://klas.kw.ac.kr/usr/cmn/login/LoginForm.do"
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

    # 위 왼쪽 상단 메뉴버튼 누르기
    browser.find_element_by_xpath("/html/body/header/div[1]/div/div[1]/button").click()
    browser.implicitly_wait(delay)

    #  복수/심화전공 버튼 누르기
    button = browser.find_element_by_xpath("/html/body/header/div[2]/div/div/div[1]/ul/li[3]/ul/li[2]/a")
    button.click()

    major = browser.find_element_by_xpath("/html/body/main/div/div/div/table[1]/tbody/tr/td[2]").text
    with open("major.txt", "w", encoding='utf-8') as f:
        f.write(major)

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
