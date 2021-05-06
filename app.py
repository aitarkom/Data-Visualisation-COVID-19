import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import json

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

#-------------------------- Manipulation des données ----------------------------------

df = pd.read_json('https://covid.ourworldindata.org/data/owid-covid-data.json ')

def delete_no_data_graph():
    countries = df.columns.values.tolist()
    for k in df.columns :
        data = pd.DataFrame(df.loc['data', k])
        if 'total_cases_per_million' not in data.columns or 'new_cases_per_million' not in data.columns or 'total_deaths_per_million' not in data.columns : 
            countries.remove(k)
    return countries

countries=delete_no_data_graph()

def delete_no_data_map() :
    df_map= pd.DataFrame(df.iloc[14])
    df_map['iso_alpha']=df_map.index
    df_map['Country']=df.loc['location']
    total_deaths = []
    total_cases=[]
    i=-1
    
    for k in df_map.iso_alpha :
        if k not in countries :
            df_map.drop(k, inplace=True)
    for j in df_map.iso_alpha:
        while 'total_deaths_per_million' not in df_map.data[:][j][i] or 'total_cases_per_million' not in df_map.data[:][j][i] :
            i-=1
        total_cases.append(df_map.data[:][j][i]['total_cases_per_million'])
        total_deaths.append(df_map.data[:][j][i]['total_deaths_per_million'])
    
    df_map['total_cases_per_million']=total_cases
    df_map['total_deaths_per_million']=total_deaths
    
    return df_map
#--------------------------------- Layout -----------------------------------------------
app.layout = html.Div([

    html.Div([
        html.H1("Projet Data Visualisation COVID-19", style={'text-align':'center'}),
        html.Br(),
        #--------------Graphe des cas-----------
        html.Div([
            dcc.Dropdown(id="Select Country",
                options =[
                {"label": t ,"value" : t } for t in countries
                ],
                multi=False,
                value="FRA",
                style={'width':"40%"}
            ),
        ]),
        html.Div(id='outpout_country', children=[]),
        html.Br(),
        html.Div([
            dcc.Dropdown(id="Select Data",
                options =[
                {"label": 'total_cases_per_million' ,"value" : 'total_cases_per_million' },
                {"label": 'new_cases_per_million' ,"value" : 'new_cases_per_million' }
                ],
                multi=False,
                value='total_cases_per_million',
                style={'width':"40%"}
            ),
        ]),
        html.Div(id='outpout_data', children=[]),
        html.Div([
            dcc.Graph(id="graphe-cas", figure={}),
        ]),
        #------------Graphe des morts-------------
        html.Br(),
        html.Div([
            dcc.Dropdown(id="Select_country_d",
                options =[
                {"label": t ,"value" : t } for t in countries
                ],
                multi=False,
                value="FRA",
                style={'width':"40%"}
            ),
        ]),
        html.Div(id='outpout_country_d', children=[]),
        html.Br(),
        html.Div([
            dcc.Dropdown(id="Select_data_d",
                options =[
                {"label": 'total_deaths_per_million' ,"value" : 'total_deaths_per_million' },
                {"label": 'new_deaths_per_million' ,"value" : 'new_deaths_per_million' }
                ],
                multi=False,
                value='total_deaths_per_million',
                style={'width':"40%"}
            ),
        ]),
        html.Div(id='outpout_data_d', children=[]),
        html.Div([
            dcc.Graph(id="graphe-morts", figure={}),
        ]),
        #----------carte choroplèthe cas------------
        html.Br(),
        html.Div([
            dcc.Dropdown(id="Select_data_map",
                options =[
                {"label": 'total_deaths_per_million' ,"value" : 'total_deaths_per_million' },
                {"label": 'total_cases_per_million' ,"value" : 'total_cases_per_million' }
                ],
                multi=False,
                value='total_deaths_per_million',
                style={'width':"40%"}
            ),
        ]),
        html.Div(id='outpout_data_map', children=[]),
        html.Div([
            dcc.Graph(id="map-cas", figure={}),
        ]),


    ]),

])

#---------------------------------Callbacks --------------------------------------------

@app.callback(
    [Output(component_id='outpout_country', component_property='children'),
     Output(component_id='outpout_data', component_property='children'),
     Output(component_id='graphe-cas', component_property='figure')],
     
    [Input(component_id='Select Country', component_property='value'),
     Input(component_id='Select Data', component_property='value')
    ]
)

def update_graphe_cas(country,cases):
    # print(country)
    # print(type(country))

    # print(cases)
    # print(type(cases))

    data = pd.DataFrame(df.loc['data', country])
    

    #Plotly Graph

    line_cas = px.line(data,
        x = 'date',
        y = cases,
        title = "Courbe d'évolution temporelle du nombre de cas confirmés / million d'habitants.")


    return format(country), format(cases), line_cas

@app.callback(
    [Output(component_id='outpout_country_d', component_property='children'),
     Output(component_id='outpout_data_d', component_property='children'),
     Output(component_id='graphe-morts', component_property='figure')],
     
    [Input(component_id='Select_country_d', component_property='value'),
     Input(component_id='Select_data_d', component_property='value')
    ]
)    

def update_graphe_mort(country,deaths):
    # print(country)
    # print(type(country))

    # print(cases)
    # print(type(cases))

    data = pd.DataFrame(df.loc['data', country])

    #Plotly Graph

    line_cas = px.line(data,
        x = 'date',
        y = deaths,
        title = "Courbe d'évolution temporelle du nombre de morts confirmés / million d'habitants.")


    return format(country), format(deaths), line_cas

@app.callback(
    [Output(component_id="map-cas", component_property='figure'),
     Output(component_id='outpout_data_map', component_property='children')],

    [Input(component_id='Select_data_map', component_property='value')]
)

def update_map(data_map):    

    #Plotly map

    fig = px.choropleth(delete_no_data_map(),
        locations = "iso_alpha" ,
        color=data_map,
        hover_name='Country',
        title="Carte du monde représentant le nombre de morts/million d'habitants ou le nombre de cas/million d'habitants", 
        labels= {"Nombre de cas par millions d'habitants"},
        color_continuous_scale=px.colors.sequential.Plasma,)
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(title=dict(font=dict(size=28),x=0.5,xanchor='center'),margin=dict(l=60,r=60,t=50,b=50))

    return fig,data_map

#---------------------------------------------------------------------------------------

if __name__ == '__main__':
        app.run_server(host= 'localhost',debug=True)
