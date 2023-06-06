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

### Executing scripts

The scripts can be run via `python3 SCRIPT_PATH` from any location, as any data output will be saved in `data/`. Plots are generated in `figures/`.

## Technical details

### Data usage, availability and limitations

All the data in the analysis was obtained from the [San Francisco open data portal](https://datasf.org/opendata/) during May 2023.
For service calls, incidents and safety complaints, the analysis only used data extracted over 3 years from 2020 to 2022.
Some key limitations that could affect the analysis are:

- Zoning districts changing during the 3-year window of our data. The zoning map is updated quarterly and the city undergoes active development. We do not have direct access to earlier versions of the zoning map, but it may be possible to get it from contact through the data maintainer. Therefore, the accuracy of our zone-related analysis in Question 3 crucially relies on zone changes being relatively small.
- A very small number of fire incidents cannot be assigned a zone due to the coverage of geometry. As a workaround, the spatial join assigns a *nearest* zone to each incident.
- Some of the fire service data contains missing values or erroneous date entries. We did not attempt to correct them and instead omitted them from the analysis. After removing these entries, we still retain at least 98% of the data in each dataset.

### Caveats with inferential statistics

Commonly with inferential statistics, the primary limitation is failing to satisfy one or more assumptions in each hypothesis test.
There are two primary assumptions that are potentially violated for each question in the analysis.

- **Independence** *(all questions)*: For each test, we perform independent random draws of the data to enforce independence. However, we do not expect the data to be independent in general. For example, in Question 1, complaints in spatiotemporal proximity could have overlapping fire incidents.
- **Normality** *(question 2)*: The fire incident count is nonnegative, so the data cannot be normally distributed.
