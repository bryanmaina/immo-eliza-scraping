import pandas as pd
import re

# HELPER FUNCTION
def clean_numeric_column(df, column, pattern='[^\\d.]'): 
    # method to clean a column by removing all characters
    # except digits and dots
    # then converting the cleaned string to floats
    # create a temporary cleaned string version
    df[column + '_clean'] = df[column].astype(str).replace(pattern, '', regex=True)
    # convert cleaned string to numeric
    df[column] = pd.to_numeric(df[column + '_clean'], errors='coerce')
    # drop the temporary clean column
    df.drop(columns=[column + '_clean'], inplace=True)
    return df

# column names copied from models.py to use in this script for reference:
    # property_id: str
    # locality_name: str
    # post_code: str
    # price: str - remove possible currency
    # property_type: str
    # type_of_sale: str
    # number_of_rooms: str
    # living_area: str - remove possible units m2
    # equiped_kitchen: str - there is a typo in the label here! should be double P
    # furnished: str
    # open_fire: str
    # terrace_area: str - remove possible units m2
    # garden_area: str - remove possible units m2
    # number_of_facades: str
    # swimming_pool: str
    # state_of_building: str

# MAIN CLASS
class DataProcessing:
    def __init__(self, file_path=None):
        # update line of code above with local CSV file path to load data <---
        self.df = pd.read_csv(file_path)

    def process_data(self): # main method to process data, further methods detailed below
        self.clean_price()
        self.filter_out_type('life sale')
        self.clean_areas()
        self.convert_yes_no_columns()
        self.fill_missing()

    def clean_price(self): # method to clean the price column
        if 'price' in self.df.columns:
            self.df = clean_numeric_column(self.df, 'price')

    def filter_out_type(self, property_type): # method to remove rows with a specific property type e.g. life sale
        if 'property_type' in self.df.columns:
            self.df = self.df[self.df['property_type'].str.lower() != property_type.lower()]

    def clean_areas(self): # method to clean the area columns
        for col in ['living_area', 'terrace_area', 'garden_area']:
            if col in self.df.columns:
                self.df = clean_numeric_column(self.df, col)

    def convert_yes_no_columns(self): # method to convert yes/no to 1/0
        columns = ['furnished', 'equipped_kitchen', 'open_fire', 'swimming_pool'] # check column names <---
        for col in columns:
            if col in self.df.columns:
                self.df[col] = self.df[col].astype(str).str.strip().str.lower()
                self.df[col] = self.df[col].map({'yes': 1, 'no': 0})
                # fill NaN after mapping - when needed
                self.df[col].fillna(0, inplace=True)

    def fill_missing(self): # method to fill NaN with zero or other defaults - is this OK? <---
        self.df.fillna(0, inplace=True)

    def save_to_csv(self, output_path): # method to create the output file, update file path <---
        self.df.to_csv(output_path, index=False)