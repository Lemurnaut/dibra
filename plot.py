import pandas
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from statsmodels.tsa.seasonal import STL
import datetime as dt
from functools import reduce


class surface():
    def year_month(dataframe, calc_option):
        dataframe_to_plot = dataframe.groupby([dataframe.index.year, dataframe.index.month]).agg(calc_option)
        dataframe_to_plot = dataframe_to_plot.unstack()

        fig = go.Figure(data=[
            go.Surface(z=dataframe_to_plot.values,
                       hovertemplate='Jahr: %{y}<br>Monat: %{x}<br>Anzahl: %{z}<extra></extra>')])
        fig.update_layout(scene=dict(
            yaxis=dict(
                title='Jahr',
                ticktext=dataframe_to_plot.index.unique().astype(str).tolist(),
                tickvals=list(range(len(dataframe_to_plot.index.unique()))),
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

        dataframe_to_plot = dataframe.groupby([dataframe.index.isocalendar().week, dataframe.index.month]).sum()
        dataframe_to_plot = dataframe_to_plot.unstack()

        fig = go.Figure(data=[go.Surface(z=dataframe_to_plot.values,
                                         hovertemplate='Monat: %{x}<br>Stunde: %{y} Uhr<br>Anzahl: %{z}<extra></extra>')])
        fig.update_layout(scene=dict(
            xaxis=dict(
                title='Monat',
                ticktext=['JAN', 'FEB', 'MÄR', 'APR', 'MAI', 'JUN', 'JUL', 'AUG', 'SEP', 'OKT', 'NOV', 'DEZ'],
                tickvals=list(range(len(dataframe_to_plot.columns))),
                tickmode='array'
            ),

            yaxis=dict(
                title='Stunde',
                ticktext=dataframe_to_plot.index.unique().astype(str).tolist(),
                tickvals=list(range(len(dataframe_to_plot.index.unique()))),
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

        dataframe_to_plot = dataframe.groupby([dataframe.index.hour, dataframe.index.isocalendar().week]).sum()
        dataframe_to_plot = dataframe_to_plot.unstack()

        fig = go.Figure(data=[go.Surface(z=dataframe_to_plot.values,
                                         hovertemplate='Woche: %{x}<br>Stunde: %{y} Uhr<br>Anzahl: %{z}<extra></extra>')])
        fig.update_layout(scene=dict(
            xaxis=dict(
                title='Woche',
                tickvals=list(range(len(dataframe_to_plot.columns))),
                tickmode='array'
            ),

            yaxis=dict(
                title='Stunde',
                ticktext=dataframe_to_plot.index.unique().astype(str).tolist(),
                tickvals=list(range(len(dataframe_to_plot.index.unique()))),
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
    """


    """
    fig = px.line(dataframe.cumsum(), hover_data={'variable': False})

    fig.update_layout(legend_title_text='')
    fig.update_layout(xaxis_title='Zeit', yaxis_title='Kumuliertes Radverkehrsaufkommen')

    fig.update_traces(hovertemplate='Zeit: %{x}<br>' +
                                    'Anzahl: %{y}<br>'
                      )

    fig.update_layout(showlegend=False)

    return fig


def linechart(dataframe):
    """
    """
    fig = go.Figure()

    fig.add_trace(
        go.Scatter(x=list(dataframe.index), y=list(dataframe.iloc[:, 0])),
    )

    fig.update_layout(
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=1,
                         label="1 Monat",
                         step="month",
                         stepmode="backward"),
                    dict(count=6,
                         label="6 Monate",
                         step="month",
                         stepmode="backward"),
                    dict(count=1,
                         label="aktuelles Jahr",
                         step="year",
                         stepmode="todate"),
                    dict(count=1,
                         label="1 Jahr",
                         step="year",
                         stepmode="backward"),
                    dict(step="all",
                         label='Alles')
                ])
            ),
            rangeslider=dict(
                visible=True
            ),
            type="date"
        )
    )

    fig.add_annotation(x=dataframe.idxmax()[0].strftime('%Y-%m-%d %H:%M:%S'), y=dataframe.max()[0],
                       text='Maximum',
                       showarrow=True,
                       arrowhead=1)

    fig.update_layout(legend_title_text='')
    fig.update_layout(xaxis_title='Zeit', yaxis_title='Radverkehrsaufkommen')
    fig.update_layout(height=580)

    return fig


def stl(dataframe, resample_option, robust_option):
    res_robust = None
    res_non_robust = None

    if robust_option == 'robust':
        robust_option = True
    elif robust_option == 'non robust':
        robust_option = False

    if resample_option == 'täglich/Summe':
        res_robust = STL(dataframe.iloc[:, 0].resample('D').sum(), robust=robust_option).fit()
        res_non_robust = STL(dataframe.iloc[:, 0].resample('D').sum(), robust=robust_option).fit()

    elif resample_option == 'täglich/Mittelwert':
        res_robust = STL(dataframe.iloc[:, 0].resample('D').mean(), robust=robust_option).fit()
        res_non_robust = STL(dataframe.iloc[:, 0].resample('D').mean(), robust=robust_option).fit()

    elif resample_option == 'monatlich/Summe':
        print(dtype(dataframe.iloc[:, 0].resample('M').sum())
        res_robust = STL(dataframe.iloc[:, 0].resample('M').sum(), robust=robust_option).fit()
        res_non_robust = STL(dataframe.iloc[:, 0].resample('M').sum(), robust=robust_option).fit()

    elif resample_option == 'monatlich/Mittelwert':
        res_robust = STL(dataframe.iloc[:, 0].resample('M').mean(), robust=robust_option).fit()
        res_non_robust = STL(dataframe.iloc[:, 0].resample('M').mean(), robust=robust_option).fit()

    if robust_option == True:
        dataframe_to_plot = res_robust

    elif robust_option == False:
        dataframe_to_plot = res_non_robust

    trend = px.line(dataframe_to_plot.trend, hover_data={'variable': False})
    trend.update_layout(legend_title_text='')
    trend.update_layout(xaxis_title='Zeit', yaxis_title='Wert')
    trend.update_traces(hovertemplate='Zeit: %{x}<br>' +
                                      'Wert: %{y}<br>'
                        )
    trend.update_layout(showlegend=False)

    seasonal = px.line(dataframe_to_plot.seasonal, hover_data={'variable': False})

    seasonal.update_layout(legend_title_text='')
    seasonal.update_layout(xaxis_title='Zeit', yaxis_title='Wert')
    seasonal.update_traces(hovertemplate='Zeit: %{x}<br>' +
                                         'Wert: %{y}<br>'
                           )
    seasonal.update_layout(showlegend=False)

    resid = px.line(dataframe_to_plot.resid, hover_data={'variable': False})
    resid.update_layout(legend_title_text='')
    resid.update_layout(xaxis_title='Zeit', yaxis_title='Wert')

    resid.update_traces(hovertemplate='Zeit: %{x}<br>' +
                                      'Wert: %{y}<br>'
                        )
    resid.update_layout(showlegend=False)

    return trend, seasonal, resid, dataframe_to_plot


def radverkehr_niederschlag(dataframe):
    fig = px.scatter_3d(dataframe, x=dataframe.index, z=str(dataframe.columns.values[1]), color='Niederschlag',
                        y=str(dataframe.columns.values[0]),
                        color_continuous_scale=px.colors.sequential.Jet, height=800
                        )

    fig.update_traces(hovertemplate='Datum: %{x} <br>' + 'Anzahl: %{y} <br>' + 'Niederschlag: %{z}')

    fig.update_traces(hoverinfo='all')
    fig.update_layout(width=1600, height=850, margin=dict(r=10, l=10, b=10, t=10))

    return fig


def radverkehr_temperatur(dataframe):
    fig = px.scatter_3d(dataframe, x=dataframe.index, z=str(dataframe.columns.values[2]), color='Temperatur',
                        y=str(dataframe.columns.values[0]),
                        color_continuous_scale=px.colors.sequential.Jet, height=800
                        )

    fig.update_traces(hovertemplate='Datum: %{x} <br>' + 'Anzahl: %{y} <br>' + 'Temperatur: %{z}')

    fig.update_traces(hoverinfo='all')
    fig.update_layout(width=1600, height=850, margin=dict(r=10, l=10, b=10, t=10))

    return fig


def sankey(dataframe_list):
    tmp_frame = reduce(lambda a, b: a.add(b, fill_value=0), dataframe_list)
    sum_all_stations = pandas.DataFrame(tmp_frame.sum(axis=1)).sum()[0]
    del tmp_frame

    label = ['Wilhelm-Kaisen-Brücke (Ost)',  # 0
             'Wilhelm-Kaisen-Brücke (West)',  # 1
             'Langemarckstraße (Ostseite)',  # 2
             'Langemarckstraße (Westseite)',  # 3
             'Radweg Kleine Weser',  # 4
             'Graf-Moltke-Straße (Ostseite)',  # 5
             'Graf-Moltke-Straße (Westseite)',  # 6
             'Schwachhauser Ring',  # 7
             'Wachmannstraße auswärts (Süd)',  # 8
             'Wachmannstraße einwärts (Nord)',  # 9
             'Osterdeich',  # 10
             'Hastedter Brückenstraße',  # 11

             'Wilhelm-Kaisen-Brücke',  # 12
             'Langemarckstraße',  # 13
             'Graf-Moltke-Straße',  # 14
             'Wachmannstraße',  # 15

             'Gesamtaufkommen alle Stationen'  # last node (sum of all stations)
             ]

    color = ['rgba(25, 55, 55, 0.5)',  # 0
             'rgba(25, 55, 55, 0.25)',  # 1
             'rgba(25, 55, 55, 0.5)',  # 2
             'rgba(25, 55, 55, 0.25)',  # 3
             'rgba(25, 55, 55, 0.6)',  # 4
             'rgba(25, 55, 55, 0.5)',  # 5
             'rgba(25, 55, 55, 0.25)',  # 6
             'rgba(25, 55, 55, 0.6)',  # 7
             'rgba(25, 55, 55, 0.5)',  # 8
             'rgba(25, 55, 55, 0.25)',  # 9
             'rgba(25, 55, 55, 0.6)',  # 10
             'rgba(25, 55, 55, 0.6)',  # 11
             'rgba(25, 55, 55, 0.6)',  # 12
             'rgba(25, 55, 55, 0.6)',  # 13
             'rgba(25, 55, 55, 0.6)',  # 14
             'rgba(25, 55, 55, 0.6)',  # 15
             'rgba(25, 55, 55, 0.8)'  # last node (sum of all stations)
             ]

    source = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11,
              12, 13, 14, 15
              ]
    target = [12, 12, 13, 13, 16, 14, 14, 16, 15, 15, 16, 16,
              16, 16, 16, 16
              ]
    value = [dataframe_list[0].sum()[0],  # 0
             dataframe_list[1].sum()[0],  # 1
             dataframe_list[2].sum()[0],  # 2
             dataframe_list[3].sum()[0],  # 3
             dataframe_list[4].sum()[0],  # 4
             dataframe_list[5].sum()[0],  # 5
             dataframe_list[6].sum()[0],  # 6
             dataframe_list[7].sum()[0],  # 7
             dataframe_list[8].sum()[0],  # 8
             dataframe_list[9].sum()[0],  # 9
             dataframe_list[10].sum()[0],  # 10
             dataframe_list[11].sum()[0],  # 11

             dataframe_list[0].sum()[0] + dataframe_list[1].sum()[0],  # 12
             dataframe_list[2].sum()[0] + dataframe_list[3].sum()[0],  # 13
             dataframe_list[5].sum()[0] + dataframe_list[6].sum()[0],  # 14
             dataframe_list[8].sum()[0] + dataframe_list[9].sum()[0],  # 15
             ]

    customdata_node = [dataframe_list[0].columns[0],  # 0
                       dataframe_list[1].columns[0],  # 1
                       dataframe_list[2].columns[0],  # 2
                       dataframe_list[3].columns[0],  # 3
                       dataframe_list[4].columns[0],  # 4
                       dataframe_list[5].columns[0],  # 5
                       dataframe_list[6].columns[0],  # 6
                       dataframe_list[7].columns[0],  # 7
                       dataframe_list[8].columns[0],  # 8
                       dataframe_list[9].columns[0],  # 9
                       dataframe_list[10].columns[0],  # 10
                       dataframe_list[11].columns[0],  # 11
                       'Wilhelm-Kaisen-Brücke (Gesamt)',  # 12
                       'Langemarckstraße (Gesamt)',  # 13
                       'Graf-Moltke-Straße (Gesamt)',  # 14
                       'Wachmannstraße (Gesamt)',  # 15
                       'Alle Stationen'  # last node (sum of all stations)
                       ]

    customdata_link = [(value[0] * 100 / value[12]).round(),  # 0
                       (value[1] * 100 / value[12]).round(),  # 1
                       (value[2] * 100 / value[13]).round(),  # 2
                       (value[3] * 100 / value[13]).round(),  # 3
                       (value[4] * 100 / sum_all_stations).round(),  # 4
                       (value[5] * 100 / value[14]).round(),  # 5
                       (value[6] * 100 / value[14]).round(),  # 6
                       (value[7] * 100 / sum_all_stations).round(),  # 7
                       (value[8] * 100 / value[15]).round(),  # 8
                       (value[9] * 100 / value[15]).round(),  # 9
                       (value[10] * 100 / sum_all_stations).round(),  # 10
                       (value[11] * 100 / sum_all_stations).round(),  # 11
                       (value[12] * 100 / sum_all_stations).round(),  # 12
                       (value[13] * 100 / sum_all_stations).round(),  # 13
                       (value[14] * 100 / sum_all_stations).round(),  # 14
                       (value[15] * 100 / sum_all_stations).round(),  # 15
                       ]

    fig = go.Figure(data=[go.Sankey(
        node=dict(
            pad=10,
            thickness=20,
            line=dict(color="black", width=0.1),
            label=label,
            color=color,
            customdata=customdata_node,
            hovertemplate='%{customdata} <br>' +
                          'gemessenes Aufkommen:%{value}<extra></extra>'
        ),
        link=dict(
            source=source,  # indices correspond to labels, eg A1, A2, A1, B1, ...
            target=target,
            value=value,
            color=color,
            customdata=customdata_link,
            hovertemplate='Anteil an %{target.customdata}: %{customdata} Prozent<extra></extra>',

        ))])

    fig.update_layout(hovermode='x')

    fig.update_layout(height=800)

    return fig
