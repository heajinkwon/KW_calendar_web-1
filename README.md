# KW_calendar_web

설치 및 사용 방법
---
해당 프로젝트를 사용하기 위해서는 필수적으로 깔아야하는 프로그램들이 있습니다.
<p>
1. 프로젝트를 원하는 경로에 clone 해주세요. 아래의 명령어를 사용하시면 됩니다. <br>

```
	git clone https://github.com/Tianea2160/KW_calendar_web.git
```
<br>
2. 아래의 명령어를 cmd 또는 anaconda(임의의 가상환경) cmd 창에서 실행해주세요(기본적으로 파이썬 3.9 버전이 설치되어 있다는 가정하에 진행됩니다.)

```
	pip install -r requirements.txt
```

<br>
저희 프로젝트는 크롬으로 웹 스크랩핑을 진행합니다.<br> 
따라서 웹 스크랩핑에 필요한 프로그램도 설치해야합니다.
<p>

<br>
3. 설정에서 크롬 버전을 확인하세요<br>

```
	ex)버전 94.0.4606.61
```

<br>
4. 아래의 사이트에 들어가셔서 2.에서 확인한 버전에 맞는 크롬 드라이버를 다운받아주세요

```
	https://chromedriver.chromium.org/downloads
```

<br>
5. 4.에서 다운 받은 .exe 파일을 clone한 프로젝트 폴더에 넣어주세요.경로는 manage.py파일이 있는 곳입니다.<br>
<br>

파일 다운로드에 관한 모든 준비가 끝났습니다.

<br>
6. 다음 두 명령어를 프로젝트 경로 순서대로 입력하면 서버가 실행됩니다.<br>

```
	python manage.py migrate
```
```
	python manage.py runserver
```

<br>
크롬에서 

```
	http://localhost:8000/kw
```
위의 주소를 붙여넣기하면 정상적으로 실행됩니다.

해당 프로젝트에 기여하는 방법
---

해당 저장소 폴더의 kw_calendar아래에 veiw.py, template에 각각 controller와 웹에 출력되는 html 파일들이 모여있습니다.
각각의 파일또는 폴더가 있는데 template에는 사용자에게 보이는 웹의 모습인 html을 만들면 되고, view.py에서는 html로 넘길 정보를 코드로 작성하시면 됩니다.
	
프로젝트 시현 동영상
---
(동영상이 제작 완료 되면 링크를 올리도록 하겠습니다.)

사용한 오픈 소스 프로젝트 주소
---
<p>
1. fullcalendar(MIT license)

```
	https://github.com/fullcalendar/fullcalendar.git
```
</p>

<p>
2. selenium(language: python, Apache License)

```
	https://www.selenium.dev/
```
```
	https://github.com/SeleniumHQ/selenium
```
</p>
