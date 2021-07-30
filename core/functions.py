from django.http import request
import pandas as pd
import numpy as np
import json
import sklearn.neighbors
from polls.models import *

pd.set_option('chained_assignment',None)
pd.set_option('display.max_columns',100)

class DistanceH:

    def distance_haversine(self, user_id):
        # School Data
        school_data = School.objects.values()
        df_school = pd.DataFrame(school_data)

        df_school_filtr = df_school[['school_name', 'lat', 'longi']]
        df_school_filtr['lat'] = df_school_filtr['lat'].apply(lambda x: np.radians(float(x)))
        df_school_filtr['longi'] = df_school_filtr['longi'].apply(lambda x: np.radians(float(x)))

        # User Data
        user_data = userData.objects.values()
        df_user = pd.DataFrame(user_data)
        df_user = df_user[df_user['user_id']==user_id]

        df_user_latLong = df_user[['id', 'lat', 'longi']]
        df_user_latLong['lat'] = df_user_latLong['lat'].apply(lambda x: np.radians(float(x)))
        df_user_latLong['longi'] = df_user_latLong['longi'].apply(lambda x: np.radians(float(x)))


        dist = sklearn.neighbors.DistanceMetric.get_metric('haversine')
        dist_matrix = (dist.pairwise
            (df_school_filtr[['lat','longi']],
            df_user_latLong[['lat','longi']])*6371
        )

        df_dist_matrix = (
            pd.DataFrame(dist_matrix)
        ).rename({0:'distance'}, axis=1)

        df_dist_matrix['school_name'] = df_school_filtr['school_name']
        df_dist_matrix = df_dist_matrix[['school_name', 'distance']]

        return df_dist_matrix

