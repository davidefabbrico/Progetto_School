
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
from core.functions import DistanceH, mainFunction, Results
from django.http import HttpResponse, Http404
import os
# from django_email_verification import send_email

# subject = 'Subject'
# html_message = render_to_string('mail_template.html', {'context': 'values'})
# plain_message = strip_tags(html_message)
# from_email = 'From <from@example.com>'
# to = 'to@example.com'


'''Set the view https://simpleisbetterthancomplex.com/tutorial/2018/01/29/how-to-implement-dependent-or-chained-dropdown-list-with-django.html'''

def loginPage(request):
    if request.user.is_authenticated:
        return redirect('/home/')
        
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('/home/')
        else:
            messages.info(request, 'Username o password non corretti')
            
    context = {}
    return render(request, 'polls/login.html', context)

def logoutUser(request):
    logout(request)
    return redirect('login')

def registrationPage(request):
    form = CreateUserForm()
    
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        email_user = request.POST.get('email')
        users_email = User.objects.filter(email=email_user).exists()
        email_exist = False
        if form.is_valid():
            if users_email:
                messages.error(request, "Email già esistente!")
                return redirect('login')
            else:
                form.save()
                inactive_user = send_verification_email(request, form)
                user = form.cleaned_data['username']
                messages.success(request, 'Account creato correttamente per ' + user + '.' + "\n Controlla la tua email per la verifica.")
                return redirect('login')
            
    context = {'form': form} # 'email_already_exist':email_exist
    return render(request, 'polls/register.html', context)

@login_required(login_url='login')
def homepage(request):
    user_id = request.user.id
    distance_df = mainFunction()

    if userData.objects.filter(user=request.user).exists():
        checkLatLong = userData.objects.filter(user=request.user.id).values()
        df_latLong = pd.DataFrame(checkLatLong)
        if df_latLong['lat'].values != "":
            json_records = distance_df.mainfunctiondf(user_id)[0].reset_index().to_json(orient ='records')
            data = []
            data = json.loads(json_records)
            context = {'d': data}
            lunghDF = len(context['d'])
        else:
            context = {}
            lunghDF = len(context['d'])
        
        dizionario = {
            'lunghDF':lunghDF,
        }
    else:
        dizionario = {}

    return render(request,'polls/home.html', dizionario)


