import pandas as pd
import requests
import json
import subprocess
from django.http import JsonResponse

uirobotPath ="C:\\Users\\Félix GM\\AppData\\Local\\Programs\\UiPath\\Studio\\UiRobot.exe"

def get_news(request):
    try:
        #uiPathTrigger()
        df = pd.read_csv('nba_backend\\nba_backend\\assets\\nbaNews.csv')

        news = df.to_dict(orient='records')
        
        print(news)
        return JsonResponse({'news':news})
    except:
        JsonResponse('error getting the news', status=400)


def uiPathTrigger(): 


    subprocess.run([uirobotPath, '-file', "C:\\Users\\Félix GM\\Documents\\UiPath\\ProcesoEnBlanco\\Main.xaml"], check=True)

    
