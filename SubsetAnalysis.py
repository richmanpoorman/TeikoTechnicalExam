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
            SELECT S.sample, S.subject, S.project, S.sample_type, S.b_cell, S.cd8_t_cell, S.cd4_t_cell, S.nk_cell, S.monocyte, P.condition, P.age, P.sex, P.treatment, P.response 
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


### TESTING
database_name = 'cell_count.db'

database_url = URL.create(
    "sqlite", 
    database=database_name
)
engine = create_engine(database_url, echo=True)

subset_analysis = subsetAnalysis(engine)
all_samples         = subset_analysis['all_samples']
samples_by_project  = subset_analysis['samples_by_project']
samples_by_response = subset_analysis['samples_by_response']
samples_by_sex      = subset_analysis['samples_by_sex']

print(all_samples)
print(samples_by_response)
print(samples_by_project)
print(samples_by_sex)

with engine.connect() as connection: 
    query = '''
        SELECT AVG(S.b_cell)
        FROM Samples S, Subjects P 
        WHERE P.condition = 'melanoma' AND P.sex = 'M' AND S.time_from_treatment_start = 0 AND S.subject = P.subject
    '''

    melanomaMalesAvgBCellsTimeZero = pd.read_sql(text(query), connection) 
    print(melanomaMalesAvgBCellsTimeZero)