from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render,render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.contrib import auth
import requests
import MySQLdb
import json

from django.http import Http404
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from django.core import serializers
from django.conf import settings


class users:
    u_id = ''
    name = ''
    username = ''
    subject = ''
    dept = ''
    password = ''
    role = ''

    data = {
        'id': u_id,
        'name': name,
        'username': username,
        'subject': subject,
        'dept': dept,
        'password': password,
        'role': role
    }



db = MySQLdb.connect(host="localhost", user="root", passwd="12345678", db="Achyuth")
cursor = db.cursor()

@csrf_exempt

def check_login(request):

    dict2 = {
        "status": "failed"
    }

    username = request.POST.get('username', '')
    password = request.POST.get('password', '')


    user = users()
    print ("before fetch")
    print (request.POST)
    print (request.GET)
    print (username)
    print (password)
    cursor.execute("select * from users where username='%s' and password='%s'" % (username,password))

    data = cursor.fetchone()
    print ("After fetch")
    print (data)

    if data:
        """user.username = data[0]
        user.name = data[1]
        user.u_id = data[2]
        user.subject = data[3]
        user.role = data[4]
        user.dept = data[5]
        user.password = data[6]

        data1 = {
            'username': user.username,
            'name': user.name,
            'id': user.u_id,
            'subject': user.subject,
            'role': user.role,
            'dept': user.dept,
        }"""
        dict1 = {
            "ID": data[0],
            "username": data[1],
            "status": "success"
        }

        return HttpResponse(json.dumps(dict1))

        #return HttpResponse("<h1> You are here</h1>")
    else:
        return HttpResponse(json.dumps(dict2))

@csrf_exempt

def check_register(request):
    user = users()
    user.name = request.POST.get('Name', '')
    user.u_id = request.POST.get('Id', '')
    user.subject = request.POST.get('Subject', '')
    user.role = request.POST.get('Role', '')
    user.dept = request.POST.get('Dept', '')
    user.username = request.POST.get('Uname_Email', '')
    user.password = request.POST.get('Password', '')
    user.cpassqord = request.POST.get('Confirm', '')

    if user.password != user.cpassqord:
        return HttpResponse("<h1> Not Success </h1>")
    else:
        try:
            cursor.execute("insert into users(username,name,id,subject,role,dept,password) values('%s','%s','%s','%s','%s','%s','%s')" % (user.username, user.name, user.u_id, user.subject, user.role, user.dept, user.password))
            db.commit()
            return render(request, "dashboard.html", {"hello":"hii"})
        except:
            return HttpResponse("<h1> User Not Created")
