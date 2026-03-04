# TeikoTechnicalExam
The technical assessment for Teiko

## Database Schema
Samples (**sample**, *subject*, project, sample_type, time_from_treatment_start, b_cell, cd8_t_cell, cd4_t_cell, nk_cell, monocyte)

Subjects (**subject**, condition, age, sex, treatment, response)

# Instructions 
1. run 'make setup' 
    This will install the dependencies
2. run 'make pipeline' 
    This will make the actual database; note that this is important to run before the dashboard, because the dashboard doesn't make the database
3. run 'make dashboard' 
    This will run the dashboard on port 8050; note that this is a local website, so you will need to make sure nothing else is running on that port
4. go to http://127.0.0.1:8050/
    This should bring you to the website

# Link
http://127.0.0.1:8050/

# Design 
I decided to break the database up into two parts; the person's profile, and the different samples 
This puts the database into a good balance of speed and repetition, as no data is really repeated
It also makes more logical sense, as the person wouldn't change even if they took multiple samples 

For the project itself, I took a more functional approach, where it would take in the engine that was connected to the database
which would allow for more switching in the future 

There are some hard coded pieces of information about the cell types, but it is that way because I am not amazingly familiar with 
the different cell types, and it should be fine since the schema is also hard coded 

The dashboard DOES process the information on its side (making the requests) but DOES NOT make the database; I did this, because the dashboard
shouldn't be responsible for the database, but in the future, we may want to move the parts to an API, but this dashboard would be easier 
to change and update with new information or data processing then it would be if it were an API (API would only really be needed if it were a public dashboard)