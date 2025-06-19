Technical assessment for Teiki.bio

## Setup and Installation

### Cloan or download the files in this github repository

### 1. Create and Activate Virtual Environment

#### Windows
```cmd
python -m venv venv
venv\Scripts\activate
```

#### Linux/Mac
```cmd
python3 -m venv venv
source venv/bin/activate
```

### 2. Install needed packages

```cmd
pip install pandas plotly scipy
```

### 3. Run the Program

#### Windows

```cmd
python main.py
```

#### Linux/Mac

```cmd
python3 main.py
```

## Schema Design

The database was desinged using three normalized tables, connected by foreign keys (sample_id and subject_id). Utilizing different tables will help as the scale of the data and project grow. As an example, one subject can have many samples, especially since we are looking at time series, meaning we can use a one to many relationship to better handle this kind of data between a subject and the samples. This can help reduce the total data storage by the use of keys and separate tables so we don't have redundant storage of a subject. This design should help reduce any data storage issues without compromising things such as data access or changes to analysis. 

## Code Structure and Design

The overall code structure follows have two files to separate the analysis section of the assessment and the database creation and functionlity. This is kept separate from the main.py file to reduce clutter and help with organization. Most of the functionlity is kept as simple as possible for the sake of time, but able to easily be exapanded into a dashboard or web interface using plotly dash or something similar. I opted for the interface to be in the terminal just for simplicity and to show an example of how the program can be used by someone from a non technical background. The main part for this that would be changed is actually getting the input through a cleaner interface for loading data and adding/removing samples from the database, such as using dropdown menus or something similar to add single sample data for uploads. Most of the functions contain default variables, such as file names, for the functionality of the assessment and so that they can be easily changes as a parameter as needed based of desired long term outlook. 

For creating visualizations, I decided to use plotly so that it can be easily implemented into a web interface using plotly dash. For the time being the program just saves the plots as html files that can be opened in a web browser. This decision was made since the environment the assessment will be run in was not known and this allows for both browser and terminal environments to be utilized. Some data, such as the summary table, is displaying just the head of the dataframe to reduce the total output in the terminal. This can easily be modified in a web interface or based off the stakeholders requirements. 

