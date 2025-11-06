import pandas as pd
import re

# HELPER FUNCTION
def clean_numeric_column(df, column, pattern='[^\\d.,]', as_int=False, is_price=False): 
    # method to clean a column by removing all unwanted characters like currencies,
    # normalize European number format
    # then converting the cleaned string to integers
    # property_id should not go through this function, as it is expected to be a combination of letters and numbers
    # create a temporary cleaned string version
    df[column + '_clean'] = df[column].astype(str).replace(pattern, '', regex=True)
    if is_price:
        # Remove dots as thousands separator, replace comma with dot for decimals
        df[column + '_clean'] = df[column + '_clean'].str.replace('.', '', regex=False)  # remove thousands sep
        df[column + '_clean'] = df[column + '_clean'].str.replace(',', '.', regex=False)  # convert decimal comma
    # convert cleaned string to numeric
    df[column] = pd.to_numeric(df[column + '_clean'], errors='coerce')
    # drop the temporary clean column
    df.drop(columns=[column + '_clean'], inplace=True)
    if as_int:
        df[column] = df[column].fillna(0).astype(int)
    return df

# column names copied from models.py to use in this script for reference:
    # property_id
    # locality_name
    # postal_code
    # price - remove possible currency
    # property_type
    # number_of_rooms
    # living_area: - remove possible units m2
    # equipped_kitchen
    # furnished
    # open_fire
    # terrace_area - remove possible units m2
    # garden_area - remove possible units m2
    # number_of_facades
    # swimming_pool
    # state_of_building

# MAIN CLASS
class DataProcessing:
    def __init__(self, file_path='test_properties.csv'):
        # update line of code above with local CSV file path to load data <---
        # need to check if csv is truly comma-separated (MacOS may create ;-separated)
        with open(file_path, 'r', encoding='utf-8') as f:
            first_line = f.readline()
            if ';' in first_line:
                sep = ';'
            else:
                sep = ','
        self.df = pd.read_csv(file_path, sep=sep, dtype={"property_id": str})
        print("Before any cleaning:")
        print(self.df.dtypes)
        print(self.df.head(5))
        print("Rows loaded:", len(self.df))

    def process_data(self): # main method to process data, further methods detailed below
        self.clean_price()
        # self.filter_out_type('life sale')
        self.clean_areas()
        self.convert_yes_no_columns()
        self.clean_other_numeric_columns()
        self.remove_duplicates()
        self.remove_empty_rows()
        self.fill_missing()

    def clean_price(self): # method to clean the price column
        if 'price' in self.df.columns:
            self.df = clean_numeric_column(self.df, 'price', as_int=True, is_price=True)
            print("Cleaning price fields...")
            print(f"After cleaning price, rows = {len(self.df)}")

    # def filter_out_type(self, type_of_sale): # method to remove rows with a specific property type e.g. life sale
    #     if 'type_of_sale' in self.df.columns:
    #         self.df = self.df[self.df['type_of_sale'].str.lower() != type_of_sale.lower()]
    #         print("Filtering out life sale property types...")
    #         print(f"After filtering out life sale property type, rows = {len(self.df)}")

    def clean_areas(self): # method to clean the area columns
        for col in ['living_area', 'terrace_area', 'garden_area']:
            if col in self.df.columns:
                # Remove units like 'm2', 'm²' (case-insensitive)
                self.df[col] = self.df[col].astype(str).str.replace(r'\s*m[²2]', '', regex=True)
                self.df = clean_numeric_column(self.df, col, as_int=True)
            print("Cleaning area fields...")
            print(f"After cleaning area, rows = {len(self.df)}")

    def convert_yes_no_columns(self): # method to convert yes/no to 1/0
        yes_no_map = {'yes': 1, 'y': 1, 'no': 0, 'n': 0}
        for col in ['furnished', 'equipped_kitchen', 'open_fire', 'swimming_pool']:
            if col in self.df.columns:
                self.df[col] = (
                    self.df[col]
                    .astype(str)
                    .str.strip()
                    .str.lower()
                    .map(yes_no_map)
                    .fillna(0)
                    .astype(int)
                )
        print("Converting Yes/No columns to 1/0 integers...")
        print(f"After converting Yes/No, rows = {len(self.df)}")

    def clean_other_numeric_columns(self): # convert other numeric columns to integers
        for col in ['number_of_rooms', 'number_of_facades']:
            if col in self.df.columns:
                self.df = clean_numeric_column(self.df, col, as_int=True)
        print("Cleaning other numeric fields...")
        print(f"After cleaning other numeric fields, rows = {len(self.df)}")

    def remove_duplicates(self): # method toemove duplicates based on all columns except property_id
        cols_to_check = [col for col in self.df.columns if col != 'property_id']
        self.df.drop_duplicates(subset=cols_to_check, keep='first', inplace=True)
        print("Removing duplicates...")
        print(f"After removing duplicates, rows = {len(self.df)}")

    def remove_empty_rows(self): # method to remove rows where Property_ID is missing or all other fields are empty
        critical_cols = [col for col in self.df.columns if col != 'property_id']
        self.df.dropna(subset=['property_id'], inplace=True)  # Remove rows without property_id
        self.df.dropna(subset=critical_cols, how='all', inplace=True)  # Remove rows where all other fields empty
        print("Removing empty rows...")
        print(f"After removing empty rows, rows = {len(self.df)}")

    def fill_missing(self): # method to fill missing fields except for property_id
        for col in self.df.columns:
           if col != 'property_id':
                if self.df[col].dtype in [int, float]:
                    self.df[col] = self.df[col].fillna(0)
                else:
                    self.df[col] = self.df[col].fillna('')
        print("Filling missing fields...")
        print(f"After filling missing fields, rows = {len(self.df)}")

    def save_to_csv(self, output_path='cleaned_properties.csv'): # method to create the output file, update file path <---
        self.df.to_csv(output_path, index=False)
        print("Saving cleaned output as csv ...")