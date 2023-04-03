import requests
import json

class AnalysisService:
    def __init__(self, data_job_service):
        self.data_job_service = data_job_service

    def submit_analysis_request(self, marketplace: str, search_query: str) -> None:
        # TODO: Implement
        pass

    def get_analysis(self, marketplace, search_query) -> dict:
        response = requests.get(f"http://{self.data_job_service}/{marketplace}/{search_query}")
        return json.loads(response.text)