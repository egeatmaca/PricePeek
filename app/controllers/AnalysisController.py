import requests
import json


class AnalysisController:
    def __init__(self, data_processor):
        self.data_processor = data_processor

    def submit_analysis_request(self, marketplace: str, search_query: str) -> None:
        # TODO: Implement
        pass

    def get_analysis(self, marketplace, search_query) -> dict:
        response = requests.get(f"http://{self.data_processor}/{marketplace}/{search_query}")
        return json.loads(response.text)