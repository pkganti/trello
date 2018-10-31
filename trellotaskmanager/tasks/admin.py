# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Team, Board, List, Card

# Register your models here.

admin.site.register(Team)
admin.site.register(Board)
admin.site.register(List)
admin.site.register(Card)
