# -*- coding: utf-8 -*-
"""
Created on Mon Apr 13 18:42:16 2020

@author: Andrea De Santis
"""

import dash
import dash_core_components as dcc
from dash.dependencies import Input, Output
import dash_html_components as html
import requests

import plotly.graph_objects as go
import pandas as pd

#import regional population data from 
df_pop_reg=pd.read_csv("italian_regions_population.csv")

#geojson file for italian regions
url_geo = 'https://raw.githubusercontent.com/Dataninja/geo-shapes/master/italy/regions.geojson'
geo_data = requests.get(url_geo).json()

#mapbox token
#token ='instert_mapbox_token_here'

#url to national and regional raw data
url_nation="https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-andamento-nazionale/dpc-covid19-ita-andamento-nazionale.csv"
url_regions="https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-regioni/dpc-covid19-ita-regioni.csv"

#functions to load and clean-up the data
def get_national_data():
    df=pd.read_csv(url_nation)
    df.drop(["stato","note_it","note_en"],axis=1,inplace=True)
    df.columns = ['Date', 'Hospitalized with symptoms', 'IC',
       'Total hospitalized', 'Quarantined at home',
       'Total positives', 'Total variation in positives','New current positives',
       'Recovered', 'Deaths', 'Total cases', 'Total tests']
    df['Date'] = df['Date'].apply(lambda x: x[:-9])
    return df

def get_national_data_latestday():
    df = get_national_data()
    return df[df["Date"]==df["Date"].max()]

def get_regional_data():
    df=pd.read_csv(url_regions)
    df.drop(["stato","note_it","note_en"],axis=1,inplace=True)
    df.columns = ['Date', 'Region Id', 'Region', 'Lat', 'Long','Hospitalized with symptoms', 'IC',
       'Total hospitalized', 'Quarantined at home',
       'Total positives', 'Total variation in positives','New current positives',
       'Recovered', 'Deaths', 'Total cases', 'Total tests']
    df['Date'] = df['Date'].apply(lambda x: x[:-9])
    return df

def get_regional_data_latestday():
    df=get_regional_data()
    return df[df["Date"]==df["Date"].max()]
    return df

def clean_daily_regional_data(df):
    df=df.append({"Date":df[df["Region"]=="P.A. Trento"]["Date"].to_numpy()[0],
        "Region Id":4,
        "Region":"Trentino Alto Adige/Sudtirol",
        "Lat":df[df["Region"]=="P.A. Trento"]["Lat"].to_numpy()[0],
        "Long":df[df["Region"]=="P.A. Trento"]["Long"].to_numpy()[0],
        "Hospitalized with symptoms": (df[df["Region"]=="P.A. Trento"]["Hospitalized with symptoms"].to_numpy()[0]+
                                   df[df["Region"]=="P.A. Bolzano"]["Hospitalized with symptoms"].to_numpy()[0]),
        "IC": (df[df["Region"]=="P.A. Trento"]["IC"].to_numpy()[0]+
                                   df[df["Region"]=="P.A. Bolzano"]["IC"].to_numpy()[0]),
        "Total hospitalized": (df[df["Region"]=="P.A. Trento"]["Total hospitalized"].to_numpy()[0]+
                                   df[df["Region"]=="P.A. Bolzano"]["Total hospitalized"].to_numpy()[0]),
        "Quarantined at home": (df[df["Region"]=="P.A. Trento"]["Quarantined at home"].to_numpy()[0]+
                                   df[df["Region"]=="P.A. Bolzano"]["Quarantined at home"].to_numpy()[0]),
        "Total positives": (df[df["Region"]=="P.A. Trento"]["Total positives"].to_numpy()[0]+
                                   df[df["Region"]=="P.A. Bolzano"]["Total positives"].to_numpy()[0]),
        "Total variation in positives": (df[df["Region"]=="P.A. Trento"]["Total variation in positives"].to_numpy()[0]+
                                   df[df["Region"]=="P.A. Bolzano"]["Total variation in positives"].to_numpy()[0]),
        "New current positives": (df[df["Region"]=="P.A. Trento"]["New current positives"].to_numpy()[0]+
                                   df[df["Region"]=="P.A. Bolzano"]["New current positives"].to_numpy()[0]),
        "Recovered": (df[df["Region"]=="P.A. Trento"]["Recovered"].to_numpy()[0]+
                                   df[df["Region"]=="P.A. Bolzano"]["Recovered"].to_numpy()[0]),
        "Deaths": (df[df["Region"]=="P.A. Trento"]["Deaths"].to_numpy()[0]+
                                   df[df["Region"]=="P.A. Bolzano"]["Deaths"].to_numpy()[0]),
        "Total cases": (df[df["Region"]=="P.A. Trento"]["Total cases"].to_numpy()[0]+
                                   df[df["Region"]=="P.A. Bolzano"]["Total cases"].to_numpy()[0]),
        "Total tests":(df[df["Region"]=="P.A. Trento"]["Total tests"].to_numpy()[0]+
                                   df[df["Region"]=="P.A. Bolzano"]["Total tests"].to_numpy()[0])
            },ignore_index=True)
    df=df[(df["Region"] != 'P.A. Trento') & (df["Region"] != 'P.A. Bolzano')]
    df.sort_values(by=["Region Id"],inplace=True)
    df.index = [i for i in range(0,20)]
    return df

