import pandas
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from statsmodels.tsa.seasonal import STL
import datetime as dt

class surface():
    def year_month(dataframe, calc_option):

        dataframe = dataframe.groupby([dataframe.index.year, dataframe.index.month]).agg(calc_option)
        dataframe = dataframe.unstack()

        fig = go.Figure(data=[
            go.Surface(z=dataframe.values, hovertemplate='Jahr: %{y}<br>Monat: %{x}<br>Anzahl: %{z}<extra></extra>')])
        fig.update_layout(scene=dict(
            yaxis=dict(
                title='Jahr',
                ticktext=dataframe.index.unique().astype(str).tolist(),
                tickvals=list(range(len(dataframe.index.unique()))),
                tickmode='array'
            ),
            xaxis=dict(
                title='Monat',
                ticktext=['JAN', 'FEB', 'MÄR', 'APR', 'MAI', 'JUN', 'JUL', 'AUG', 'SEP', 'OKT', 'NOV', 'DEZ'],
                tickvals=list(range(len(dataframe.columns))),
                tickmode='array'
            ),
            zaxis=dict(
                title='Anzahl'
            ),
        ),
            width=1600,
            height=850,
            margin=dict(r=10, l=10, b=10, t=10
                        ))
        return fig

    def month_week(dataframe, calc_option):
        import plotly.graph_objects as go

        dataframe = dataframe.groupby([dataframe.index.isocalendar().week, dataframe.index.month]).sum()
        dataframe = dataframe.unstack()

        fig = go.Figure(data=[go.Surface(z=dataframe.values,
                                         hovertemplate='Monat: %{x}<br>Stunde: %{y} Uhr<br>Anzahl: %{z}<extra></extra>')])
        fig.update_layout(scene=dict(
            xaxis=dict(
                title='Monat',
                ticktext=['JAN', 'FEB', 'MÄR', 'APR', 'MAI', 'JUN', 'JUL', 'AUG', 'SEP', 'OKT', 'NOV', 'DEZ'],
                tickvals=list(range(len(dataframe.columns))),
                tickmode='array'
            ),

            yaxis=dict(
                title='Stunde',
                ticktext=dataframe.index.unique().astype(str).tolist(),
                tickvals=list(range(len(dataframe.index.unique()))),
                tickmode='array'
            ),
            zaxis=dict(
                title='Anzahl'
            ),
        ),
            width=1600,
            height=850,
            margin=dict(r=10, l=10, b=10, t=10
                        ))
        return fig

    def week_hour(dataframe, calc_option):
        import plotly.graph_objects as go

        dataframe = dataframe.groupby([dataframe.index.hour, dataframe.index.isocalendar().week]).sum()
        dataframe = dataframe.unstack()

        fig = go.Figure(data=[go.Surface(z=dataframe.values,
                                         hovertemplate='Woche: %{x}<br>Stunde: %{y} Uhr<br>Anzahl: %{z}<extra></extra>')])
        fig.update_layout(scene=dict(
            xaxis=dict(
                title='Woche',
                tickvals=list(range(len(dataframe.columns))),
                tickmode='array'
            ),

            yaxis=dict(
                title='Stunde',
                ticktext=dataframe.index.unique().astype(str).tolist(),
                tickvals=list(range(len(dataframe.index.unique()))),
                tickmode='array'
            ),
            zaxis=dict(
                title='Anzahl'
            ),
        ),
            width=1600,
            height=850,
            margin=dict(r=10, l=10, b=10, t=10
                        ))
        return fig

def moving_av(dataframe, window, periods):
    ma = dataframe.resample('D').sum().rolling(window=window, center=True, min_periods=periods).mean()
    ma = ma.rename(columns={dataframe.columns[0]: 'gleitender Mittelwert'})
    ma = pandas.merge(dataframe.resample('D').sum(), ma, left_index=True, right_index=True, how='outer')
    dataframe = ma.rename(columns={dataframe.columns[0]: 'Aufkommen'})

    fig = px.line(dataframe, x=dataframe.index, y=['Aufkommen', 'gleitender Mittelwert'],
                  hover_data={'variable': False})

    fig.update_traces(hoverinfo='text+name', mode='lines+markers')
    fig.update_traces(hovertemplate='Anzahl: %{y}')

    fig.update_layout(hovermode="x")

    fig.update_layout(showlegend=False)
    fig.update_layout(xaxis_title='Zeit', yaxis_title='Radverkehrsaufkommen')
    return fig

