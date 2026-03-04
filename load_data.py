import pandas as pd 
from pandas import DataFrame

from sqlalchemy import create_engine, URL, Engine, text
from typing import TypedDict


class DataTables(TypedDict):
    subjects : DataFrame 
    samples  : DataFrame

def importData(fileName : str = 'data/cell-count.csv') -> DataTables:
    raw_data : DataFrame = pd.read_csv(fileName)
    subjects : DataFrame = raw_data[["subject", "condition", "age", "sex", "treatment", "response"]].drop_duplicates()
    samples  : DataFrame = raw_data[["sample", "subject", "project", "sample_type", "time_from_treatment_start", "b_cell", "cd8_t_cell", "cd4_t_cell", "nk_cell", "monocyte"]]
    
    return {
        "samples" : samples, 
        "subjects" : subjects
    }



## Data validation checking
# print(raw_data["samples"])
# print(raw_data["subjects"])

# print(raw_data["samples"].duplicated(["sample"]).any())
# print(raw_data["subjects"].duplicated(["subject"]).any())

# print(raw_data["samples"].dtypes)
# print(raw_data["subjects"].dtypes)

def createDatabase(raw_data : DataTables, database_name : str = 'cell_count.db') -> Engine: 
    database_url = URL.create(
        "sqlite", 
        database=database_name
    )
    engine = create_engine(database_url, echo=True)
    
    ### Drop the table if it exists in the DB (so that we can create a new table after)
    with engine.connect() as connection: 
        

        connection.execute(text(
            '''
                DROP TABLE IF EXISTS Samples;  
            '''
        ))
        connection.execute(text(
            '''
                DROP TABLE IF EXISTS Subjects;
            '''
        ))
        connection.execute(text(
            '''
                CREATE TABLE IF NOT EXISTS Subjects (
                    subject TEXT PRIMARY KEY, 
                    condition TEXT, 
                    age INTEGER, 
                    sex CHAR(1), 
                    treatment TEXT, 
                    response TEXT
                );
            '''
        ))
        connection.execute(text(
            '''
                CREATE TABLE IF NOT EXISTS Samples (
                    sample TEXT PRIMARY KEY, 
                    subject TEXT REFERENCES Subjects(subject), 
                    project TEXT,
                    sample_type TEXT, 
                    time_from_treatment_start INTEGER, 
                    b_cell INTEGER, 
                    cd8_t_cell INTEGER, 
                    cd4_t_cell INTEGER, 
                    nk_cell INTEGER, 
                    monocyte INTEGER
                );
            '''
        ))
        connection.commit()

        raw_data["subjects"].to_sql("Subjects", con=connection, if_exists='append', index=False)
        raw_data["samples"].to_sql("Samples", con=connection, if_exists='append', index=False)

    return engine
    
### TESTING


raw_data = importData()

engine = createDatabase(raw_data)

with engine.connect() as connection: 
    subjects_results = pd.read_sql(text('SELECT * FROM Subjects'), connection)

    samples_results = pd.read_sql(text('SELECT * FROM Samples'), connection)

    print(subjects_results)
    print(samples_results)