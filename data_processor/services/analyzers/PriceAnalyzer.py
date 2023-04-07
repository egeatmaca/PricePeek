import pandas as pd
from typing import Generator

class PriceAnalyzer:
    def analyze(self, data_generator: Generator) -> dict:
        print(f'Analyzing prices...')
        df = pd.DataFrame(data_generator)
        print(df)
        print(f'Finished analyzing prices.')
        return df.to_dict('records')

        