class mainFunction:

    def mainfunctiondf(self, user_id):
        user_data = userData.objects.values()
        df_user = pd.DataFrame(user_data)
        df_user = df_user[df_user['user_id']==user_id].drop(['user_id', 'lat', 'longi'], axis=1).reset_index(drop=True)

        school_data = School.objects.values()
        df_school = pd.DataFrame(school_data)

        dist = DistanceH()
        df_dist = dist.distance_haversine(user_id)

        df_tot = df_school.merge(df_dist, on='school_name').drop(['lat', 'longi'], axis=1)
        df_tot['distance'] = df_tot['distance'].apply(lambda x: round(x, 2))

        
        # scleta della distanza
        if df_user.iloc[0]['choice_distance'] != 0:
            df_tot = df_tot[df_tot['distance']<=df_user.iloc[0]['choice_distance']]

            
        list_speed = ['crecupero', 'extracurr', 'bStudio', 'stage', 'certificazioni', 'tutOrient']
        
        if str(df_user.iloc[0]['parit_choice']) != '0':
            df_tot = df_tot[df_tot['parit_choice']==df_user.iloc[0]['parit_choice']]
        for i in list_speed:
            if df_user.iloc[0][i] != 0 or df_user.iloc[0][i]:
                df_tot = df_tot[df_tot[i]==df_user.iloc[0][i]]


        # parent subject / subject
        if len(userData.objects.filter(user_id=user_id, parsub__pk__isnull=False).values('parsub__pk')) != 0:
            user_parsub = userData.objects.filter(parsub__pk__isnull=False).values('parsub__pk', 'user_id')
            df_parsub = pd.DataFrame(user_parsub)
            df_parsub_user = df_parsub[df_parsub['user_id']==user_id]
            id_parsub_user = df_parsub_user['parsub__pk']
            sub = Subject.objects.values()
            df_sub = pd.DataFrame(sub)
            df_sub_user = df_sub[df_sub['parsub_id'].isin(id_parsub_user)]
        else:
            Sub = Subject.objects.values()
            df_sub_user = pd.DataFrame(Sub)


        # area interesse / dettagli area interesse
        if len(userData.objects.filter(user_id=user_id, areaint__pk__isnull=False).values('areaint__pk')) != 0:
            user_parai = userData.objects.filter(user_id=user_id, areaint__pk__isnull=False).values('areaint__pk', 'user_id')
            df_ai = pd.DataFrame(user_parai)
            df_ai_user = df_ai[df_ai['user_id']==user_id] # ho il pk dell'area di interesse
            id_ai_user = df_ai_user['areaint__pk']
            detai = DettagliAreaInteresse.objects.values()
            df_detai = pd.DataFrame(detai)
            df_detai_user = df_detai[df_detai['name_ai_id'].isin(id_ai_user)]
        else:
            ai = DettagliAreaInteresse.objects.values()
            df_detai_user = pd.DataFrame(ai)
        
        durata = userData.objects.filter(user_id=user_id, durata__pk__isnull=False).values('durata__pk')
        df_durata_user = pd.DataFrame(durata, columns=['durata__pk'])

        # da school a durata
        if len(durata) != 0:
            durata_school = School.objects.filter(durata__pk__isnull=False).values('durata__pk', 'school_name')
            df_durata_school = pd.DataFrame(durata_school)
            df_durata_school = df_durata_school.groupby('school_name')['durata__pk'].apply(list).reset_index()
            query = df_durata_school['durata__pk'].apply(lambda x: any([k in x for k in df_durata_user['durata__pk'].values]))
            df_final_durata = df_durata_school[query]
            df_tot = df_tot.merge(df_final_durata, on='school_name')
        
        
        dettagliareainteresse = userData.objects.filter(user_id=user_id, dettagli_area_interesse__pk__isnull=False).values('dettagli_area_interesse__pk')
        df_dettagli_user = pd.DataFrame(dettagliareainteresse, columns=['dettagli_area_interesse__pk'])

        # dettagli aree di interesse
        if len(dettagliareainteresse) != 0:
            detai_school = School.objects.filter(dettagli_area_interesse__pk__isnull=False).values('dettagli_area_interesse__pk', 'school_name')
            df_detai_school = pd.DataFrame(detai_school)
            df_detai_school = df_detai_school.groupby('school_name')['dettagli_area_interesse__pk'].apply(list).reset_index()
            query_detai = df_detai_school['dettagli_area_interesse__pk'].apply(lambda x: any([k in x for k in df_dettagli_user['dettagli_area_interesse__pk'].values]))
            df_final_detai = df_detai_school[query_detai]
            df_tot = df_tot.merge(df_final_detai, on='school_name')
        
        # area di interesse
        areainteresse = userData.objects.filter(user_id=user_id, areaint__pk__isnull=False).values('areaint__pk')
        df_area_user = pd.DataFrame(areainteresse, columns=['areaint__pk'])
        
        if len(areainteresse) != 0:
            ai_school = School.objects.filter(dettagli_area_interesse__name_ai__pk__isnull=False).values('dettagli_area_interesse__name_ai__pk', 'school_name')
            df_ai_school = pd.DataFrame(ai_school)
            df_ai_school = df_ai_school.groupby('school_name')['dettagli_area_interesse__name_ai__pk'].apply(list).reset_index()
            query_ai = df_ai_school['dettagli_area_interesse__name_ai__pk'].apply(lambda x: any([k in x for k in df_area_user['areaint__pk'].values]))
            df_final_ai = df_ai_school[query_ai]
            df_tot = df_tot.merge(df_final_ai, on='school_name')
        
        # materie
        subUser = userData.objects.filter(user_id=user_id, sub__pk__isnull=False).values('sub__pk')
        df_subject_user = pd.DataFrame(subUser, columns=['sub__pk'])
        
        if len(subUser) != 0:
            sub_school = School.objects.filter(sub__pk__isnull=False).values('sub__pk', 'school_name')
            df_subject_school = pd.DataFrame(sub_school)
            df_subject_school = df_subject_school.groupby('school_name')['sub__pk'].apply(list).reset_index()
            query_sub = df_subject_school['sub__pk'].apply(lambda x: any([k in x for k in df_subject_user['sub__pk'].values]))
            df_final_sub = df_subject_school[query_sub]
            df_tot = df_tot.merge(df_final_sub, on='school_name')

        # parent materie
        parsub = userData.objects.filter(user_id=user_id, parsub__pk__isnull=False).values('parsub__pk')
        df_parsub_user = pd.DataFrame(parsub, columns=['parsub__pk'])
        
        if len(parsub) != 0:
            parsub_school = School.objects.filter(sub__parsub__pk__isnull=False).values('sub__parsub__pk', 'school_name')
            df_parsub_school = pd.DataFrame(parsub_school)
            df_parsub_school = df_parsub_school.groupby('school_name')['sub__parsub__pk'].apply(list).reset_index()
            query_parsub = df_parsub_school['sub__parsub__pk'].apply(lambda x: any([k in x for k in df_parsub_user['parsub__pk'].values]))
            df_final_parsub = df_parsub_school[query_parsub]
            df_tot = df_tot.merge(df_final_parsub, on='school_name')
            

        return df_tot['school_name'], df_sub_user, df_detai_user


