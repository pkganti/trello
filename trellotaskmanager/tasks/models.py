# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from profiles.models import Profile

# Create your models here.

class Team(models.Model):
    name = models.CharField(max_length=200, null=False)
    members = models.ManyToManyField(Profile, related_name='profiles')

    def __str__(self):
        return "%s"%(self.name)

class BoardManager(models.Manager):
    def get_all_active_boards(self):
        active_boards = self.filter(is_active=True)
        return active_boards

class Board(models.Model):
    PRORITY_CHOICES = (
        ('HI', 'High'),
        ('LO', 'Low'),
        ('ME', 'Medium'),
    )
    name = models.CharField(max_length=200, null=False)
    priority = models.CharField(
        max_length = 2,
        choices = PRORITY_CHOICES,
        default = 'LO',
    )
    team = models.ForeignKey('Team', blank=True, null=True, related_name='boards')
    is_active = models.BooleanField(default=True)

    objects = BoardManager()

    def __str__(self):
        return "%s"%(self.name)

class ListManager(models.Manager):
    def get_all_active_lists(self):
        active_lists = self.filter(is_active=True)
        return active_lists

class List(models.Model):
    name = models.CharField(max_length=200, null=False)
    board = models.ForeignKey('Board', blank=True, null=True, related_name='lists')
    is_active = models.BooleanField(default=True)

    objects = ListManager()

    def __str__(self):
        return "%s"%(self.name)

class CardManager(models.Manager):
    def get_all_active_cards(self):
        active_cards = self.filter(is_active=True)
        return active_cards

class Card(models.Model):
    title = models.CharField(max_length=200, null=False)
    due_date = models.DateField(auto_now_add=True)
    created_by = models.ForeignKey('profiles.Profile', blank=True, null=True, related_name='cards')
    list = models.ForeignKey('List', blank=True, null=True, related_name='cards')
    is_active = models.BooleanField(default=True)

    objects = CardManager()

    def __str__(self):
        return "%s"%(self.title)
