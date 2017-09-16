# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import Http404
from django.template import loader
from django.views import generic
import models


def index(request):
    return render(request, 'index.html')

def output(request):
    res = models.search(request.GET['text'])
    context = {
        'people': res,
    }
    return render(request, 'result.html', context)

def detail(request, people_id):
    res = models.search_id(people_id)
    context = {
        'people': res,
    }
    return render(request, 'detail.html', context)