class Results:

    def result(self, user_id):
        userdata = userData.objects.filter(user_id=user_id).values()
        df = pd.DataFrame(userdata)

        df = df.replace({False: 'No', True: 'Si'})

        json_records = df.reset_index().to_json(orient ='records')
        data = []
        data = json.loads(json_records)

        choiceUser = userData.objects.filter(user_id=user_id).values('dettagli_area_interesse__det_ai', 'areaint__name_ai', 'sub__name_sub', 'parsub__parsub')
        df_user = pd.DataFrame(choiceUser)

        schoolData = School.objects.values()
        df_school = pd.DataFrame(schoolData)

        dist = DistanceH()
        df_distance = dist.distance_haversine(user_id)
        main = mainFunction()
        df_school_user = main.mainfunctiondf(user_id)[0]

        df_school = df_school.merge(df_distance, on='school_name').reset_index(drop=True)
        df_school = df_school.merge(df_school_user, on="school_name").reset_index(drop=True)
        sc_filter = School.objects.values('school_name', 'sub__name_sub', 'sub__parsub__parsub', 'dettagli_area_interesse__det_ai', 'dettagli_area_interesse__name_ai__name_ai')
        df_school_filter = pd.DataFrame(sc_filter)
        df_school['distance'] = df_school['distance'].apply(lambda x: round(x, 3))

        if len(df_school) != 0:
            df_school_tmp = df_school.merge(df_school_filter, on='school_name').reset_index(drop=True)
            df_school_tmp = df_school_tmp.groupby('school_name').apply(lambda x: [list(x['sub__name_sub']), list(x['sub__parsub__parsub']), list(x['dettagli_area_interesse__det_ai']), list(x['dettagli_area_interesse__name_ai__name_ai'])]).apply(pd.Series).reset_index()
            df_school_tmp.columns = ['school_name', 'sub__name_sub', 'sub__parsub__parsub', 'dettagli_area_interesse__det_ai', 'dettagli_area_interesse__name_ai__name_ai']
        else:
            df_school_tmp = pd.DataFrame({})

        school_user = df_school[['school_name', 'distance']]

        if len(df_school_tmp) != 0:
            df_deta = school_user.merge(df_school_tmp, on='school_name').drop('distance', axis=1)
            df_deta['sub__name_sub'] = df_deta['sub__name_sub'].apply(lambda x: set(x))
            df_deta['sub__parsub__parsub'] = df_deta['sub__parsub__parsub'].apply(lambda x: set(x))
            df_deta['dettagli_area_interesse__det_ai'] = df_deta['dettagli_area_interesse__det_ai'].apply(lambda x: set(x))
            df_deta['dettagli_area_interesse__name_ai__name_ai'] = df_deta['dettagli_area_interesse__name_ai__name_ai'].apply(lambda x: set(x))
        else:
            df_deta = pd.DataFrame({})

        for i in range(len(df_school)):
            if df_school['lavoro'][i] == 1.0:
                df_school['lavoro'][i] = '/'
            if df_school['uni'][i] == 1.0:
                df_school['uni'][i] = '/'

        for i in range(len(df_user['dettagli_area_interesse__det_ai'])):
            if df_user['dettagli_area_interesse__det_ai'][i] == None:
                df_user['dettagli_area_interesse__det_ai'][i] = '-'
        
        for i in range(len(df_user['areaint__name_ai'])):
            if df_user['areaint__name_ai'][i] == None:
                df_user['areaint__name_ai'][i] = '-'
        
        for i in range(len(df_user['sub__name_sub'])):
            if df_user['sub__name_sub'][i] == None:
                df_user['sub__name_sub'][i] = '-'
        
        for i in range(len(df_user['parsub__parsub'])):
            if df_user['parsub__parsub'][i] == None:
                df_user['parsub__parsub'][i] = '-'
        

        json_recordsSchool = df_school.reset_index().to_json(orient ='records')
        dataSchool = []
        dataSchool = json.loads(json_recordsSchool)

        json_recordsSchoolDeta = df_deta.reset_index().to_json(orient ='records')
        dataSchoolDeta = []
        dataSchoolDeta = json.loads(json_recordsSchoolDeta)

        context = {
            'd': data,
            'dettagli':set(df_user['dettagli_area_interesse__det_ai']),
            'areaint':set(df_user['areaint__name_ai']),
            'subject':set(df_user['sub__name_sub']),
            'parsub':set(df_user['parsub__parsub']),
            'school': dataSchool,
            'school_deta':dataSchoolDeta
            }
        return context
