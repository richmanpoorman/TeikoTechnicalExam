from load_data import importData, createDatabase
from InitialAnalysis import initialAnalysis
from StatisticalAnalysis import relativeFrequencies, createFigures, signficanceTest 
from SubsetAnalysis import subsetAnalysis, melanomaMalesAvgBCellsTimeZero

from dash import Dash, html, dcc

from dash.html import Div, H1, H2, H3, P
from dash.dash_table import DataTable
from dash.dcc import Graph

from pandas import DataFrame

from typing import Optional

app = Dash() 

# Step 1
raw_data = importData()
engine = createDatabase(raw_data)

# Step 2
initial_analysis = initialAnalysis(engine)


# Step 3
relative_frequences = relativeFrequencies(engine, initial_analysis) 
responders = relative_frequences['responders']
nonresponders = relative_frequences['nonresponders']
box_figures = createFigures(relative_frequences)
significance_tests = signficanceTest(relative_frequences)

# Step 4 
subset_analysis = subsetAnalysis(engine)
all_samples         = subset_analysis['all_samples']
samples_by_project  = subset_analysis['samples_by_project']
samples_by_response = subset_analysis['samples_by_response']
samples_by_sex      = subset_analysis['samples_by_sex']
melanoma_males_avg_b_cells_time_zero = melanomaMalesAvgBCellsTimeZero(engine)


def DashPandasTable(dataframe : DataFrame, id : Optional[str] = None) -> DataTable: 
    return DataTable(
        id = id, 
        data = dataframe.to_dict('records'), 
        columns = [{"name" : col, "id" : col} for col in dataframe.columns],
        style_table={
            'height': '300px',   
            'overflowY': 'auto', 
            'width': '100%',     
            'overflowX': 'auto'  
        }
    )

app.layout = Div(children=[

    H1(children = 'Initial Analsysis : Overview'),
        DashPandasTable(initial_analysis, "overview_table"),

    
    H1(children = 'Statistical Analysis'),
        H2("Relative Frequencies"),
            H3("Responders"), 
                DashPandasTable(responders, "responders_data"),
            H3("Non-responders"),
                DashPandasTable(nonresponders, "nonresponders_data"),
        H2("Box Plot of Immune Cell Populations between Responders and Non-responders"), 
            Graph(id='relative_frequency_graph', figure = box_figures),
    H2("Report on Significance"),
        DashPandasTable(significance_tests, "significance_test"),
        P("As shown here, the only significant change in the result was found to be in the cd4_t_cell percentage, as it is the only one with a p-value less than 0.05, meaning it is the only significant result"),

    H1(children = 'Subset Analysis'),
        H2("All Melanoma PBMC Samples at Baseline Treated with Miraclib"),
            DashPandasTable(all_samples, "all_samples_data"), 
        H2("Extended Queries"), 
            H3("Count for each project"),
                DashPandasTable(samples_by_project, "project_samples_data"), 
            H3("Count of Responsive"), 
                DashPandasTable(samples_by_response, "response_samples_data"), 
            H3("Count of Sex"), 
                DashPandasTable(samples_by_sex, "sex_samples_data"), 
        H2("Average number of B cells for responders at Time = 0"),
            DashPandasTable(melanoma_males_avg_b_cells_time_zero, "melanoma_males_avg_b_cells_time_zero")
])

if __name__ == '__main__':
    app.run(debug=True)