import datetime

import streamlit as st

import plot


def sidebar_date():
    st.sidebar.write('Datum eingrenzen')

    startdate = st.sidebar.date_input('vom', value=datetime.date(2012, 1, 1))
    enddate = st.sidebar.date_input('bis', value=(datetime.date.today() - datetime.timedelta(1)))

    return startdate, enddate

def sidebar_time():
    hours = ['00:00:00',
             '01:00:00',
             '02:00:00',
             '03:00:00',
             '04:00:00',
             '05:00:00',
             '06:00:00',
             '07:00:00',
             '08:00:00',
             '09:00:00',
             '10:00:00',
             '11:00:00',
             '12:00:00',
             '13:00:00',
             '14:00:00',
             '15:00:00',
             '16:00:00',
             '17:00:00',
             '18:00:00',
             '19:00:00',
             '20:00:00',
             '21:00:00',
             '22:00:00',
             '23:00:00',
             ]
    starttime, endtime = st.sidebar.select_slider('Tageszeit eingrenzen', options=hours,
                                                                          value=('00:00:00', '23:00:00'),
                                                                          key='Time_slider')

    return starttime, endtime

def data_options():
    st.sidebar.markdown('Optionen')

    st.sidebar.markdown('Datenvorverarbeitung')

    outliers_option = st.sidebar.radio('Außreißer Optionen', ('Behalte Ausreißer','Entferne Ausreißer', 'Ersetze Ausreißer mit Mittelwerten'))

    if outliers_option == 'Behalte Ausreißer':
        remove_outliers_option = False
        fill_outliers_option = False
    if outliers_option == 'Entferne Ausreißer':
        remove_outliers_option = True
        fill_outliers_option = False
    if outliers_option == 'Ersetze Ausreißer mit Mittelwerten':
        remove_outliers_option = False
        fill_outliers_option = True

    st.sidebar.write('Fehlende Werte')
    fill_missing_index_option = st.sidebar.checkbox('Ersetze fehlende Messzeitpunkte mit Mittelwerten', value=False)
    fill_missing_values_option = st.sidebar.checkbox('Ersetze fehlende Messwerte mit Mittelwerten', value=False)

    return remove_outliers_option, fill_outliers_option, fill_missing_index_option, fill_missing_values_option

def sidebar_station_select(dataframe_list):
    station_names = [dataframe.columns[0] for dataframe in dataframe_list]

    station_dict = {}

    for key in station_names:
        for value in dataframe_list:
            station_dict[key] = value
            dataframe_list.remove(value)
            break

    stationID = st.sidebar.multiselect('Radzählstation', station_names, default='Wilhelm-Kaisen-Brücke (Ost)')

    selected_dfs = [station_dict.get(i) for i in stationID]
    return selected_dfs

def sidebar_graph_select():
    selected_graph = st.sidebar.radio('Diagrammtyp',['Info',
                                                        'Übersicht',
                                                        'Kumulationen',
                                                        'Tagesverlauf',
                                                        'gleitender Mittelwert',
                                                        'Saison-Trend-Zerlegung',
                                                        'Oberflächendiagramm',
                                                        'Radverkehr und Wetter'
                                                        ])
    return selected_graph

def stl_options():
    st.sidebar.markdown('**Diagrammoptionen**')
    resample_option = st.sidebar.selectbox('Abtastrate/Funktion', ('täglich/Summe', 'täglich/Mittelwert', 'monatlich/Summe', 'monatlich/Mittelwert'))
    robust_option = st.sidebar.selectbox('Robustheit', ('robust', 'non robust'))
    return resample_option, robust_option

def surface_options():
    st.sidebar.markdown('**Diagrammoptionen**')
    plot_option = st.sidebar.selectbox('Typ', ('Jahr/Monat', 'Wochen/Stunden'))
    calc_option = st.sidebar.selectbox('Summen/Mittelwerte', ('Summen', 'Mittelwerte'))
    if calc_option == 'Summen':
        calc_option = 'sum'
    elif calc_option == 'Mittelwerte':
        calc_option = 'mean'
    return  plot_option, calc_option

def ma_options(dataframe):
    st.sidebar.markdown('**Diagrammoptionen**')
    moving_average_window = st.sidebar.slider(
        'Größe des sich bewegenden Fensters. Enthält die Anzahl der Beobachtungen, die zur Berechnung gleitenden Mittelwertes verwendet werden.', min_value=0, max_value=int(dataframe.count()[0] / 24))
    moving_average_period = st.sidebar.slider('Erforderliche Mindestanzahl von Beobachtungen im oben definierten Fenster.', min_value=0,
                                              max_value=int(dataframe.count()[0] / 24))

    return moving_average_window, moving_average_period






