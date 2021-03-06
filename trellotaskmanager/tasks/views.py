# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import pdb
from django.conf import settings
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics

from .serializers import TeamSerializer, BoardSerializer, ListSerializer, CardSerializer
from .models import Team, Board, List, Card
from profiles.models import Profile
from profiles.forms import SignUpForm

# This permission class is for checking whether the user is authenticated
class IsAuthenticatedUser(IsAuthenticated):
    def has_permission(self, request, view):
        if not request.user.is_authenticated():
            return False
        return True

# This permission class is to check whether the user is a member of Team
class IsAuthorizedTeamMember(IsAuthenticated):
    def has_permission(self, request, view):
        if request.method == 'GET':
            return True
        else:
            user = request.user
            user_profile = Profile.objects.get(user=user)
            team_id = request.path.split('/')[-2]
            team = Team.objects.get(id=int(team_id))

            if user_profile in team.members.all():
                return True
            else:
                return False
        return super(IsAuthorizedTeamMember, self).has_permission(request, view)

# To remove the csrf enforcement
class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return  # To not perform the csrf check previously happening

class LoginView(View):
    def get(self, request):
        c = {}
        return render(request, 'login.html', c)

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                # redirect the user to his home page
                login(request, user)
                return render(request, 'user_home.html')
            else:
                # User is present but inactive, throw an error message
                return HttpResponse("Inactive user.")
        else:
            # User is not present in the system, redirect to the login page
            return render(request, 'login.html')

        return render(request, 'login.html')

# The site home page
class HomeView(View):
    def get(self, request):
        c = {}
        return render(request, 'user_home.html', c)

# Logout page
class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('login-home')

class RegistrationView(View):
    def get(self, request):
        c = {}
        return render(request, 'user_register.html', c)

    def post(self, request):
        form = SignUpForm(request.POST)
        c = {}
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.save()
            profile = Profile.objects.get(user=user)
            profile.first_name = user.first_name
            profile.last_name = user.last_name
            profile.save()
            password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=password)
            login(request, user)
            return redirect('user-home')
            #return render(request, 'user_home.html', c)
        return render(request, 'user_register.html', c)

# Returns all the teams
class TeamList(generics.ListCreateAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer

#This will only return the teams which the user is member of because of Permission Classes
class UserTeamList(generics.ListCreateAPIView):
    def get_queryset(self):
        # Only the teams which the user is member of should be displayed on the home page
        user = self.request.user
        profile_user = Profile.objects.get(user=user)
        teams = Team.objects.all()
        user_teams = []
        for team in teams:
            if not profile_user in team.members.all():
                continue
            user_teams.append(team)
        return user_teams

    serializer_class = TeamSerializer
    permission_classes = (IsAuthenticatedUser,)

# Returns the details of a Team
class TeamDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    permission_classes = (IsAuthenticatedUser, IsAuthorizedTeamMember,)

    # This below code is to exempt csrf token
    authentication_classes = (CsrfExemptSessionAuthentication, )

# Returns all the boards
class BoardList(generics.ListCreateAPIView):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer

# This view is to fetch the boards of a particular team, Input is the Team ID
# Return all the boards of a team
class TeamBoardsList(generics.ListAPIView):
    def get_queryset(self):
        try:
            team_id = int(self.request.path.split('/')[-2])
            team = Team.objects.get(id=team_id)
            return Board.objects.filter(team=team)
        except:
            return Board.objects.all()

    serializer_class = BoardSerializer

# Returns details of a board
class BoardDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer

# Returns all the lists
class ListList(generics.ListCreateAPIView):
    queryset = List.objects.all()
    serializer_class = ListSerializer

# This is the view to list all the lists of a Board, Input is the Board ID
# Returns all the lists of a Board
class ListBoardLists(generics.ListAPIView):
    def get_queryset(self):
        try:
            board_id = int(self.request.path.split('/')[-2])
            board = Board.objects.get(id=board_id)
            return List.objects.filter(board=board)
        except:
            return List.objects.all()
    serializer_class = ListSerializer

# Returns the detail of a List
class ListDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = List.objects.all()
    serializer_class = ListSerializer

# Returns all the cards
class CardList(generics.ListCreateAPIView):
    queryset = Card.objects.all()
    serializer_class = CardSerializer

# This is the view to list all the cards of a List, Input is the List ID
# Returns all the cards of a List
class ListCardLists(generics.ListAPIView):
    def get_queryset(self):
        try:
            list_id = int(self.request.path.split('/')[-2])
            list = List.objects.get(id=list_id)
            return Card.objects.filter(list=list)
        except:
            return Card.objects.all()
    serializer_class = CardSerializer

# Returns the detail of a Card
class CardDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Card.objects.all()
    serializer_class = CardSerializer
