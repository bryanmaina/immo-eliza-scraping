# Immo Eliza - Data Collection

## Description

A virtual real estate company "Immo Eliza" wants to develop a machine learning model to make price predictions on real estate sales in Belgium. They hired us to help with the entire pipeline.

Our first task was to build a dataset gathering information about at least 10000 properties all over Belgium. This dataset is used later to train our prediction model.

We looked into different immo sites, such as Immoweb, Immovlan, Realo and Zimmo, but limited our final output.

The final dataset is a csv file with the following columns:

- Property ID
- Locality name
- Postal code
- Price
- Type of property (house or apartment)
- Number of rooms
- Living area (area in m²)
- Equipped kitchen (No - 0/ Yes - 1)
- Furnished (No - 0/ Yes - 1)
- Open fire (No - 0/ Yes - 1)
- Terrace (area in m² or None if no terrace)
- Garden (area in m² or None if no garden)
- Number of facades
- Swimming pool (No - 0/ Yes - 1)
- State of building (new, to be renovated, ...)

## Installation

> [!NOTE]
> *For Mac users: use `python3` instead of `python` in the below commands.*

1. Create a virtual environment:
   ```
   python -m venv venv
   ```
2. Activate the virtual environment:
   ```
   source venv/bin/activate
   ```
3. Install the dependencies:
   ```
   python -m pip install -r requirements.txt
   ```

## Repo structure

```
.
├── data/
│   ├── cleaned/
│   │   └── cleaned_property_data.csv
│   └── raw/
│       └── scraped_data.csv
├── src/
│   ├── conf/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   └── config.yaml
│   ├── scrapers/
│   │   ├── __init__.py
│   │   ├── basescraper.py
│   │   ├── realoscraper.py
│   ├── __init__.py
│   ├── data_processing.ipynb
│   ├── data_processing.py
│   ├── error_handling.py
│   ├── main.py
│   ├── models.py
│   └── scraper_service.py
├── .gitignore
├── PLAN.md
├── README.md
└── requirements.txt
```

## Development

We planned our project in Trello (https://trello.com/b/pXNAM8iq/data-collection-stage)

We created a private Github repository (https://github.com/bryanmaina/immo-eliza-scraping) with access for the team and the coach, and will make it public after completion of the project.

During the week, Brian focused on Git and scraping the Realo site, which was later decided to be stopped while shifting to Immoweb; Anna focused on Trello and scraping the Zimmo site, & Kristin started with reviewing the Selenium training documentation, then looked into identifiers on different immo websites and fields for duplicate identification, and on a script for data processing. 

> [!NOTE]
> *Don't forget to format your code before submitting a pull request!*

```
python -m black .
```

## Usage

Add when this would be used <---

## Sources

We are scraping the following immo sites:
- Immoweb (https://www.immoweb.be)
- Zimmo (https://www.zimmo.be/)

## Contributors

This was a group project:

- Anna - Project lead, workflow & Trello manager
- Bryan - Repo manager, handling Git
- Kristin - Documenter, writing README & presentation summarizing work

## Timeline

We had a week to work on this project (5 days)