# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

import MySQLdb

from pymongo import MongoClient

import re

# Create your models here

def search_id(people_id):
    client = MongoClient('localhost', 27017)
    db = client.wiki
    collection = db.people
    res = collection.find_one({'id': int(people_id)})
    return res

def extractCursor(cursor):
    res = []
    for people in cursor:
        res.append(people)
    return res

def AndWithHighlight(a, b):
    number = dict()
    for p in a:
        number[p['id']] = p['text']
    res = []
    for p in b:
        if (p['id'] in number):
            res.append(p)
            res[len(res) - 1]['text'] = number[p['id']] + res[len(res) - 1]['text']
    return res

def And(a, b):
    number = dict()
    for p in a:
        number[p['id']] = True
    res = []
    for p in b:
        if (p['id'] in number):
            res.append(p)
    return res

def Or(a, b):
    number = dict()
    res = []
    for p in a:
        number[p['id']] = True
        res.append(p)
    for p in b:
        if not (p['id'] in number):
            res.append(p)
    return res


def Match(text, title):
    client = MongoClient('localhost', 27017)
    db = client.wiki
    collection = db.people

    res = []

    for t in text.split(' '):
        if (len(t) < 3):
            continue
        re_text = re.compile('^.*%s.*$' % t, re.IGNORECASE)
        re_title = re.compile('^.*%s.*$' % title, re.IGNORECASE)
        anything = re.compile('^.*$', re.IGNORECASE)
        if (title == ""):
            cursor0 = collection.find({'row': {'$elemMatch': {'0': re_text}}})
            cursor1 = collection.find({'row': {'$elemMatch': {'1': re_text}}})
            ap = highlight(Or(extractCursor(cursor0), extractCursor(cursor1)), t)
            res = ap if (res == []) else AndWithHighlight(res, ap)
        else:
            cursor = collection.find({'row': {'$elemMatch': {'0': re_title, '1': re_text}}})
            ap = highlight(extractCursor(cursor), t)
            res = ap if (res == []) else AndWithHighlight(res, ap)

    return res



def highlight(allpeople, text):

    res = []


    for people in allpeople:
        es = ""
        s = ""

        for row in people['row']:
            if (row[0] == ""):
                s = s + " ¶"  + row[1] + "¶  "
            elif (row[1] == ""):
                s = s + " ¶"  + row[0] + "¶  "
            else:
                s = s + " ¶" + row[0] + " : " + row[1] + "¶  "

        numlimit = 4
        for i in xrange(len(text), len(s)):
            if (s[i - len(text) : i].lower() == text.lower()):
                l = i - len(text)
                r = i
                tot = 1
                lenlimit = 64
                while (l > 0 and tot > 0 ):
                    if (s[l] == '¶' and s[l + 1] != '¶'):
                        tot = tot - 1
                    l = l - 1
                    lenlimit = lenlimit - 1
                    if (lenlimit <= 0 and s[l] == ' '):
                        break

                tot = 1
                lenlimit = 64
                while (r < len(s) and tot > 0):
                    if (s[r] == '¶' and s[r - 1] != '¶'):
                        tot = tot - 1
                    r = r + 1
                    lenlimit = lenlimit - 1
                    if (lenlimit <= 0 and s[r] == ' '):
                        break

                l = l + 2
                r = r - 1

                es = es + s[l : i - len(text)] + "<span class='highlight'>" + s[i - len(text): i] + "</span>" + s[i : r] + "   ... <br>  "
                es = re.sub("<br>", "  ", es)
                numlimit = numlimit - 1
                if (numlimit == 0):
                    break


        res.append({
            'id': people['id'],
            'name': people['name'],
            'image': people['image'],
            'text': es,
        })

    return res





def search(text):
    bracket = re.compile('\[.*\]', re.IGNORECASE)
    got = bracket.search(text)
    res = []
    if (got != None):
        limits = got.group().split(' ')
        for limit in limits:
            title = limit[1:-1].split(':')[0]
            info = limit[1:-1].split(':')[1]
            res = Match(info, title) if (res == []) else And(res, Match(info, title))
    text = re.sub(bracket, "", text)
    if (text == ""):
        res = []
    else:
        res = Match(text, "") if (res == []) else And(res, Match(text, ""))
    return res



class People(models.Model):
    name = models.CharField(max_length = 100)
    title = models.CharField(max_length = 4096)
    information = models.TextField(max_length = 65536)
    infotext = models.TextField(max_length = 65536)
    imageurl = models.CharField(max_length = 1024, default = '')


    def __str__(self):
        return self.name