def week_dist(dataframe):
    weekend = np.where(dataframe.index.weekday < 5, 'Weekday', 'Weekend')
    by_time = dataframe.groupby([weekend, dataframe.index.time]).mean().round()

    merge_1 = pandas.DataFrame(by_time.xs('Weekday'))
    merge_1 = merge_1.rename(columns={merge_1.columns[0]: 'Werktag'})
    merge_2 = pandas.DataFrame(by_time.xs('Weekend'))
    merge_2 = merge_2.rename(columns={merge_2.columns[0]: 'Wochenende'})

    dataframe = pandas.merge(merge_1, merge_2, left_index=True, right_index=True, how='outer')

    fig = px.line(dataframe, x=dataframe.index, y=['Werktag', 'Wochenende'], hover_data={'variable': False})

    fig.update_traces(hoverinfo='text+name', mode='lines+markers')
    fig.update_traces(hovertemplate='Anzahl: %{y}')

    fig.update_layout(hovermode="x")

    fig.update_layout(showlegend=False)
    fig.update_layout(xaxis_title='Zeit', yaxis_title='Durchschnittliches Radverkehrsaufkommen')

    return fig

def weekdays(dataframe):
    dataframe_startdate = dataframe.index.min()
    dataframe_enddate = dataframe.index.max()

    dataframe_first_monday = dataframe_startdate - dataframe_startdate.weekday() * dt.timedelta(days=1)
    dataframe_last_sunday = (dataframe_enddate - dataframe_enddate.weekday() * dt.timedelta(days=1)) + dt.timedelta(
        days=6)

    dataframe = dataframe.loc[dataframe_first_monday: dataframe_last_sunday]

    weekday = np.where(dataframe.index.weekday == 0, 'Montag', 'restofweek')
    monday = dataframe.groupby([weekday, dataframe.index.time]).mean().round()

    weekday = np.where(dataframe.index.weekday == 1, 'Dienstag', 'restofweek')
    tuesday = dataframe.groupby([weekday, dataframe.index.time]).mean().round()

    weekday = np.where(dataframe.index.weekday == 2, 'Mittwoch', 'restofweek')
    wednesday = dataframe.groupby([weekday, dataframe.index.time]).mean().round()

    weekday = np.where(dataframe.index.weekday == 3, 'Donnerstag', 'restofweek')
    thursday = dataframe.groupby([weekday, dataframe.index.time]).mean().round()

    weekday = np.where(dataframe.index.weekday == 4, 'Freitag', 'restofweek')
    friday = dataframe.groupby([weekday, dataframe.index.time]).mean().round()

    weekday = np.where(dataframe.index.weekday == 5, 'Sonnabend', 'restofweek')
    saturday = dataframe.groupby([weekday, dataframe.index.time]).mean().round()

    weekday = np.where(dataframe.index.weekday == 6, 'Sonntag', 'restofweek')
    sunday = dataframe.groupby([weekday, dataframe.index.time]).mean().round()

    merge_1 = pandas.DataFrame(monday.xs('Montag'))
    merge_1 = merge_1.rename(columns={merge_1.columns[0]: 'Montag'})

    merge_2 = pandas.DataFrame(tuesday.xs('Dienstag'))
    merge_2 = merge_2.rename(columns={merge_2.columns[0]: 'Dienstag'})

    merge_3 = pandas.DataFrame(wednesday.xs('Mittwoch'))
    merge_3 = merge_3.rename(columns={merge_3.columns[0]: 'Mittwoch'})

    merge_4 = pandas.DataFrame(thursday.xs('Donnerstag'))
    merge_4 = merge_4.rename(columns={merge_4.columns[0]: 'Donnerstag'})

    merge_5 = pandas.DataFrame(friday.xs('Freitag'))
    merge_5 = merge_5.rename(columns={merge_5.columns[0]: 'Freitag'})

    merge_6 = pandas.DataFrame(saturday.xs('Sonnabend'))
    merge_6 = merge_6.rename(columns={merge_6.columns[0]: 'Sonnabend'})

    merge_7 = pandas.DataFrame(sunday.xs('Sonntag'))
    merge_7 = merge_7.rename(columns={merge_7.columns[0]: 'Sonntag'})

    # start the merge orgy
    merge_tmp = pandas.merge(merge_1, merge_2, left_index=True, right_index=True, how='outer')
    merge_tmp = pandas.merge(merge_tmp, merge_3, left_index=True, right_index=True, how='outer')
    merge_tmp = pandas.merge(merge_tmp, merge_4, left_index=True, right_index=True, how='outer')
    merge_tmp = pandas.merge(merge_tmp, merge_5, left_index=True, right_index=True, how='outer')
    merge_tmp = pandas.merge(merge_tmp, merge_6, left_index=True, right_index=True, how='outer')
    dataframe = pandas.merge(merge_tmp, merge_7, left_index=True, right_index=True, how='outer')

    fig = px.line(dataframe, x=dataframe.index,
                  y=['Montag', 'Dienstag', 'Mittwoch', 'Donnerstag', 'Freitag', 'Sonnabend', 'Sonntag'],
                  hover_data={'variable': False})

    fig.update_traces(hoverinfo='text+name', mode='lines+markers')
    fig.update_traces(hovertemplate='Anzahl: %{y}')

    fig.update_layout(hovermode="x")

    fig.update_layout(showlegend=False)
    fig.update_layout(xaxis_title='Zeit', yaxis_title='Durchschnittliches Radverkehrsaufkommen')

    return fig, dataframe_first_monday, dataframe_last_sunday


