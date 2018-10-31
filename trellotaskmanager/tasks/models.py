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

    def __str__(self):
        return "%s"%(self.name)

class List(models.Model):
    name = models.CharField(max_length=200, null=False)
    board = models.ForeignKey('Board', blank=True, null=True, related_name='lists')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return "%s"%(self.name)

class Card(models.Model):
    title = models.CharField(max_length=200, null=False)
    due_date = models.DateField(auto_now_add=True)
    created_by = models.ForeignKey('profiles.Profile', blank=True, null=True, related_name='cards')
    list = models.ForeignKey('List', blank=True, null=True, related_name='cards')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return "%s"%(self.title)
