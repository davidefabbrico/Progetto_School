
import datetime

from django.db import models
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class AreaInteresse(models.Model):
    name_ai = models.CharField(max_length=200)
    def __str__(self):
        return self.name_ai
    
class DettagliAreaInteresse(models.Model):
    det_ai = models.CharField(max_length=200)
    name_ai = models.ForeignKey(AreaInteresse, on_delete=models.CASCADE, related_name='ai')
    def __str__(self):
        return self.det_ai

class parentSubject(models.Model):
    parsub = models.CharField(max_length=300)
    def __str__(self):
        return self.parsub

class Subject(models.Model):
    name_sub = models.CharField(max_length=200)
    parsub = models.ForeignKey(parentSubject, on_delete=models.CASCADE, related_name='sub')
    def __str__(self):
        return self.name_sub
    
    
class yearsSchool(models.Model):
    year = models.CharField(max_length=1)    
    
    def __str__(self):
        return self.year

# dalla materia alla scuola query?
# School.objects.filter(sub__pk=1)
# School.objects.filter(sub__name_sub='Meccanica') query con nome

class School(models.Model):
    
    PAR_CHOICE = (("S", "Statale"), ("NS", "Non Statale"))
    
    
    school_name = models.CharField("Nome della Scuola", max_length=1000)
    lavoro = models.FloatField("Lavoro", default=0, validators=[
            MaxValueValidator(100),
            MinValueValidator(1)]) # max e min
    uni = models.FloatField("Università", default=0, validators=[
            MaxValueValidator(100),
            MinValueValidator(1)]) # max e min
    longi = models.CharField("Longitudine (x)", max_length=1000)
    lat = models.CharField("Latitudine (y)", max_length=1000)
    parit_choice = models.CharField("Statale/Non Statale",
        max_length=100,
        choices=PAR_CHOICE,
        default="NS"
    )
    sub = models.ManyToManyField(Subject)
    dettagli_area_interesse = models.ManyToManyField(DettagliAreaInteresse)
    durata = models.ManyToManyField('polls.yearsSchool')
    crecupero = models.BooleanField("Corsi di recupero/approfondimento", default=False)
    extracurr = models.BooleanField("Attività Extra Curriculari", default=False)
    stage = models.BooleanField("Studio/Stage all'estero", default=False)
    certificazioni = models.BooleanField("Corsi per Certificazioni", default=False)
    tutOrient = models.BooleanField("Tutoraggio e Orientamento", default=False)
    bStudio = models.BooleanField("Borsa di studio", default=False)

    def __str__(self):
        return self.school_name

class PAR_STATUS:
    CHOICES = (("S", "Statale"), ("NS", "Non Statale"), (0, "Non selezionato"))

class userData(models.Model):
    
    lavoro = models.FloatField("Lavoro", default=0, validators=[
            MaxValueValidator(100),
            MinValueValidator(1)])
    
    uni = models.FloatField("Università", default=0, validators=[
            MaxValueValidator(100),
            MinValueValidator(1)])

    parit_choice = models.CharField("Statale/Non Statale",
        max_length=100,
        choices=PAR_STATUS().CHOICES,
        default=0
    )
    # User.objects.get().user_data.lon 
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_data", default='Nessuno')
    longi = models.CharField("Longitudine (x)", max_length=1000)
    lat = models.CharField("Latitudine (y)", max_length=1000) 
    areaint = models.ManyToManyField(AreaInteresse)
    dettagli_area_interesse = models.ManyToManyField(DettagliAreaInteresse)
    durata = models.ManyToManyField('polls.yearsSchool')
    parsub = models.ManyToManyField(parentSubject)
    sub = models.ManyToManyField(Subject)
    crecupero = models.BooleanField("Corsi di recupero/approfondimento", default=False)
    extracurr = models.BooleanField("Attività Extra Curriculari", default=False)
    bStudio = models.BooleanField("Borsa di studio", default=False)
    stage = models.BooleanField("Studio/Stage all'estero", default=False)
    certificazioni = models.BooleanField("Corsi per Certificazioni", default=False)
    tutOrient = models.BooleanField("Tutoraggio e Orientamento", default=False)
    choice_distance = models.IntegerField("Distanza", default=0)

    def __str__(self):
         return self.user.email

class userDataFeedback(models.Model):
    answer = models.ForeignKey(to="polls.Answer", default='', null=True, on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='answers', default='', on_delete=models.CASCADE)
    question = models.ForeignKey(to="polls.Question", default='', on_delete=models.CASCADE)
    custom_answer = models.CharField(max_length=255, default='')

    def __str__(self):
         return self.question.text

# https://docs.djangoproject.com/en/3.2/ref/models/constraints/
    

class Question(models.Model):
    text = models.CharField(max_length=255)
    required = models.BooleanField(default=False)
    answers = models.ManyToManyField(to='polls.Answer', related_name='questions', default='', blank=True)
    def __str__(self):
         return self.text


class ANSWER_TYPES:
    CHOICES = (("checkbox", "checkbox input"), ("radio", "radio input"), ("textarea", "textarea input"))


class Answer(models.Model):
    text = models.CharField(max_length=255)
    type = models.CharField("Tipo risposta (html)",
        max_length=100,
        choices=ANSWER_TYPES().CHOICES,
        default=0
    )

    def __str__(self):
         return self.text




# userDataFeedback.objects.all()[0].answer.all()[0].questions.all()