def linechart_cumsum(dataframe):
    '''
    plotly linechart

    takes list of dataframes


    '''
    fig = px.line(dataframe.cumsum(), hover_data={'variable': False})

    fig.update_layout(legend_title_text='')
    fig.update_layout(xaxis_title='Zeit', yaxis_title='Kumuliertes Radverkehrsaufkommen')

    fig.update_traces(hovertemplate='Zeit: %{x}<br>' +
                                    'Anzahl: %{y}<br>'
                      )

    fig.update_layout(showlegend=False)

    return fig


def linechart(dataframe):
    '''
    '''
    fig = go.Figure()

    fig.add_trace(
        go.Scatter(x=list(dataframe.index), y=list(dataframe.iloc[:, 0])))

    fig.update_layout(
        title_text=dataframe.columns[0]
    )

    fig.update_layout(
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                        dict(count=1,
                             label="1m",
                             step="month",
                             stepmode="backward"),
                        dict(count=6,
                             label="6m",
                             step="month",
                             stepmode="backward"),
                        dict(count=1,
                             label="YTD",
                             step="year",
                             stepmode="todate"),
                        dict(count=1,
                             label="1y",
                             step="year",
                             stepmode="backward"),
                        dict(step="all")
                    ])
                ),
                rangeslider=dict(
                    visible=True
                ),
                type="date"
            ),
            template='none'
        )

    fig.add_annotation(x=dataframe.idxmax()[0].strftime('%Y-%m-%d %H:%M:%S'), y=dataframe.max()[0],
                           text='Maximum',
                           showarrow=True,
                           arrowhead=1)

    fig.update_layout(legend_title_text='')
    fig.update_layout(xaxis_title='Zeit', yaxis_title='Radverkehrsaufkommen')

    fig.update_layout(template='none')

    return fig


def stl(dataframe, resample_option, robust_option):
    if robust_option == 'robust':
        robust_option = True
    if robust_option == 'non robust':
        robust_option = False

    if resample_option == 'täglich/Summe':
        res_robust = STL(dataframe.iloc[:, 0].resample('D').sum(), robust=robust_option).fit()
        res_non_robust = STL(dataframe.iloc[:, 0].resample('D').sum(), robust=robust_option).fit()

    if resample_option == 'täglich/Mittelwert':
        res_robust = STL(dataframe.iloc[:, 0].resample('D').mean(), robust=robust_option).fit()
        res_non_robust = STL(dataframe.iloc[:, 0].resample('D').mean(), robust=robust_option).fit()

    if resample_option == 'monatlich/Summe':
        res_robust = STL(dataframe.iloc[:, 0].resample('M').sum(), robust=robust_option).fit()
        res_non_robust = STL(dataframe.iloc[:, 0].resample('M').sum(), robust=robust_option).fit()

    if resample_option == 'monatlich/Mittelwert':
        res_robust = STL(dataframe.iloc[:, 0].resample('M').mean(), robust=robust_option).fit()
        res_non_robust = STL(dataframe.iloc[:, 0].resample('M').mean(), robust=robust_option).fit()

    if robust_option == True:
        return res_robust.trend, res_robust.seasonal, res_robust.resid
    if robust_option == False:
        return res_non_robust.trend, res_non_robust.seasonal, res_non_robust.resid


