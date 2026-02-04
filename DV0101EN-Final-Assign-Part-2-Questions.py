#!/usr/bin/env python
# coding: utf-8

import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

# Load the data
data = pd.read_csv(
    'https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/'
    'd51iMGfp_t0QpO30Lym-dw/automobile-sales.csv'
)

# Initialize the Dash app
app = dash.Dash(__name__)

# List of years
year_list = [i for i in range(1980, 2024)]

# ---------------------------------------------------------------------------------------
# Layout
app.layout = html.Div([

    # TASK 2.1: Title
    html.H1(
        "Automobile Sales Statistics Dashboard",
        style={'text-align': 'center', 'color': '#503D36', 'font-size': '24px'}
    ),

    # TASK 2.2: Dropdowns
    html.Div([
        html.Label("Select Statistics:"),
        dcc.Dropdown(
            id='dropdown-statistics',
            options=[
                {'label': 'Yearly Statistics', 'value': 'Yearly Statistics'},
                {'label': 'Recession Period Statistics', 'value': 'Recession Period Statistics'}
            ],
            value='Select Statistics',
            placeholder='Select a report type'
        )
    ]),

    html.Div(
        dcc.Dropdown(
            id='select-year',
            options=[{'label': i, 'value': i} for i in year_list],
            value='Select-year'
        )
    ),

    # TASK 2.3: Output container
    html.Div([
        html.Div(
            id='output-container',
            className='chart-grid',
            style={'display': 'flex'}
        )
    ])
])

# ---------------------------------------------------------------------------------------
# TASK 2.4: Enable / Disable Year Dropdown
@app.callback(
    Output('select-year', 'disabled'),
    Input('dropdown-statistics', 'value')
)
def update_input_container(selected_statistics):
    if selected_statistics == 'Yearly Statistics':
        return False
    return True

# ---------------------------------------------------------------------------------------
# TASK 2.4–2.6: Output Container Callback
@app.callback(
    Output('output-container', 'children'),
    [
        Input('dropdown-statistics', 'value'),
        Input('select-year', 'value')
    ]
)
def update_output_container(selected_statistics, selected_year):

    # ================= RECESSION STATISTICS =================
    if selected_statistics == 'Recession Period Statistics':

        recession_data = data[data['Recession'] == 1]

        yearly_rec = recession_data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        R_chart1 = dcc.Graph(
            figure=px.line(
                yearly_rec,
                x='Year',
                y='Automobile_Sales',
                title='Average Automobile Sales during Recession'
            )
        )

        average_sales = recession_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
        R_chart2 = dcc.Graph(
            figure=px.bar(
                average_sales,
                x='Vehicle_Type',
                y='Automobile_Sales',
                title='Average Automobile Sales by Vehicle Type during Recession'
            )
        )

        exp_rec = recession_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
        R_chart3 = dcc.Graph(
            figure=px.pie(
                exp_rec,
                values='Advertising_Expenditure',
                names='Vehicle_Type',
                title='Advertising Expenditure Share by Vehicle Type during Recession'
            )
        )

        unemp_data = recession_data.groupby(
            ['unemployment_rate', 'Vehicle_Type']
        )['Automobile_Sales'].mean().reset_index()

        R_chart4 = dcc.Graph(
            figure=px.bar(
                unemp_data,
                x='unemployment_rate',
                y='Automobile_Sales',
                color='Vehicle_Type',
                labels={
                    'unemployment_rate': 'Unemployment Rate',
                    'Automobile_Sales': 'Average Automobile Sales'
                },
                title='Effect of Unemployment Rate on Vehicle Type and Sales'
            )
        )

        return [
            html.Div(
                className='chart-item',
                children=[R_chart1, R_chart2],
                style={'display': 'flex'}
            ),
            html.Div(
                className='chart-item',
                children=[R_chart3, R_chart4],
                style={'display': 'flex'}
            )
        ]

    # ================= YEARLY STATISTICS =================
    elif selected_statistics == 'Yearly Statistics' and selected_year != 'Select-year':

        yearly_data = data[data['Year'] == selected_year]

        yas = data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        Y_chart1 = dcc.Graph(
            figure=px.line(
                yas,
                x='Year',
                y='Automobile_Sales',
                title='Average Automobile Sales over the years'
            )
        )

        mas = data.groupby('Month')['Automobile_Sales'].mean().reset_index()
        Y_chart2 = dcc.Graph(
            figure=px.line(
                mas,
                x='Month',
                y='Automobile_Sales',
                title='Total Monthly Automobile Sales'
            )
        )

        avr_vdata = yearly_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
        Y_chart3 = dcc.Graph(
            figure=px.bar(
                avr_vdata,
                x='Vehicle_Type',
                y='Automobile_Sales',
                title=f'Average Vehicles Sold by Vehicle Type in {selected_year}'
            )
        )

        exp_data = yearly_data.groupby('Vehicle_Type')['Advertising_Expenditure'].mean().reset_index()
        Y_chart4 = dcc.Graph(
            figure=px.pie(
                exp_data,
                values='Advertising_Expenditure',
                names='Vehicle_Type',
                title='Total Advertisement Expenditure by Vehicle Type'
            )
        )

        return [
            html.Div(
                className='chart-item',
                children=[Y_chart1, Y_chart2],
                style={'display': 'flex'}
            ),
            html.Div(
                className='chart-item',
                children=[Y_chart3, Y_chart4],
                style={'display': 'flex'}
            )
        ]

    return None

# ---------------------------------------------------------------------------------------
# Run the app
if __name__ == '__main__':
    app.run(debug=True)