#instantiate dapp
app=dash.Dash()

#markdown header
markdown_text = '''
# Covid-19 outbreak in Italy
Data taken from: https://github.com/pcm-dpc/COVID-19

Dashboard source code available at: https://github.com/AndreaDesan/Italy-Covid19-Dashboard
'''

#create list of dictionaries for the x-axis of the national and regional timeseries scatterplot
timeseries_options = [{"label":i,"value":i} for i in list(get_national_data().columns[1:])]
region_options = [{"label":i,"value":i} for i in list(get_regional_data()["Region"].unique())]

#list of dictionary of the linear-log switch for the y-axis
log_axis_options=[
    {"label":"linear y axis","value":"linear"},
    {"label":"log y axis","value":"log"}
]


#app layout
app.layout = html.Div([
    html.Div(dcc.Markdown(children=markdown_text),
            style={"width":"100%","height":"150px","text-align":"center",'display': 'inline-block'}),
   
    html.H2(id="update-date",
             style={"position":"absolute","left":"5%","top":"7%","width":"20%", 'display': 'inline-block'}),

    html.Div([
    html.Div(dcc.Graph(id="national-timeseries")),
    html.Div(dcc.RadioItems(id='axis-type-national',
                             options=log_axis_options,
                            value="linear"),
             style={"position":"relative","left":"2%","width":"35%","text-align":"center",'display': 'inline-block'}),
    html.Div(dcc.Dropdown(id='timeseries-picker',
                          options=timeseries_options,
                          value="New current positives"),
             style={"position":"relative","left":"20%","width":"35%","text-align":"center",'display': 'inline-block'}),
    ], style={"position":"relative","left":"1%","width":"45%",'display': 'inline-block'}),
    
        html.Div(dcc.Graph(id="national-total-cases"),
             style={"position":"absolute","left":"50%","width":"45%",'display': 'inline-block'}),

    html.Div([
    html.Div(dcc.Graph(id="regional-timeseries")),
    html.Div(dcc.RadioItems(id='axis-type-regional',
                             options=log_axis_options,
                            value="linear"),
              style={"position":"relative","left":"0.55%","width":"30%","text-align":"center",'display': 'inline-block'}),
    html.Div(dcc.Dropdown(id='timeseries-picker-regional',
                          options=timeseries_options,
                          value="New current positives"),
             style={"position":"relative","left":"0.5%","width":"35%","text-align":"center",'display': 'inline-block'}),
    html.Div(dcc.Dropdown(id='region-picker',
                          options=region_options,
                          value="Lombardia"),
             style={"position":"relative","left":"0.5%","width":"30%","text-align":"center",'display': 'inline-block'}),
    ], style={"position":"relative","left":"-44%", "top":"490px","width":"45%",'display': 'inline-block'}),

    html.Div(dcc.Graph(id="national-total-cases-density"),
             style={"position":"relative","left":"50%", "width":"45%",'display': 'inline-block'}),

    dcc.Interval(
            id='interval-component',
            interval=24*3600*1000, # in milliseconds
            n_intervals=0)
],style={"backgroundColor":"#D3D3D3","height":"1200px"})   

#update latest update text box
@app.callback(Output('update-date', 'children'),
              [Input('interval-component', 'n_intervals')])
