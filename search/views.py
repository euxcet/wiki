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
    page = 0
    if ('page' in request.GET):
        page = int(request.GET['page']) - 1


    plist = [(i + 1) for i in xrange(0, len(res) / 15 + ((len(res) % 15) > 0))]

    context = {
        'text': request.GET['text'],
        'people': res,
        'count': len(res),
        'page': page + 1,
        'pfrom': page * 15,
        'psize': len(res) / 15 + ((len(res) % 15) > 0),
        'pto': min(page * 15 + 15, len(res)),
        'plist': plist,
    }
    print context
    return render(request, 'result.html', context)

def detail(request, people_id):
    res = models.search_id(people_id)
    context = {
        'people': res,
    }
    return render(request, 'detail.html', context)
