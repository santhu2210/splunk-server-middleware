# Create your views here.

from django.conf import settings
from django.views import generic
from django.views.generic import View
from django.contrib.auth import authenticate, logout, get_user_model, login
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.http import Http404, HttpResponse, JsonResponse
from datetime import datetime, timedelta
from django.core.files.storage import default_storage

import os
import json

from django.core.mail import EmailMessage,send_mail
from clientapp.splunk_server_util import get_splunk_server_response

# Global declaration of operation folder
ROOT_FOLDER = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def Home_view(request):
    if request.method == 'POST':
        # return redirect('appserver:dashboard')
        # return render(request, 'home.html', {"user" : user})
        pass

    else:
        # GET, generate blank form
        return render(request, 'home.html', {"method": 'GET'})


def MakeRequest(request):
    if request.method == 'POST':
        try:
            # # POST, generate form with data from the request
            serverip = request.POST['serverip']
            username = request.POST['username']
            password = request.POST['passkey']
            keyword = request.POST['keyword']
            start_time_range = request.POST['eventday']
            email = request.POST['email']

            earliest_dt = ':'.join(start_time_range.split('   '))
            latest_dt = datetime.now().strftime("%m/%d/%Y:%H:%M:%S")

            print(serverip, username, password, keyword, email, earliest_dt, latest_dt)

            response_dict = get_splunk_server_response(serverip, username, password, keyword, earliest_dt, latest_dt)
            if response_dict['status']:
                mail_body_text = response_dict['searchqry_response']

                # email = EmailMessage('Test', 'Test', to=['sample_dev@gmail.com'])
                # email.send()

                # Send verification email
                send_mail(
                    'Splunk search results of query :' + keyword,
                    mail_body_text,
                    'msg2shanth@outlook.com',
                    [email],
                    fail_silently=False,
                )
                return render(request, 'home.html', {"method": 'POST', "status": "True", "eve_msg": "Search query responses sent to given Mail "})
            else:
                return render(request, 'home.html', {"method": 'POST', "status": "False", "eve_msg": "Problem in server, please check all fields. "})
        except Exception as e:
            print("Exception raise :", str(e))
            return render(request, 'home.html', {"method": 'POST', "status": "False", "eve_msg": "Problem in Processing, please check all fields. "})

    else:
        # GET, generate blank form
        return render(request, 'home.html')