def update_date(n):
      df = get_national_data()
      return "Latest update:\n" + df["Date"].max()

#update national timeseries
@app.callback(Output('national-timeseries', 'figure'),
              [Input('interval-component', 'n_intervals'),
               Input('timeseries-picker', 'value'),
              Input('axis-type-national','value')])
def update_national_timeseries(n,selected_value,axis_type):
    df=get_national_data()
    return {
        'data': [go.Scatter(x=df.index,
                            text = df['Date'],
                            y=df[selected_value],
                            hovertemplate = '<b>Date</b>: <b>%{text}</b>' +
                            '<br><b>Value</b>: <b>%{y}</b></br><extra></extra>',
                           mode="markers+lines")],
        'layout': go.Layout(
            title = "National: "+selected_value,
            xaxis={'title': 'Day'},
            xaxis_type="linear",
            yaxis_type=axis_type,
            yaxis={'title': selected_value},
            hovermode='closest',
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )
    }
            
#update regional timeseries plot
@app.callback(Output('regional-timeseries', 'figure'),
              [Input('interval-component', 'n_intervals'),
               Input('timeseries-picker-regional', 'value'),
              Input('axis-type-regional','value'),
              Input('region-picker','value')])
def update_regional_timeseries(n,selected_value,axis_type,region):
    df=get_regional_data()
    df = df[df["Region"]==region]
    df.index = [i for i in range(0,len(df.index))]
    return {
        'data': [go.Scatter(x=df.index,
                            text = df['Date'],
                            y=df[selected_value],
                            hovertemplate = '<b>Date</b>: <b>%{text}</b>' +
                            '<br><b>Value</b>: <b>%{y}</b></br><extra></extra>',
                           mode="markers+lines")],
        'layout': go.Layout(
            title = region+": "+selected_value,
            xaxis={'title': 'Day'},
            xaxis_type="linear",
            yaxis_type=axis_type,
            yaxis={'title': selected_value},
            hovermode='closest',
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )
    }

#update total national cases - regional scatter map
@app.callback(Output('national-total-cases', 'figure'),
              [Input('interval-component','n_intervals')])
def update_national_total_cases(n):
    df=clean_daily_regional_data(get_regional_data_latestday())
    return {
        'data': [go.Scattermapbox(lat=df["Lat"],
                         lon=df["Long"], 
                         mode="markers",
                         customdata=df["Total cases"],
                         marker=dict(
                         size=df["Total cases"]/500
                                     ),
                         text = df['Region'],
                        hovertemplate = '<b>Region</b>: <b>%{text}</b>'+
                                            '<br><b>Total cases </b>: %{customdata}<br><extra></extra>',
                        )],
        'layout': go.Layout( 
                    title = "Total cases",
                    mapbox_style="open-street-map",
                    mapbox=dict(
 #                           accesstoken=token,
                            bearing=0,
                            center=go.layout.mapbox.Center(
                                lat=42,
                                lon=13
                                ),
                            pitch=0,
                            zoom=3.7
                            ),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
                    #margin={"r":250,"t":0,"l":350,"b":150}
        )
    }

#update national density choropleth map
@app.callback(Output('national-total-cases-density', 'figure'),
              [Input('interval-component','n_intervals')])
def update_national_total_cases_density(n):
    df=clean_daily_regional_data(get_regional_data_latestday())
    return {
        'data': [go.Choroplethmapbox(geojson=geo_data, 
                                    featureidkey="properties.COD_REG", 
                                    locations=df["Region Id"],
                                    z=df["Total cases"]/df_pop_reg["Population"]*10000,
                                    text = df['Region'],
                                    hovertemplate = '<b>Region</b>: <b>%{text}</b>'+
                                            '<br><b> Total cases per 10k inhabitants </b>: %{z}<br><extra></extra>',
                                    colorscale="blues")],
        'layout': go.Layout( 
                    title = "Total cases per 10000 inhabitants",
                    mapbox_style="open-street-map",
                    mapbox=dict(
#                            accesstoken=token,
                            bearing=0,
                            center=go.layout.mapbox.Center(
                                lat=42,
                                lon=13
                                ),
                            pitch=0,
                            zoom=3.7
                            ),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
                    #margin={"r":250,"t":0,"l":350,"b":150}
        )
    }
            
if __name__ == '__main__':
    app.run_server()