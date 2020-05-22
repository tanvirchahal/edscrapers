# -*- coding: utf-8 -*-

""" module returns data for insights page """
import os
import pandas as pd
from edscrapers.tools.stats.stats import Statistics
from edscrapers.tools.dashboard.ckan_api import CkanApi
from edscrapers.tools.dashboard.pages.air import (get_datasets_bars_data, 
                                                 get_table_rows_by_office,
                                                 get_total_resources_by_office)

class InsightsData():

    # path to Excel sheet used for creating stas dataframes
    PATH_TO_EXCEL_SHEET = os.path.join(os.getenv('ED_OUTPUT_PATH'), 
                            'tools', 'stats', 'metrics.xlsx')

    def __init__(self):
        self.stats = Statistics()
        self.ckan_api = CkanApi()

    def get_compare_dict(self):            
        return self.stats.get_compare_dict()

    def get_df_from_excel_sheet(self, sheet_name):
        """ helper function used to read excel sheets and 
            create dataframes from the specified sheet"""

        return pd.read_excel(self.PATH_TO_EXCEL_SHEET, sheet_name, engine='openpyxl')

    def resources_by_domain_df(self):
        # this function uses a concatenation of 2 different excel sheets and dataframes
        df = self.get_df_from_excel_sheet('RESOURCE COUNT PER DOMAIN (DATOPIAN-AIR INTERSECTION)')
        working_df1 = pd.DataFrame(columns=['domain'])
        working_df1['domain'] = df['domain']
        working_df1['resource count'] = df['resource count_datopian']

        df = self.get_df_from_excel_sheet('RESOURCE COUNT PER DOMAIN (DATOPIAN ONLY)')
        working_df2 = pd.DataFrame(columns=['domain'])
        working_df2['domain'] = df['domain']
        working_df2['resource count'] = df['resource count']

        # concatenate the 2 dataframes
        return pd.concat([working_df1, working_df2], axis='index', ignore_index=True)

    def dataset_by_office_data(self):
        # returns the rows for the datasets by office table including total
        rows = get_table_rows_by_office('datasets_by_office')

        total_air = 0
        total_datopian = 0

        for row in rows: 
            total_air += row.get('air', 0)
            total_datopian += row.get('datopian', 0)

        total_row = {'s': 'Total', 'air' : total_air, 'datopian' : total_datopian}
        rows.append(total_row)

        return rows

    def resources_by_publisher_df(self):
        data = dict(get_total_resources_by_office('datopian'))

        publishers = []
        counts = []
        for key,value in data.items():
            publishers.append(key)
            counts.append(value)

        df = pd.DataFrame(columns=['publisher','resource count'])
        df['publisher'] = publishers
        df['resource count'] = counts

        return df

    def get_initial_estimate_data(self, id):

        data = {
            "datasets" : 32985,
            "resources" : 52709,
            "pages" : 52745,
            "domains" : 26
        }

        return data.get(id, 0)
