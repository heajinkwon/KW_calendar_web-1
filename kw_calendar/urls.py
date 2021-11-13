from django.urls import path

from kw_calendar import views


# localhost:8000/kw  url 이후의 주소를 설정하여 페이지를 생성할 수 있습니다.
urlpatterns = [
    path("calendar/", views.calendar),
    path("test/", views.test),
    path("", views.index),
    path("goToUrl", views.goToPage),
    path("zoom_link/", views.zoom_link),
    path("major_site/", views.major_site),
    path("login/", views.login),
    path("evaluation/", views.evaluation),
    path("alarm/", views.alarm),

]
