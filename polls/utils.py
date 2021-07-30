from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.views.generic import ListView, CreateView, UpdateView
from django.urls import reverse_lazy
from .models import *
from .forms import CreateUserForm
from django.contrib.auth.forms import UserCreationForm
from distutils.util import strtobool
from django.contrib.auth.models import User
from django.contrib import messages
import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import pandas as pd
from verify_email.email_handler import send_verification_email # pip install Django-Verify-Email
from django.core import mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib.auth import get_user_model
from core.functions import DistanceH, mainFunction

def dataHome(request, user_id):
    distance_df = mainFunction()
    parSub = parentSubject.objects.values()
    df_parsub = pd.DataFrame(parSub)
    parent_subjects = df_parsub['parsub'].to_list()
    # subject
    subjects = distance_df.mainfunctiondf(user_id)[1]['name_sub'].to_list()
     
    # area interesse
    ai = AreaInteresse.objects.values()
    df_ai = pd.DataFrame(ai)
    areaint = df_ai['name_ai'].to_list()

    dettagli = distance_df.mainfunctiondf(user_id)[2]['det_ai'].to_list()
    
    if userData.objects.filter(user=request.user).exists():
        checkLatLong = userData.objects.filter(user=request.user).values()
        df_latLong = pd.DataFrame(checkLatLong)
        if df_latLong['lat'].values != "":
            json_records = distance_df.mainfunctiondf(user_id)[0].reset_index().to_json(orient ='records')
            data = []
            data = json.loads(json_records)
            context = {'d': data}
        else:
            context = {}
        
        dizionario = {
            'mainDF': context, 
            'Sub': subjects, 
            'ParSub': parent_subjects,
            'DetAI': dettagli,
            'AI': areaint
        }
        
    else:
        dizionario = {
            'Sub': subjects, 
            'ParSub': parent_subjects,
            'DetAI': dettagli,
            'AI': areaint
        }
    
    return dizionario

