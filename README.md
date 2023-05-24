# San Francisco fire service analysis

A hobby data science project to analyze San Francisco's fire service calls, safety complaints and incidents.
A summary of the project and its results is posted on my website [here](https://mneyrane.com/projects/sanfranciscofire).
The exploration and analysis is done entirely in Python using `pandas`, `geopandas`, `scipy.stats` and `seaborn`.

An overview of how to run the code, where to obtain the data, and technical details omitted from the project summary are discussed below.

## Running the code

### Requirements

The data processing and analysis scripts are written in Python. The project summary results were ran with **Python 3.11.2** and the following packages:

| Package | Version |
| ------- | ------- |
| `geopandas` | 0.13.0 |
| `matplotlib` | 3.7.1 |
| `numpy` | 1.24.3 |
| `pandas` | 2.0.1 |
| `scipy` | 1.10.1 |
| `seaborn` | 0.12.2 |
| `shapely` | 2.0.1 |

For convenience, I have included a `requirements.txt` to install via `pip`.

It may be possible to run the scripts with older versions of these packages or Python, but I have not attempted to test this.

### Datasets

To reproduce the analysis results (via the scripts under `02-analysis/`), I have included the finalized (i.e. extracted and cleaned) datasets under the `data/` directory. These have the filenames `DP-*.csv.gz`.

To download the original data, which can be processed using the scripts under `01-data-processing/`, visit the [San Francisco open data portal](https://datasf.org/opendata/) and search for

- fire department calls for service
- fire incidents
- fire safety complaints
- zoning map - zoning districts
- bay area counties

and export the datasets to CSV format. 
Save them to the `data/` directory and compress them with **gzip**.

### Code organization

The code is organized in the directories:

- `01-data-processing/` : extraction and cleaning of data
- `02-analysis/` : generate plots and perform statistical tests

For the data processing, script numbers indicate what order they should be executed in. 
Scripts sharing the same number are viewed as independent.

Finally, *all the datasets the scripts work on should be placed in the* `data/` *directory*.

### Order of execution and commands

**FIRST FOLDER**
...

- SCRIPT NAME:
    - Input: INPUT FILENAME
    - Output: OUTPUT FILENAME
    - Approximate runtime: TIME (IN SECONDS)
    - Command: `TERMINAL COMMAND TO RUN`
    ----
- REPEAT: ...

**SECOND FOLDER**
...

## Technical details

### Data usage and availability

...

### Processing and limitations

...

### Caveats with inferential statistics

...
