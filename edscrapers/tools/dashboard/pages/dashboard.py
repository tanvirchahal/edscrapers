import dash
import dash_table
import pandas as pd
import dash_daq as daq
import plotly.graph_objects as go
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

from edscrapers.tools.dashboard.pages.insights_data import InsightsData
from edscrapers.tools.dashboard.utils import buttonsToRemove
from edscrapers.tools.dashboard.pages.components import header, led_display
from edscrapers.tools.dashboard.ckan_api import CkanApi

class DashboardPage():

    def __init__(self):
        self.ckan_api = CkanApi()

    def json_data(self):
        return [ {"id" : "total", "label" : "Total", "value" : 272},
             {"id" : "scraped", "label" : "Scraped Datasets", "value" : 223},
             {"id" : "amended", "label" : "Datasets Amended by User", "value" : 15},
             {"id" : "manually", "label" : "Datasets Manually Added", "value" : 34} ]

    def datasets_in_portal_led_data(self, id):

        value = 0

        data = self.json_data()
        for json_dict in data:
            if json_dict.get("id") == id:
                value = json_dict.get("value")
                break
        
        return  value
    
    def datasets_in_portal_led_label(self, id):

        label = ""

        data = self.json_data()
        for json_dict in data:
            if json_dict.get("id") == id:
                label = json_dict.get("label")
                break
        
        return label

    def get_total_datasets_in_portal(self):
        package_names = self.ckan_api.get_package_list()
        return(len(package_names))

    def datasets_in_portal_pie_data(self):

        labels = [] 
        values = []

        data = self.json_data()
        for json_dict in data:

            if json_dict.get("id") == "total":
                continue

            label = json_dict.get("label")
            value = json_dict.get("value")
            labels.append(label)
            values.append(value)
        
        return labels, values

    def datasets_in_portal_pie(self):
        """" function is used to created a pie chart showing
        the number of datasets in the Portal """

        labels, values = self.datasets_in_portal_pie_data()

        pie_figure = go.Figure(data=[go.Pie(labels=labels,
                                            values=values,
                                            title={
                                                'font': {'size': 16}, 
                                                'position': 'top right'}
                                            )])
        pie_figure.update_traces(textposition='inside', textinfo='value+label')

        # return the pie chart
        return dcc.Graph(id='resources_by_domain_pie',
                        figure=pie_figure,
                        config={ 
                            'modeBarButtonsToRemove': buttonsToRemove 
                        }
        )

    def tooltip(self):
        return html.Div([
            html.Span("Datasets in Portal", style={'font-weight':'bold'}),
            html.Span(" - Total number of datasets in portal."),
            html.Br(),
            html.Br(), 
            html.Span("Scraped Datasets", style={'font-weight':'bold'}),
            html.Span(" - Total number of scraped datasets."),
            html.Br(),
            html.Br(),
            html.Span("Datasets Amended", style={'font-weight':'bold'}), 
            html.Span(" - Total number of scraped datasets which have been amended by a user."),
            html.Br(),
            html.Br(),
            html.Span("Datasets Manually Added", style={'font-weight':'bold'}), 
            html.Span(" - Total number of datasets manually added by a user.")
        ])

def generate_layout():
    
    p = DashboardPage()

    label_total = p.datasets_in_portal_led_label("total")
    value_total = p.get_total_datasets_in_portal()
    label_scraped = p.datasets_in_portal_led_label("scraped")
    value_scraped = 0
    label_amended = p.datasets_in_portal_led_label("amended")
    value_amended = 0
    label_manually = p.datasets_in_portal_led_label("manually")
    value_manually = 0

    return html.Div(children=[
    
    # Datasets By Domain
    html.Hr(),
    header('Portal Totals', 
            'portal-totals', p.tooltip()),   
    html.Hr(),

    # LED displays
    
    led_display(value_total, label_total),
    led_display(value_scraped, label_scraped),
    led_display(value_amended, label_amended),
    led_display(value_manually, label_manually),

    html.Hr(),

    # Total dataset in the portal pie chart
    html.Div([
            p.datasets_in_portal_pie(),
        ], style={'vertical-align': 'middle'}
    ),
    
    ])
    
external_stylesheets = [dbc.themes.BOOTSTRAP, 'https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.layout = generate_layout

if __name__ == '__main__':
    app.run_server(debug=False, dev_tools_hot_reload=True, host='0.0.0.0')