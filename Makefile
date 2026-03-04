PYTHON = python
PIP = pip

all: setup pipeline 

setup: requirements.txt
	$(PIP) install -r requirements.txt

pipeline: Pipeline.py load_data.py InitialAnalysis.py StatisticalAnalysis.py SubsetAnalysis.py
	$(PYTHON) Pipeline.py

dashboard: Dashboard.py load_data.py InitialAnalysis.py StatisticalAnalysis.py SubsetAnalysis.py
	$(PYTHON) Dashboard.py

