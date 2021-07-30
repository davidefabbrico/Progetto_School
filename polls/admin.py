from django.contrib import admin

from .models import *

class SchoolAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['school_name']}),
        ('Preparazione al mondo del lavoro / Università', {'fields': ['lavoro', 'uni']}),
        ('Longitudine / Latitudine', {'fields': ['lat', 'longi']}),
        ('Materia', {'fields': ['sub']}),
        ('Paritario / Non Paritario', {'fields': ['parit_choice']}),
        ('Area di interesse', {'fields': ['dettagli_area_interesse']}),
        ('Durata Anni di Scuola', {'fields': ['durata']}),
        ("Valori Booleani", {'fields': ['crecupero', 'extracurr', 'stage', 'certificazioni', 'tutOrient', 'bStudio']})

    ]
    search_fields = ['school_name']
    list_display = ('school_name', 'bStudio')


class SubjectsAdmin(admin.ModelAdmin):
    pass

class parSubjectsAdmin(admin.ModelAdmin):
    pass

class NameInterestAdmin(admin.ModelAdmin):
    pass

class DetInterestAdmin(admin.ModelAdmin):
    pass

class yearsSchoolAdmin(admin.ModelAdmin):
    pass

class userDataAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Id Utente', {'fields': ['user']}),
        ('Preparazione al mondo del lavoro / Università', {'fields': ['lavoro', 'uni']}),
        ('Longitudine / Latitudine', {'fields': ['longi', 'lat']}),
        ('Paritario / Non Paritario', {'fields': ['parit_choice']}),
        ('Area di interesse', {'fields': ['areaint', 'dettagli_area_interesse']}),
        ('Branca Materie / Materie', {'fields': ['sub']}),
        ('Durata Anni di Scuola', {'fields': ['durata']}),
        ('Distanza Scelta', {'fields':['choice_distance']}),
        ("Valori Booleani", {'fields': ['crecupero', 'extracurr', 'stage', 'certificazioni', 'tutOrient', 'bStudio']})

    ]
    # search_fields = ['school_name']
    # list_display = ('school_name', 'apom')

class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Testo', {'fields': ['text']}),
        ('Risposta', {'fields': ['answers']}),
        ('Richiesta', {'fields': ['required']}),
    ]

class AnswerAdmin(admin.ModelAdmin):
    pass

class userDataFeedbackAdmin(admin.ModelAdmin):
    fieldsets = [
        ('User', {'fields': ['user']}),
        ('Domanda', {'fields': ['question']}),
        ('Risposta', {'fields': ['answer']}),
        ('Custom', {'fields': ['custom_answer']})
    ]

admin.site.register(School, SchoolAdmin)
admin.site.register(Subject, SubjectsAdmin)
admin.site.register(parentSubject, parSubjectsAdmin)
admin.site.register(AreaInteresse, NameInterestAdmin)
admin.site.register(DettagliAreaInteresse, DetInterestAdmin)
admin.site.register(yearsSchool, yearsSchoolAdmin)
admin.site.register(userData, userDataAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)
admin.site.register(userDataFeedback, userDataFeedbackAdmin)