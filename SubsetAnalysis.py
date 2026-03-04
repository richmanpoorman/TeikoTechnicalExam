from sqlalchemy import Engine, text, URL, create_engine
from pandas import DataFrame
import pandas as pd 
from typing import TypedDict

class SubsetData(TypedDict):
    all_samples : DataFrame 
    samples_by_project : DataFrame 
    samples_by_response : DataFrame 
    samples_by_sex : DataFrame


def subsetAnalysis(database_engine : Engine) -> SubsetData: 
    
    with database_engine.connect() as connection: 
        query = '''
            SELECT S.sample, S.subject, S.project, S.b_cell, S.cd8_t_cell, S.cd4_t_cell, S.nk_cell, S.monocyte, P.age, P.sex, P.response 
            FROM Samples S, Subjects P
            WHERE S.time_from_treatment_start = 0 AND S.sample_type = 'PBMC' AND P.condition = 'melanoma' AND P.treatment = 'miraclib' AND S.subject = P.subject
        '''

        all_samples : DataFrame = pd.read_sql(text(query), connection)

        # Get the counts

        samples_by_project  : DataFrame = all_samples.groupby(['project']).size().reset_index(name='count')
        samples_by_response : DataFrame = all_samples.groupby(['response']).size().reset_index(name='count')
        samples_by_sex      : DataFrame = all_samples.groupby(['sex']).size().reset_index(name='count')


        project_types_query = ''' SELECT DISTINCT S.project FROM Samples S'''
        response_types_query = '''SELECT DISTINCT S.response FROM Subjects S'''
        sex_types_query      = '''SELECT DISTINCT S.sex FROM Subjects S'''

        project_types  : DataFrame = pd.read_sql(text(project_types_query), connection) 
        response_types : DataFrame = pd.read_sql(text(response_types_query), connection)
        sex_types      : DataFrame = pd.read_sql(text(sex_types_query), connection)

        by_project  : DataFrame = project_types.merge(samples_by_project, on='project', how='left').fillna({'count' : 0}).astype({'project' : str, 'count' : int})
        by_response : DataFrame = response_types.merge(samples_by_response, on='response', how='left').fillna({'count' : 0}).astype({'response' : str, 'count' : int})
        by_sex      : DataFrame = sex_types.merge(samples_by_sex, on='sex', how='left').fillna({'count' : 0}).astype({'sex' : str, 'count' : int})


        return {
            'all_samples'         : all_samples, 
            'samples_by_project'  : by_project, 
            'samples_by_response' : by_response, 
            'samples_by_sex'      : by_sex
        }

def melanomaMalesAvgBCellsTimeZero(database_engine : Engine) -> DataFrame:
    with database_engine.connect() as connection: 
        query = '''
            SELECT AVG(S.b_cell)
            FROM Samples S, Subjects P 
            WHERE P.condition = 'melanoma' AND P.sex = 'M' AND S.time_from_treatment_start = 0 AND P.response = 'yes' AND S.subject = P.subject
        '''

        return pd.read_sql(text(query), connection) 

### TESTING
