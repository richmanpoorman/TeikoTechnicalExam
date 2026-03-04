import pandas as pd 
from pandas import DataFrame

from sqlalchemy import create_engine, URL, Engine, text
from typing import TypedDict

database_name = 'cell_count.db'

def initialAnalysis(database_engine : Engine) -> DataFrame: 
    with database_engine.connect() as connection: 
        cell_types = ['b_cell', 'cd8_t_cell', 'cd4_t_cell', 'nk_cell', 'monocyte']
        totalCount = f'SELECT sample, ({" + ".join(cell_types)}) as total_count FROM Samples'
        eachPopulation = [f'SELECT sample, \'{population}\' AS population, {population} AS count \nFROM Samples \n' for population in cell_types]
        noPercentage = "UNION ALL\n".join(eachPopulation)

        analysisQuery = f'''
            WITH total_counts AS ({totalCount}), 
                 no_percentage AS ({noPercentage})
            SELECT T.sample, T.total_count, P.population, P.count, 100.0 * P.count / T.total_count AS percentage
            FROM total_counts T, no_percentage P 
            WHERE T.sample = P.sample
            ORDER BY T.sample, P.population
        '''

        analysisData : DataFrame = pd.read_sql(text(analysisQuery), con=connection)

        return analysisData

### TESTING