@login_required(login_url='login')
def GeouserData(request):
    action = request.POST.get('action')
    lat = request.POST.get('lat')
    lon = request.POST.get('lon')
    if action == 'save_position':
        if userData.objects.filter(user=request.user).exists():
            obj = userData.objects.get(user=request.user)
            obj.lat = lat
            obj.longi = lon
            obj.save()
        else:
            userData.objects.create(user=request.user, longi=lon, lat=lat)
    
    data = {
        'parit_choice':None,
        'choice_distance':None,
        'durata':None,
        'crecupero':None,
        'extracurr':None,
        'bStudio':None,
        'stage':None,
        'certificazioni':None,
        'tutOrient':None,
    }

    if action == "save_par":
        if request.method == 'POST':
            if request.POST["choice_par"] == 'Statale':
                par = 'S'
                if userData.objects.filter(user=request.user).exists():
                    obj = userData.objects.get(user=request.user)
                    obj.parit_choice = par
                    obj.save()
                else:
                    userData.objects.create(user=request.user, parit_choice=par)
            else:
                par = 'NS'
                if userData.objects.filter(user=request.user).exists():
                    obj = userData.objects.get(user=request.user)
                    obj.parit_choice = par
                    obj.save()
                else:
                    userData.objects.create(user=request.user, parit_choice=par)
        
        data['parit_choice'] = par
        
    if action == "save_dist":
        if request.method == 'POST':
            if request.POST["choice_dist"] == '10':
                dist = 10
                if userData.objects.filter(user=request.user).exists():
                    obj = userData.objects.get(user=request.user)
                    obj.choice_distance = 10
                    obj.save()
                else:
                    userData.objects.create(user=request.user, distance=dist)
            if request.POST["choice_dist"] == '20':
                dist = 20
                if userData.objects.filter(user=request.user).exists():
                    obj = userData.objects.get(user=request.user)
                    obj.choice_distance = dist
                    obj.save()
                else:
                    userData.objects.create(user=request.user, choice_distance=dist)
            elif request.POST["choice_dist"] == '30':
                dist = 30
                if userData.objects.filter(user=request.user).exists():
                    obj = userData.objects.get(user=request.user)
                    obj.choice_distance = dist
                    obj.save()
                else:
                    userData.objects.create(user=request.user, choice_distance=dist)
            elif request.POST["choice_dist"] == '40':
                dist = 2000
                if userData.objects.filter(user=request.user).exists():
                    obj = userData.objects.get(user=request.user)
                    obj.choice_distance = dist
                    obj.save()
                else:
                    userData.objects.create(user=request.user, choice_distance=dist)
                
                    
        data['choice_distance'] = dist
        

    # durata
    if action == "save_dur":
        if request.method == 'POST':
            user_year = request.POST.get("choice_dur", 1)
            y = yearsSchool.objects.get(year=user_year)
            if request.POST['check_dur'] == 'true':
                if userData.objects.filter(user=request.user).exists():
                    obj = userData.objects.get(user=request.user)
                    obj.durata.add(y)
                    obj.save()
                else:
                    userData.objects.create(user=request.user, durata=user_year)
            else:
                if userData.objects.filter(user=request.user).exists():
                    obj = userData.objects.get(user=request.user)
                    obj.durata.remove(y)
                    obj.save()
                else:
                    userData.objects.create(user=request.user, durata=False)

        data['durata'] = user_year
    
    # boolean values 
    # corsi di approfondimento / recupero

    if action == "save_appr":
        if request.method == 'POST':
            if request.POST["choice_appr"] == 'true':
                if userData.objects.filter(user=request.user).exists():
                    obj = userData.objects.get(user=request.user)
                    obj.crecupero = True
                    obj.save()
                else:
                    userData.objects.create(user=request.user, crecupero=True)
            elif request.POST["choice_appr"] == 'false':
                if userData.objects.filter(user=request.user).exists():
                    obj = userData.objects.get(user=request.user)
                    obj.crecupero = False
                    obj.save()
                else:
                    userData.objects.create(user=request.user, crecupero=False)

    
        data['crecupero'] = True


    if action == "save_att":
        if request.method == 'POST':
            if request.POST["choice_att"] == 'true':
                if userData.objects.filter(user=request.user).exists():
                    obj = userData.objects.get(user=request.user)
                    obj.extracurr = True
                    obj.save()
                else:
                    userData.objects.create(user=request.user, extracurr=True)
            
            else:
                if userData.objects.filter(user=request.user).exists():
                    obj = userData.objects.get(user=request.user)
                    obj.extracurr = False
                    obj.save()
                else:
                    userData.objects.create(user=request.user, extracurr=False)
        data['extracurr'] = True


    # if action == "":
    #     if request.method == 'POST':
    #         boole = strtobool(request.POST.get('asda',False))
    #         if userData.objects.filter(user=request.user).exists():
    #             obj = userData.objects.get(user=request.user)
    #             getattr(obj, request.POST.get('dbkey'))
    #             obj.extracurr = boole
    #             obj.objects.filter().update(dbkey=bool)
    #         else:
    #             userData.objects.create(user=request.user, extracurr=boole)
    #     data['extracurr'] = True


    if action == "save_bor":
        if request.method == 'POST':
            if request.POST["choice_bor"] == 'true':
                if userData.objects.filter(user=request.user).exists():
                    obj = userData.objects.get(user=request.user)
                    obj.bStudio = True
                    obj.save()
                else:
                    userData.objects.create(user=request.user, bStudio=True)
        
            elif request.POST["choice_bor"] == 'false':
                    if userData.objects.filter(user=request.user).exists():
                        obj = userData.objects.get(user=request.user)
                        obj.bStudio = False
                        obj.save()
                    else:
                        userData.objects.create(user=request.user, bStudio=False)

        data['bStudio'] = True

    if action == "save_stage":
        if request.method == 'POST':
            if request.POST["choice_stage"] == 'true':
                if userData.objects.filter(user=request.user).exists():
                    obj = userData.objects.get(user=request.user)
                    obj.stage = True
                    obj.save()
                else:
                    userData.objects.create(user=request.user, stage=True)
            
            else:
                    if userData.objects.filter(user=request.user).exists():
                        obj = userData.objects.get(user=request.user)
                        obj.stage = False
                        obj.save()
                    else:
                        userData.objects.create(user=request.user, stage=False)
        
        data['stage'] = True

    if action == "save_cert":
        if request.method == 'POST':
            if request.POST["choice_cert"] == 'true':
                if userData.objects.filter(user=request.user).exists():
                    obj = userData.objects.get(user=request.user)
                    obj.certificazioni = True
                    obj.save()
                else:
                    userData.objects.create(user=request.user, certificazioni=True)
            
            else:
                if userData.objects.filter(user=request.user).exists():
                    obj = userData.objects.get(user=request.user)
                    obj.certificazioni = False
                    obj.save()
                else:
                    userData.objects.create(user=request.user, certificazioni=False)
        
        data['certificazioni'] = True

    if action == "save_tut":
        if request.method == 'POST':
            if request.POST["choice_tut"] == 'true':
                if userData.objects.filter(user=request.user).exists():
                    obj = userData.objects.get(user=request.user)
                    obj.tutOrient = True
                    obj.save()
                else:
                    userData.objects.create(user=request.user, tutOrient=True)
            else:
                if userData.objects.filter(user=request.user).exists():
                    obj = userData.objects.get(user=request.user)
                    obj.tutOrient = False
                    obj.save()
                else:
                    userData.objects.create(user=request.user, tutOrient=False)
        
        data['tutOrient'] = True
        
        
    # subject
    if action == "save_sub":
        if request.method == 'POST':
            user_sub = request.POST.get("choice_sub", 1)
            subj = Subject.objects.get(name_sub=user_sub)
            if request.POST["check_sub"] == 'true':
                if userData.objects.filter(user=request.user).exists():
                    obj = userData.objects.get(user=request.user)
                    obj.sub.add(subj)
                    obj.save()
                else:
                    userData.objects.create(user=request.user, sub=user_sub)
            else:
                if userData.objects.filter(user=request.user).exists():
                    obj = userData.objects.get(user=request.user)
                    obj.sub.remove(subj)
                    obj.save()
                else:
                    userData.objects.create(user=request.user, sub=False)
                

        data['subject'] = user_sub
        
    
    # par subject
    if action == "save_parsub":
        if request.method == 'POST':
            user_parsub = request.POST.get("choice_parsub", 1)
            parsubj = parentSubject.objects.get(parsub=user_parsub)
            if request.POST["check_parsub"] == 'true':
                if userData.objects.filter(user=request.user).exists():
                    obj = userData.objects.get(user=request.user)
                    obj.parsub.add(parsubj)
                    obj.save()
                else:
                    userData.objects.create(user=request.user, parsub=user_parsub)
            else:
                if userData.objects.filter(user=request.user).exists():
                    obj = userData.objects.get(user=request.user)
                    obj.parsub.remove(parsubj)
                    obj.save()
                else:
                    userData.objects.create(user=request.user, parsub=False)
                

        data['parentsubject'] = user_parsub
        
    # ai
    if action == "save_ai":
        if request.method == 'POST':
            user_ai = request.POST.get("choice_ai", 1)
            ai = AreaInteresse.objects.get(name_ai=user_ai)
            if request.POST["check_ai"] == 'true':
                if userData.objects.filter(user=request.user).exists():
                    obj = userData.objects.get(user=request.user)
                    obj.areaint.add(ai)
                    obj.save()
                else:
                    userData.objects.create(user=request.user, areaint=user_ai)
            else:
                if userData.objects.filter(user=request.user).exists():
                    obj = userData.objects.get(user=request.user)
                    obj.areaint.remove(ai)
                    obj.save()
                else:
                    userData.objects.create(user=request.user, areaint=False)
                

        data['area_interesse'] = user_ai
        
    
    # dettagli area interesse
    if action == "save_detai":
        if request.method == 'POST':
            user_detai = request.POST.get("choice_detai", 1)
            detai = DettagliAreaInteresse.objects.get(det_ai=user_detai)
            if request.POST["check_detai"] == 'true':
                if userData.objects.filter(user=request.user).exists():
                    obj = userData.objects.get(user=request.user)
                    obj.dettagli_area_interesse.add(detai)
                    obj.save()
                else:
                    userData.objects.create(user=request.user, dettagli_area_interesse=user_detai)
            else:
                if userData.objects.filter(user=request.user).exists():
                    obj = userData.objects.get(user=request.user)
                    obj.dettagli_area_interesse.remove(detai)
                    obj.save()
                else:
                    userData.objects.create(user=request.user, parsub=False)
                

        data['dettagli_area_interesse'] = user_detai
        
    if action == "save_reset":
        if request.method == 'POST':
            if userData.objects.filter(user=request.user).exists():
                obj = userData.objects.get(user=request.user)
                obj.tutOrient = False
                obj.certificazioni = False
                obj.stage = False
                obj.bStudio = False
                obj.extracurr = False
                obj.durata.set([])
                obj.crecupero = False
                obj.choice_distance = 0
                obj.parit_choice = 0
                obj.sub.set([])
                obj.parsub.set([])
                obj.areaint.set([])
                obj.dettagli_area_interesse.set([])
                obj.save()

    return JsonResponse(data=data)


