from sqlalchemy import Engine, text, URL, create_engine

from load_data import importData, createDatabase
from InitialAnalysis import initialAnalysis
from StatisticalAnalysis import relativeFrequencies, createFigures, signficanceTest 
from SubsetAnalysis import subsetAnalysis, melanomaMalesAvgBCellsTimeZero

import pandas as pd

### STEP 1
database_source = 'data/cell-count.csv'
database_name = 'cell_count.db'

initial_data_output = 'data/output/initial-data.csv'

responder_frequency_output = 'data/output/responder-frequency.csv'
nonresponder_frequency_output = 'data/output/nonresponder-frequency.csv'
siginficance_output = 'data/output/significance.csv'
figure_output = 'data/output/figure.html'

filtered_samples_output = 'data/output/filtered_samples_output.csv'
project_count_output = 'data/output/project-count.csv'
response_count_output = 'data/output/response-count.csv'
sex_count_output = 'data/output/sex-count.csv'

melanoma_output = 'data/output/melanoma-male.csv'

raw_data = importData(database_source)

engine = createDatabase(raw_data, database_name)

### STEP 2

# with engine.connect() as connection: 
#     subjects_results = pd.read_sql(text('SELECT * FROM Subjects'), connection)

#     samples_results = pd.read_sql(text('SELECT * FROM Samples'), connection)

#     # print(subjects_results)
#     # print(samples_results)


initial_data = initialAnalysis(engine)
# print(initial_data)
initial_data.to_csv(initial_data_output)

### STEP 3

population_frequencies = relativeFrequencies(engine, initial_data)
responders = population_frequencies['responders']
nonresponders = population_frequencies['nonresponders']

responders.to_csv(responder_frequency_output)
nonresponders.to_csv(nonresponder_frequency_output)
# print(population_frequencies)


signficances = signficanceTest(population_frequencies) 

signficances.to_csv(siginficance_output)
# print(signficances)

figure = createFigures(population_frequencies) 

figure.write_html(figure_output)

### STEP 4

subset_analysis = subsetAnalysis(engine)
all_samples         = subset_analysis['all_samples']
samples_by_project  = subset_analysis['samples_by_project']
samples_by_response = subset_analysis['samples_by_response']
samples_by_sex      = subset_analysis['samples_by_sex']

all_samples.to_csv(filtered_samples_output)
samples_by_project.to_csv(project_count_output)
samples_by_response.to_csv(response_count_output)
samples_by_sex.to_csv(sex_count_output)

# print(all_samples)
# print(samples_by_response)
# print(samples_by_project)
# print(samples_by_sex)

melanoma_males_avg_b_cells_time_zero = melanomaMalesAvgBCellsTimeZero(engine)

melanoma_males_avg_b_cells_time_zero.to_csv(melanoma_output)
# print(melanoma_males_avg_b_cells_time_zero)