import requests
import json
import os

class AnalysisController:
    def get_analysis(self, marketplace, search_query):
        response = requests.get(f"http://{os.environ.get('DATA_JOB_SERVICE')}/{marketplace}/{search_query}")
        return json.loads(response.text)