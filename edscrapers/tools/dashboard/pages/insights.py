""" module creates the dashboard '/insights' page """

# -*- coding: utf-8 -*-
import dash
import dash_table
import dash_daq as daq
import plotly.graph_objects as go
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

import pandas as pd
from edscrapers.tools.dashboard.pages.air import get_datasets_bars_data

from edscrapers.tools.dashboard.utils import buttonsToRemove
from edscrapers.tools.dashboard.pages.insights_data import InsightsData
from edscrapers.tools.dashboard.pages.tooltips import (INSIGHTS_TOTALS_SCRAPED_TOOLTIP,
                                                INSIGHTS_TOTALS_INGESTED_TOOLTIP,
                                                INSIGHTS_DATASETS_BY_DOMAIN_TOOOLTIP,
                                                INSIGHTS_DATASETS_BY_OFFICE_TOOOLTIP,
                                                INSIGHTS_RESOURCES_BY_DOMAIN_TOOOLTIP,
                                                INSIGHTS_RESOURCES_BY_OFFICE_TOOOLTIP,
                                                INSIGHTS_TOTALS_INITIAL_TOOLTIP)
from edscrapers.tools.dashboard.pages.components import header, led_display
                                        
class InsightsPage():

    def __init__(self):
        self.data = InsightsData()
    
    def dataset_by_domain_table(self):
        """ function used to create the Table component which displays 
        the number of pages/datasets obtained from each domain """

        # get the dataframe from the excel sheet
        df = self.data.get_df_from_excel_sheet('PAGE COUNT (DATOPIAN)')

        # add a total of page count at the end of the df
        total_page_count = df['page count'].sum()   

        df_total = pd.DataFrame([['Total', total_page_count]], 
                            columns=['domain','page count'])
        df = df.append(df_total, ignore_index=True)

        # create the DataTable
        return dash_table.DataTable(
                id='dataset_by_domain_table',
                #columns=[{"name": i, "id": i} \
                #    if i != "page count" else \
                #        {"name": "Dataset Count", "id": i} \
                #            for i in df.columns],
                columns=[{"id": "domain", "name": "Domain"}, 
                        {"id": "page count", "name": "Dataset Count"}],
                data=df.to_dict('records'),
                sort_action='native',
                style_cell={'textAlign': 'left', 
                            'whiteSpace': 'normal'},
                            #fixed_rows={ 'headers': True, 'data': 0 },
                            #virtualization=True,
                style_cell_conditional=[
                            {'if': {'column_id': 'domain'},
                            'width': '70%',
                            'textAlign': 'right'},
                            {'if': {'column_id': 'page count'},
                            'width': '30%'},
                            #{'if': {'row_index': 'odd'},
                            #'backgroundColor': 'rgb(248, 248, 248)'}
                            ],
                style_table={
                            'maxHeight': '300px',
                            'maxWidth': '100%',
                            'overflowY': 'auto',
                            'overflowX': 'hidden',
                            'margin': 0,
                            'padding': 0,
                            },
                style_header={
                            'backgroundColor': 'rgb(230, 230, 230)',
                            'fontWeight': 'bold',
                            'textAlign': 'center',
                            }
        )


    def dataset_by_domain_bar(self):
        """ function creates a bar chart which displays the 
        number of pages/datasets per domain """
        # the the dataframe from the Excel sheet
        df = self.data.get_df_from_excel_sheet('PAGE COUNT (DATOPIAN)')
        # create the bar chart using the created dataframe
        return dcc.Graph(
            id='dataset_by_domain_graph',
            figure={
                'data': [
                            {'x': df['domain'], 'y': df['page count'], 'type': 'bar'}
                        ],
                'layout': {
                    #'title': 'Datasets by Domain'
                }
            },
            config={ 
                'modeBarButtonsToRemove': buttonsToRemove 
            }
        )


    def resources_by_domain_table(self):
        """ function is used to create DataTable containing
        the number of resources/domains """

        # to perform this tasks, we need to collect stas from 2 different sheets
        # and unifiy it into one dataframe

        # get the resources collected from the datopian end of the air-datopian intersect
        df = self.data.get_df_from_excel_sheet('RESOURCE COUNT PER DOMAIN (DATOPIAN-AIR INTERSECTION)')

        # create a dataframe to hold the necessary info we use for this task
        working_df1 = pd.DataFrame(columns=['domain'])
        working_df1['domain'] = df['domain']
        working_df1['resource count'] = df['resource count_datopian']

        # get the resources from the DAtopian only resource count
        df = self.data.get_df_from_excel_sheet('RESOURCE COUNT PER DOMAIN (DATOPIAN ONLY)')
        
        working_df2 = pd.DataFrame(columns=['domain'])
        working_df2['domain'] = df['domain']
        working_df2['resource count'] = df['resource count']

        # concatenate the 2 dataframes
        working_df1 = pd.concat([working_df1,
                                working_df2], axis='index', ignore_index=True)
        
        # sort values
        working_df1.sort_values(by='resource count', axis='index',
                                    ascending=False, inplace=True,
                                    ignore_index=True)

        # add a total of resource count at the end of the df
        total_resource_count = working_df1['resource count'].sum()   

        df_total = pd.DataFrame([['Total', total_resource_count]], 
                            columns=['domain','resource count'])
        working_df1 = working_df1.append(df_total, ignore_index=True)
        
        # return the created DataTable
        return dash_table.DataTable(
                    id='resource_by_domain_table',
                    #columns=[{"name": i, "id": i} for i in working_df1.columns],
                    columns=[{"id": "domain", "name": "Domain"},
                            {"id": "resource count", "name": "Resource Count"}],
                    data=working_df1.to_dict('records'),
                    sort_action='native',
                    style_cell={'textAlign': 'left', 
                        'whiteSpace': 'normal'},
                    #fixed_rows={ 'headers': True, 'data': 0 },
                    #virtualization=True,
                    style_cell_conditional=[
                        {'if': {'column_id': 'domain'},
                        'width': '70%', 'textAlign': 'right'},
                        {'if': {'column_id': 'resource count'},
                        'width': '30%'},
                        #{'if': {'row_index': 'odd'},
                        #'backgroundColor': 'rgb(248, 248, 248)'}
                        ]
                        ,
                    style_table={
                        'maxHeight': '300px',
                        'maxWidth': '100%',
                        'overflowY': 'scroll',
                        'overflowX': 'hidden',
                        'margin': 0,
                        'padding': 0
                    },
                    style_header={
                        'backgroundColor': 'rgb(230, 230, 230)',
                        'fontWeight': 'bold',
                        'textAlign': 'center',
                    }
        )

    def resources_by_domain_pie(self):
        """" function is used to created a pie chart showing
        the number of resources gotten per domain """

        df = self.data.resources_by_domain_df()

        pie_figure = go.Figure(data=[go.Pie(labels=df['domain'],
                                            values=df['resource count'],
                                            title={
                                                #'text': 'Resources By Domain', 
                                                'font': {'size': 16}, 
                                                'position': 'bottom right'})])
        pie_figure.update_traces(textposition='inside', textinfo='value+label')

        # return the pie chart
        return dcc.Graph(id='resources_by_domain_pie',
                         figure=pie_figure,
                         config={ 
                            'modeBarButtonsToRemove': buttonsToRemove 
                         }
                        )

    def resources_by_publisher_table(self):

        df = self.data.resources_by_publisher_df()

         # add a total of resource count at the end of the df
        total_resource_count = df['resource count'].sum()   

        df_total = pd.DataFrame([['Total', total_resource_count]], 
                            columns=['publisher','resource count'])
        df = df.append(df_total, ignore_index=True)

        # return the created DataTable
        return dash_table.DataTable(
            id='resource_by_publisher_table',
            columns=[{"id": "publisher", "name": "Publisher"},
                     {"id": "resource count", "name": "Resource Count"}],
            data=df.to_dict('records'),
            sort_action='native',
            style_cell={'textAlign': 'left', 
                'whiteSpace': 'normal'},
            style_cell_conditional=[
                {'if': {'column_id': 'publisher'},
                'width': '70%', 'textAlign': 'right'},
                {'if': {'column_id': 'resource count'},
                'width': '30%'},
                #{'if': {'row_index': 'odd'},
                #'backgroundColor': 'rgb(248, 248, 248)'}
                ],
            style_table={
                        'maxHeight': '300px',
                        'maxWidth': '100%',
                        'overflowY': 'scroll',
                        'overflowX': 'hidden',
                        'margin': 0,
                        'padding': 0
            },
            style_header={
                        'backgroundColor': 'rgb(230, 230, 230)',
                        'fontWeight': 'bold',
                        'textAlign': 'center',
            }        
        )

    def resources_by_publisher_pie(self):

        df = self.data.resources_by_publisher_df()

        pie_figure = go.Figure(data=[go.Pie(labels=df['publisher'],
                                            values=df['resource count'],
                                            title={
                                                #'text': 'Resources By Domain', 
                                                'font': {'size': 16}, 
                                                'position': 'bottom right'})])
        pie_figure.update_traces(textposition='inside', textinfo='value+label')

        # return the pie chart
        return dcc.Graph(id='resources_by_publisher_pie',
                         figure=pie_figure,
                         config={ 
                            'modeBarButtonsToRemove': buttonsToRemove 
                         }
                        )

