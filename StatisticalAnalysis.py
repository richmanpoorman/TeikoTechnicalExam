from pandas import DataFrame
import pandas as pd 
from typing import TypedDict, Optional
from sqlalchemy import create_engine, URL, text, Engine
from InitialAnalysis import initialAnalysis

from plotly.graph_objects import Figure, Box, Scatter

from statsmodels.stats.weightstats import ztest

class PopulationFrequencies(TypedDict):
    responders : DataFrame 
    nonresponders : DataFrame

def relativeFrequencies(database_engine : Engine, initial_analysis : Optional[DataFrame] = None) -> PopulationFrequencies: 
    if initial_analysis is None: 
        initial_analysis = initialAnalysis(database_engine)
    
    

    with database_engine.connect() as connection: 
        responder_samples_query = '''
            SELECT A.sample 
            FROM Samples A, Subjects U 
            WHERE U.response = "yes" AND U.condition = \'melanoma\' AND U.treatment = \'miraclib\' AND A.sample_type = \'PBMC\' AND U.subject = A.subject
        '''

        nonresponders_samples_query =  '''
            SELECT A.sample 
            FROM Samples A, Subjects U 
            WHERE U.response = "no" AND U.condition = \'melanoma\' AND U.treatment = \'miraclib\' AND A.sample_type = \'PBMC\' AND U.subject = A.subject
        '''

        connection.commit() 
        # print(pd.read_sql(text('''SELECT * FROM Subjects S WHERE S.response = 'yes' '''), connection))

        responders_samples     = pd.read_sql(text(responder_samples_query), connection)
        nonresponders_samples = pd.read_sql(text(nonresponders_samples_query), connection)

        # print(responders_samples)
        # print(nonresponders_samples)
        # print(responders_samples.dtypes)
        # print(initial_analysis.dtypes)

        responders_relative_frequency     = responders_samples.merge(initial_analysis, how="left", on="sample")[["sample", "population", "percentage"]]
        nonresponders_relative_frequency = nonresponders_samples.merge(initial_analysis, how="left", on="sample")[["sample", "population", "percentage"]]


        return {
            "responders" : responders_relative_frequency,
            "nonresponders" : nonresponders_relative_frequency
        }


def createFigures(population_frequencies : PopulationFrequencies, showScatter : bool = False) -> Figure: 
    responder_frequencies = population_frequencies["responders"]
    nonresponder_frequencies = population_frequencies["nonresponders"]


    figure = Figure()
    
    responder_box_plot = Box(
        y = responder_frequencies["percentage"],
        x = responder_frequencies["population"],
        name = "Responsive", 
        marker_color = 'green', 
        boxpoints= 'all' if showScatter else None
    )

    nonresponder_box_plot =  Box(
        y = nonresponder_frequencies["percentage"], 
        x = nonresponder_frequencies["population"], 
        name = "Unresponsive", 
        marker_color = 'red', 
        boxpoints= 'all' if showScatter else None
    )

    figure.add_trace(responder_box_plot)
    figure.add_trace(nonresponder_box_plot)
    

    figure.update_layout(
        boxmode='group',
        xaxis= {
            'title' :  {
                'text' : 'Cell Types'
            } 
        },
        yaxis= {
            'title' :  {
                'text' : 'Percentage of Total Cells'
            } 
        }
    )

    return figure

def signficanceTest(population_frequencies : PopulationFrequencies) -> DataFrame: 
    responder_frequencies = population_frequencies["responders"]
    nonresponder_frequencies = population_frequencies["nonresponders"]

    cell_types = ['b_cell', 'cd8_t_cell', 'cd4_t_cell', 'nk_cell', 'monocyte']

    frequencies_populations_by_type = [
        (
            cell_type,
            nonresponder_frequencies[nonresponder_frequencies['population'] == cell_type]['percentage'],
            responder_frequencies[responder_frequencies['population'] == cell_type]['percentage']
        ) 
        for cell_type in cell_types
    ]

    z_test_results_zipped = [(cell_type, *ztest(x1 = nonresponsive_frequencies, x2 = responsive_frequencies, value = 0)) for cell_type, nonresponsive_frequencies, responsive_frequencies in frequencies_populations_by_type]
    cell_types, z_test_values, p_values = zip(*z_test_results_zipped)

    return DataFrame({
        "cell_types" : cell_types, 
        "z_statistic" : z_test_values, 
        "p_value" : p_values
    })

### TESTING
