from sqlalchemy import Engine, text, URL, create_engine

from load_data import importData, createDatabase
from InitialAnalysis import initialAnalysis
from StatisticalAnalysis import relativeFrequencies, createFigures, signficanceTest 
from SubsetAnalysis import subsetAnalysis, melanomaMalesAvgBCellsTimeZero

import pandas as pd

### STEP 1
database_source = 'data/cell-count.csv'
database_name = 'cell_count.db'
figure_output = 'data/figure.html'

raw_data = importData(database_source)

engine = createDatabase(raw_data, database_name)

### STEP 2

with engine.connect() as connection: 
    subjects_results = pd.read_sql(text('SELECT * FROM Subjects'), connection)

    samples_results = pd.read_sql(text('SELECT * FROM Samples'), connection)

    print(subjects_results)
    print(samples_results)


initial_data = initialAnalysis(engine)
print(initial_data)

### STEP 3

population_frequencies = relativeFrequencies(engine, initial_data)

print(population_frequencies)

signficances = signficanceTest(population_frequencies) 

print(signficances)

figure = createFigures(population_frequencies) 

figure.write_html(figure_output)

### STEP 4

subset_analysis = subsetAnalysis(engine)
all_samples         = subset_analysis['all_samples']
samples_by_project  = subset_analysis['samples_by_project']
samples_by_response = subset_analysis['samples_by_response']
samples_by_sex      = subset_analysis['samples_by_sex']

print(all_samples)
print(samples_by_response)
print(samples_by_project)
print(samples_by_sex)

melanoma_males_avg_b_cells_time_zero = melanomaMalesAvgBCellsTimeZero(engine)
print(melanoma_males_avg_b_cells_time_zero)