@login_required(login_url='login')
def filtered_data(request):
    user_id = request.user.id
    distance_df = mainFunction()

    parSub = parentSubject.objects.values()
    df_parsub = pd.DataFrame(parSub)
    parent_subjects = df_parsub['parsub'].to_list()
     
    # area interesse
    ai = AreaInteresse.objects.values()
    df_ai = pd.DataFrame(ai)
    areaint = df_ai['name_ai'].to_list()

    if userData.objects.filter(user=request.user).exists():
        # subject
        subjects = distance_df.mainfunctiondf(user_id)[1]['name_sub'].to_list()
        dettagli = distance_df.mainfunctiondf(user_id)[2]['det_ai'].to_list()
        checkLatLong = userData.objects.filter(user=request.user).values()
        df_latLong = pd.DataFrame(checkLatLong)
        if df_latLong['lat'].values != "":
            json_records = distance_df.mainfunctiondf(user_id)[0].reset_index().to_json(orient ='records')
            data = []
            data = json.loads(json_records)
            context = {'d': data}
        else:
            context = {}
        
        user_data = userData.objects.get(user=request.user)
        
        
        areaint_selected = user_data.areaint.values()
        sub_selected = user_data.sub.values()
        parsub_selected = user_data.parsub.values()
        detai_selected = user_data.dettagli_area_interesse.values()

        dizionario = {
            'mainDF': context, 
            'Sub': {
                'db':subjects,
                'selected': [],
            }, 
            'ParSub': {
                'db': parent_subjects,
                'selected': [],
            },
            'DetAI': {
                'db': dettagli,
                'selected': [],
            }, 
            'AI': {
                'db':areaint,
                'selected': []
            },
            'lunghDF': len(context['d'])
        }

        
        for selected_ai in areaint_selected:
            dizionario['AI']['selected'].append(selected_ai) 
        
        for selected_sub in sub_selected:
            dizionario['Sub']['selected'].append(selected_sub)
        
        for selected_parsub in parsub_selected:
            dizionario['ParSub']['selected'].append(selected_parsub)

        for selected_detai in detai_selected:
            dizionario['DetAI']['selected'].append(selected_detai)
        
    else:
        dizionario = {
        }

    context = {}
    context.update(dizionario)
    
    return JsonResponse(data=dizionario)

