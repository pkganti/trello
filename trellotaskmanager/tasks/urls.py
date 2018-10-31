from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth.views import login
from .views import TeamList, TeamDetail, BoardList, BoardDetail, ListList, ListDetail, CardList, CardDetail, LoginView, HomeView, LogoutView, RegistrationView

urlpatterns = [

     # Home page URL, Login URL
     url(r'^$', LoginView.as_view(), name="login-home"),
     url(r'^home/$', HomeView.as_view(), name="user-home"),
     url(r'^logout/$', LogoutView.as_view(), name="user-logout"),

     url(r'^signup/$', RegistrationView.as_view(), name="user-registration"),

     # API URL's for Trello
     url(r'^teams/', TeamList.as_view(), name="teams-all"),
     url(r'^team/(?P<pk>\d+)/', TeamDetail.as_view(), name="team-detail"),
     url(r'^boards/', BoardList.as_view(), name="boards-all"),
     url(r'^board/(?P<pk>\d+)/', BoardDetail.as_view(), name="board-detail"),
     url(r'^lists/', ListList.as_view(), name="lists-all"),
     url(r'^list/(?P<pk>\d+)/', ListDetail.as_view(), name="list-detail"),
     url(r'^cards/', CardList.as_view(), name="cards-all"),
     url(r'^card/(?P<pk>\d+)/', CardDetail.as_view(), name="card-detail"),
]
