import pandas as pd
from typing import Generator
from models.PriceAnalysis import PriceAnalysis

class PriceAnalyzer:
    def analyze(self, data_generator: Generator) -> PriceAnalysis:
        print(f'Analyzing prices...')
        df = pd.DataFrame(data_generator)
        print(df)
        print(f'Finished analyzing prices.')
        return df

        