def inizio(request):
    return render(request,'polls/iniziale.html')

@login_required(login_url='login')
def feedback(request):
    if userDataFeedback.objects.filter(user=request.user).exists():
        return redirect('/risultati')
    return render(request,'polls/feedback.html')

def privacy(request):
    return render(request,'polls/privacy.html')


def error_404_view(request, exception):
    return render(request, 'polls/404.html')

def error_500_view(request):
    return render(request, 'polls/500.html')

def poke(request):
    return render(request, 'polls/poke.html')

@login_required(login_url='login')
def risultati(request):
    res = Results()
    context = res.result(request.user.id)
    return render(request, 'polls/risultati.html', context)



@login_required(login_url='login')
def get_all_questions_data(request):
    res = []
    questions = Question.objects.all()
    for question in questions:
        q = {}
        q = {
            'id': question.pk,
            'text': question.text,
            'answers': [], 
            'required': question.required,
        }
        for answer in question.answers.all():
            q['answers'].append({
                'id':answer.pk,
                'text':answer.text,
                'type': answer.type,
            })
        res.append(q)    

    return JsonResponse(data=res, safe=False)

@login_required(login_url='login')
def save_all_questions_data(request):
    res = []
    answers_json = request.POST.get('jsonData')
    json_ans = json.loads(answers_json) 
    df_ans = pd.DataFrame(json_ans)
    df_ansTrue = df_ans[df_ans['checked']==True].reset_index(drop=True)
    df_ansZero = df_ans[df_ans['id_answer']=='0'].reset_index(drop=True)
    df_merge = df_ansZero.append(df_ansTrue)
    df_merge = df_merge[df_merge['text']!=''].reset_index(drop=True)
    list_bulk = []
    for i in range(len(df_merge)):
        if df_merge['id_answer'][i] == '0':
            list_bulk.append(userDataFeedback(user=request.user, question_id=df_merge['id_question'][i], custom_answer=df_merge['text'][i]))
        else:
            list_bulk.append(userDataFeedback(user=request.user, question_id=df_merge['id_question'][i], answer_id=df_merge['id_answer'][i]))
    userDataFeedback.objects.bulk_create(list_bulk)
    return JsonResponse(data=res, safe=False)