def generate_split_layout():
    """" function generates the latyout for this page """

    p = InsightsPage()

    return html.Div(children=[

    # Totals Based on Original Scraper
    html.Hr(style={'margin-top':'0px'}),
    header('Initial Estimate', 'totals-initial', INSIGHTS_TOTALS_INITIAL_TOOLTIP),
    html.Hr(),

    # LED displays
    led_display(p.data.get_initial_estimate_data("datasets"), 
        "DATASETS"),
    led_display(p.data.get_initial_estimate_data("resources"), 
        "RESOURCES"),
    led_display(p.data.get_initial_estimate_data("pages"),
        "PAGES"),
    led_display(p.data.get_initial_estimate_data("domains"), 
        "DOMAINS"),


    # Totals Based on Original Scraper
    html.Hr(style={'margin-top':'30px'}),
    header('Based on Scraper', 'totals-scraper', INSIGHTS_TOTALS_SCRAPED_TOOLTIP),
    html.Hr(),

    # LED displays
    led_display(p.data.get_compare_dict()['total']['datopian']['datasets'], 
        "DATASETS"),
    led_display(p.data.get_compare_dict()['total']['datopian']['resources'], 
        "RESOURCES"),
    led_display(sum(s for s in p.data.get_compare_dict()['total']['datopian']['pages'].values()),
        "PAGES"),
    led_display(p.data.resources_by_domain_df().count()['domain'], 
        "DOMAINS"),

    # Totals Ingested in the Data Portal
    html.Hr(style={'margin-top':'30px'}),
    header('Ingested into Data Portal', 'totals-ingested', INSIGHTS_TOTALS_INGESTED_TOOLTIP),
    html.Hr(),

    # LED displays
    led_display(000,
        "DATASETS"),
    led_display(000,
        "RESOURCES"),
    led_display(000,
        "PAGES"),
    led_display(0,
        "DOMAINS"),


    # Datasets By Publisher
    html.Hr(style={'margin-top':'70px'}),
    header('Datasets Ingested into the Portal by Publisher', 
            'datasets-office', INSIGHTS_DATASETS_BY_OFFICE_TOOOLTIP),
    html.Hr(),
    
    html.Div([
        dash_table.DataTable(
            columns=[{'name': 'Publisher', 'id': 's'}, 
                    {'name': 'Count', 'id': 'datopian'}],
            data=p.data.dataset_by_office_data(),
            sort_action='native',
            style_cell={'textAlign': 'left'},
            style_cell_conditional=[
                    #{'if': {'row_index': 'odd'},
                    #'backgroundColor': 'rgb(248, 248, 248)'}
                    ],
            style_table={
                'maxHeight': '300px',
            },
            style_header={
                    'backgroundColor': 'rgb(230, 230, 230)',
                    'fontWeight': 'bold',
                    'textAlign': 'center',
                    }

        ),
    ], style={
            'width': '50%', 
            'display': 'inline-block', 
            'vertical-align': 'middle'}
    ),

    html.Div([
        dcc.Graph(
            figure={
                'data': get_datasets_bars_data(),
                'layout': {
                    #'title': 'Datasets by Office'
                }
            },
            config={ 
                'modeBarButtonsToRemove': buttonsToRemove 
            }
            ),
        ], 
        style={
            'width': '50%', 
            'display': 'inline-block', 
            'vertical-align': 'middle'
            }
    ),

    # Resources by Publisher
    html.Hr(),
    header('Resources Ingested into the Portal by Publisher', 
            'resources-office',INSIGHTS_RESOURCES_BY_OFFICE_TOOOLTIP),
    html.Hr(),

    html.Div([
        p.resources_by_publisher_table()
    ],
    style={
        'width': '50%', 
        'display': 'inline-block',
        'vertical-align': 'middle', 
        'overflow-x': 'auto',
        'margin-bottom': '50px',}
    ),

    html.Div([
        p.resources_by_publisher_pie(),
    ], style={
        'width': '50%', 
        'display': 'inline-block', 
        'vertical-align': 'middle'}
    ),
    

    # Datasets By Domain
    html.Hr(),
    header('Datasets Ingested into the Portal by Domain', 
            'datasets-domain',INSIGHTS_DATASETS_BY_DOMAIN_TOOOLTIP),   
    html.Hr(),

    html.Div([
        p.dataset_by_domain_table()
    ],
    style={
        'width': '50%', 
        'display': 'inline-block',
        'vertical-align': 'middle', 
        'overflow-x': 'auto',
        'margin-bottom': '50px',}
    ),

    html.Div([
        p.dataset_by_domain_bar()],
        style={
            'width': '50%', 
            'display': 'inline-block', 
            'vertical-align': 'middle',
            'margin-bottom': '50px',
        }
    ),

    # Resources by Domain
    html.Hr(),
    header('Resources Ingested into the Portal by Domain', 
            'resources-domain',INSIGHTS_RESOURCES_BY_DOMAIN_TOOOLTIP),
    html.Hr(),

    html.Div([
        p.resources_by_domain_table()
    ], style={
        'width': '50%', 
        'display': 'inline-block', 
        'vertical-align': 'middle'}
    ),

    html.Div([
        p.resources_by_domain_pie(),
    ], style={
        'width': '50%', 
        'display': 'inline-block', 
        'vertical-align': 'middle'}
    ),

    html.Hr(),

])

external_stylesheets = [dbc.themes.BOOTSTRAP, 'https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.layout = generate_split_layout

if __name__ == '__main__':
    app.run_server(debug=False, dev_tools_hot_reload=True, host='0.0.0.0')