# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import pdb
from django.conf import settings
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

from rest_framework.permissions import IsAuthenticated
from rest_framework import generics

from .serializers import TeamSerializer, BoardSerializer, ListSerializer, CardSerializer
from .models import Team, Board, List, Card
from profiles.models import Profile
from profiles.forms import SignUpForm


class IsAuthenticatedUser(IsAuthenticated):
    def has_permission(self, request, view):
        if not request.user.is_authenticated():
            return False
        return True

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

class LoginView(View):
    def get(self, request):
        # Code block for GET request
        c = {}
        return render(request, 'login.html', c)

    def post(self, request):
        # Code block for POST request
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

class HomeView(View):
    def get(self, request):
        c = {}
        return render(request, 'user_home.html', c)

class LogoutView(View):
    def get(self, request):
        logout(request)
        return render(request, 'login.html')

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


#This will only return the teams which the user logged in is member of because of Permission Classes
class TeamList(generics.ListCreateAPIView):
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

class TeamDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    permission_classes = (IsAuthenticatedUser, IsAuthorizedTeamMember,)

class BoardList(generics.ListCreateAPIView):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer

class BoardDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer

class ListList(generics.ListCreateAPIView):
    queryset = List.objects.all()
    serializer_class = ListSerializer

class ListDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = List.objects.all()
    serializer_class = ListSerializer

class CardList(generics.ListCreateAPIView):
    queryset = Card.objects.all()
    serializer_class = CardSerializer

class CardDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Card.objects.all()
    serializer_class = CardSerializer
