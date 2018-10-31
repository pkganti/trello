from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth.views import login
from .views import *

urlpatterns = [

     # Home page URL, Login URL
     url(r'^$', LoginView.as_view(), name="login-home"),
     url(r'^home/$', HomeView.as_view(), name="user-home"),
     url(r'^logout/$', LogoutView.as_view(), name="user-logout"),
     url(r'^signup/$', RegistrationView.as_view(), name="user-registration"),

     # Teams API URL's
     url(r'^teams/$', TeamList.as_view(), name="teams-all"),
     url(r'^team/(?P<pk>\d+)/$', TeamDetail.as_view(), name="team-detail"),
     url(r'^user/teams/$', UserTeamList.as_view(), name="user-teams-all"),

     # Board API URL's
     url(r'^boards/$', BoardList.as_view(), name="boards-all"),
     url(r'^boards/team/(?P<pk>\d+)/$', TeamBoardsList.as_view(), name="team-board-list"),
     url(r'^board/(?P<pk>\d+)/$', BoardDetail.as_view(), name="board-detail"),

     # Lists API URL's
     url(r'^lists/$', ListList.as_view(), name="lists-all"),
     url(r'^lists/board/(?P<pk>\d+)/$', ListBoardLists.as_view(), name="board-lists-list"),
     url(r'^list/(?P<pk>\d+)/$', ListDetail.as_view(), name="list-detail"),

     # Cards API URL's
     url(r'^cards/$', CardList.as_view(), name="cards-all"),
     url(r'^cards/list/(?P<pk>\d+)/$', ListCardLists.as_view(), name="list-cards-list"),
     url(r'^card/(?P<pk>\d+)/$', CardDetail.as_view(), name="card-detail"),
]
