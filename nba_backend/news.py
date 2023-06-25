import pandas as pd
import requests
import json
import subprocess
from django.http import JsonResponse

uirobotPath ="C:\\Users\\Félix GM\\AppData\\Local\\Programs\\UiPath\\Studio\\UiRobot.exe"
mainFile = "C:\\Users\\Félix GM\\Documents\\UiPath\\ProcesoEnBlanco\\Main.xaml"

def get_news(request):
    try:
        # uiPathTrigger()
        df = pd.read_csv('nba_backend\\nba_backend\\assets\\nbaNews.csv')

        news = df.to_dict(orient='records')
        
        print(news)
        return JsonResponse({'news':news})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


def uiPathTrigger(): 
  

    subprocess.run([uirobotPath, '-file', mainFile], check=True)

    