def radverkehr_niederschlag(dataframe, resample_option):
    if resample_option == 'D':
        dataframe = dataframe.resample('D').agg({dataframe.columns.values[0]: 'sum', dataframe.columns.values[1]: 'sum',
                                                 dataframe.columns.values[2]: 'mean'})
    else:
        pass

    fig = px.scatter_3d(dataframe, x=dataframe.index, z=str(dataframe.columns.values[1]), color='Niederschlag',
                        y=str(dataframe.columns.values[0]),
                        color_continuous_scale=px.colors.sequential.Jet, height=800
                        )

    fig.update_traces(hovertemplate='Datum: %{x} <br>' + 'Anzahl: %{y} <br>' + 'Niederschlag: %{z}')

    fig.update_traces(hoverinfo='all')

    return fig


def radverkehr_temperatur(dataframe, resample_option):
    if resample_option == 'D':
        dataframe = dataframe.resample('D').agg({dataframe.columns.values[0]: 'sum', dataframe.columns.values[1]: 'sum',
                                                 dataframe.columns.values[2]: 'mean'}).round()
    else:
        pass

    fig = px.scatter_3d(dataframe, x=dataframe.index, z=str(dataframe.columns.values[2]), color='Temperatur',
                        y=str(dataframe.columns.values[0]),
                        color_continuous_scale=px.colors.sequential.Jet, height=800
                        )

    fig.update_traces(hovertemplate='Datum: %{x} <br>' + 'Anzahl: %{y} <br>' + 'Temperatur: %{z}')

    fig.update_traces(hoverinfo='all')

    return fig

def sankey(dataframe_list):
    label = ['Wilhelm-Kaisen-Brücke (Ost)',
             'Wilhelm-Kaisen-Brücke (West)',
             'Langemarckstraße (Ostseite)',
             'Langemarckstraße (Westseite)',
             'Radweg Kleine Weser',
             'Graf-Moltke-Straße (Ostseite)',
             'Graf-Moltke-Straße (Westseite)',
             'Schwachhauser Ring',
             'Wachmannstraße auswärts (Süd)',
             'Wachmannstraße einwärts (Nord)',
             'Osterdeich',
             'Hastedter Brückenstraße',

             'Wilhelm-Kaisen-Brücke',
             'Langemarckstraße',
             'Graf-Moltke-Straße',
             'Wachmannstraße',
            ]


    source = [0,1,2,3,4,5,6,7,8,9,10,11,
              12,13,14,15
             ]
    target = [12,12,13,13,16,14,14,16,15,15,16,16,
              16,16,16,16
             ]
    value = [dataframe_list[0].sum()[0],
             dataframe_list[1].sum()[0],
             dataframe_list[2].sum()[0],
             dataframe_list[3].sum()[0],
             dataframe_list[4].sum()[0],
             dataframe_list[5].sum()[0],
             dataframe_list[6].sum()[0],
             dataframe_list[7].sum()[0],
             dataframe_list[8].sum()[0],
             dataframe_list[9].sum()[0],
             dataframe_list[10].sum()[0],
             dataframe_list[11].sum()[0],

             dataframe_list[0].sum()[0] + dataframe_list[1].sum()[0],
             dataframe_list[2].sum()[0] + dataframe_list[3].sum()[0],
             dataframe_list[5].sum()[0] + dataframe_list[6].sum()[0],
             dataframe_list[8].sum()[0] + dataframe_list[9].sum()[0],
            ]


    fig = go.Figure(data=[go.Sankey(
        node = dict(
          pad = 10,
          thickness =20,
          line = dict(color = "black", width = 0.1),
          label = label,
          color = "grey",
        ),
        link = dict(
          source = source, # indices correspond to labels, eg A1, A2, A1, B1, ...
          target = target,
          value = value
      ))])

    fig.update_layout(hovermode = 'x')

    fig.update_layout(height=800)

    return fig





