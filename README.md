# Smart-Traffic-Violation-Pattern-Detector
A Streamlit-based dashboard to analyze, visualize, and detect patterns in traffic violation data using interactive charts, maps, and trend analysis.

## Overview
This project is a Streamlit web application designed to analyze traffic violation data. It provides a user-friendly interface to explore, visualize, and gain insights from traffic violation datasets.

## Documentation: For a comprehensive understanding of the project, please refer to our detailed core documentation:

1. System Architecture (Basic): High-level overview, architecture diagrams, and directory structure.
2. Page Development Details: In-depth analysis of each page, purpose, and dependencies.
3. Visual Diagrams: Detailed Architecture, Data Flow, and Component Interaction diagrams.

## Features
Dataset Management:
Upload your own CSV datasets.
View and browse the loaded dataset.

Numerical Analysis:
Get a quick overview of your dataset, including shape and sample rows.
View detailed information about each column, including data types and descriptive statistics.

Data Visualization:
Generate various plots to visualize data distributions and relationships.

Trend Analysis:
Analyze trends in the data over time.

Map Visualization:
Visualize geographical data on an interactive map.

Correlation Analysis:
Explore correlations between numerical columns with a heatmap.

## Use Cases
Traffic police departments analyzing violation trends
Smart city planners identifying high-risk zones
Data analysts exploring real-world public datasets
Academic projects and demonstrations of data visualization

## How to Run
Clone the repository:

git clone https://github.com/Vinay1608m/Smart-Traffic-Violation-Pattern-Detector.git
cd smart-traffic-violation-pattern-detector
Choose your package manager:

 ## Primary Method: Using pip
Create and activate a virtual environment:

python -m venv .venv

# Activate the virtual environment

 On Windows (Command Prompt)
.\.venv\Scripts\activate

 On Windows (PowerShell)
.\.venv\Scripts\Activate.ps1

 On macOS/Linux
source .venv/bin/activate

## Install dependencies:
pip install .
Run the application:

streamlit run main.py
📂 Project Structure
.
├── .idea
├── artifact file
│   ├── Agile_Template_v0.1.xlsx
│   ├── Defect_Tracker Template_v0.1.xlsx
│   ├── Unit_Test_Plan_v0.1.xlsx
├── images
│   ├── smart_traffic.jpg
├── styles
│   ├── main.css
├── views
│   ├── _1_Home.py
│   ├── _2_Dashboard.py
│   ├── _3_Time_Trend_Analysis.py
│   ├── _4_Environment_Analysis.py
│   ├── _5_Vehicle_Analysis.py
│   ├── _6_Driver_Behaviour_Analysis.py
│   ├── _7_Payment_Analysis.py
│   ├── _8_Map_Visualisation.py
│   ├── _9_Report.py
│   └── _10_About.py
├── generate_cleaned_data.py
├── india_states.geojson
├── Indian_Traffic_Violations.csv
├── main.py
├── README.md
├── requirements.txt
├── utils.py
├── world.geojson

 ## Dependencies
The main dependencies for this project are listed in the pyproject.toml file. They include:

streamlit>=1.28 - Streamlit
pandas>=2.0 - Pandas
numpy>=1.23 - Numpy
matplotlib>=3.7 - Matplotlib
seaborn>=0.12 - Seaborn
plotly>=5.15 - Plotly
folium>=0.14 - Folium
streamlit-folium>=0.15 - Streamlit Folium
requests>=2.31 - Requests

## Future Enhancements

Machine Learning–based violation prediction
Real-time data ingestion via APIs
User authentication and role-based access
Automated report generation (PDF)
