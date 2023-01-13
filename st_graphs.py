import streamlit as st
import streamlit.components.v1 as components
import pandas
import plot
import preprocess
import st_elements
import st_infotext

class get_values(object):
    def __init__(self, dataframe):
        self.index_date_min = dataframe.index.min().strftime('%d-%m-%Y')
        self.index_date_max = dataframe.index.max().strftime('%d-%m-%Y')
        self.index_time_min = dataframe.index.min().strftime('%H:%M')
        self.index_time_max = dataframe.index.max().strftime('%H:%M')

        self.max = '{:,.0f}'.format(dataframe.max()[0])

        self.idxmax_date = dataframe.idxmax()[0].strftime('%d-%m-%Y')
        self.idxmax_time = dataframe.idxmax()[0].strftime('%H:%M')

        self.stats = self.stats(dataframe)

    def stats(self, dataframe):
        col = dataframe.columns[0]
        vals = dataframe.describe().values
        index = ['Anzahl der Messwerte', 'Mittelwert', 'Standardabweichung', 'Minimum', '25% Perzentil',
                 '50% Perzentil', '75% Perzentil', 'Maximum']
        stats = pandas.DataFrame(index=index)
        stats[col] = vals
        return stats


class SelectGraph():
    def __init__(self):
        self.info = self.info()
        self.overview = self.overview()
        self.week_dist = self.week_dist()

    def info():
        st.header('Das inoffizielle Bremer Radzählstationen Analysetool')
        st.markdown('by M o i n S t e f k o')

        src = '<iframe width="100%" height="600px" frameborder="0" allowfullscreen src="//umap.openstreetmap.fr/de/map/unbenannte-karte_570969?scaleControl=false&miniMap=false&scrollWheelZoom=false&zoomControl=true&allowEdit=false&moreControl=true&searchControl=null&tilelayersControl=null&embedControl=null&datalayersControl=true&onLoadPanel=undefined&captionBar=false"></iframe>'
        components.html(src, height=600, scrolling=False)

        st.write(
            'Das inoffizielle Radstationen Analysetool wurde entwickelt, um interessierten Benutzer*innen einen tieferen Einblick in die Daten der Bremer Radzählstationen (https://vmz.bremen.de/radzaehlstationen/) zu geben. Hierfür stehen verschiedene Diagrammtypen als Werkzeuge zu Verfügung. Darüber hinaus werden die Daten der Radzählstationen Daten des Deutschen Wetterdienstes (www.dwd.de) verknüpft.')
        st.write(
            'An der linken Bildschirmleiste befindet sich das Optionsmenü. Hier können die Grundeinstellungen zu den Radzählstationen, dem Zeitraum und des Diagrammtyps vorgenommen werden. Je nach gewähltem Diagrammtyp stehen weitere Optionen zu Verfügung.')

        with st.expander('Stationstabelle / Beginn der Messungen'):
            Stationstabelle = {'Stationsname': ['Wilhelm-Kaisen-Brücke (West)',
                                                'Wilhelm-Kaisen-Brücke (Ost)',
                                                'Langemarckstraße (Ostseite)',
                                                'Langemarckstraße (Westseite)',
                                                'Radweg Kleine Weser',
                                                'Graf-Moltke-Straße (Ostseite)',
                                                'Graf-Moltke-Straße (Westseite)',
                                                'Hastedter Brückenstraße',
                                                'Schwachhauser Ring',
                                                'Wachmannstraße auswärts (Süd)',
                                                'Wachmannstraße einwärts (Nord)',
                                                'Osterdeich',
                                                ],
                    'Erster Messwert > 0 am' : ['2012-01-01 00:00:00',
                                                '2012-01-01 00:00:00',
                                                '2012-03-14 11:00:00',
                                                '2012-04-23 13:00:00',
                                                '2012-04-18 11:00:00',
                                                '2012-04-16 13:00:00',
                                                '2012-04-16 11:00:00',
                                                '2012-04-25 12:00:00',
                                                '2012-03-14 05:00:00',
                                                '2012-04-24 15:00:00',
                                                '2012-04-24 12:00:00',
                                                '2012-04-17 11:00:00',
                                                ]}
            stationstabelle = pandas.DataFrame(Stationstabelle)
            stationstabelle.set_index(stationstabelle.Stationsname, inplace=True)
            stationstabelle = stationstabelle.drop(columns={stationstabelle.columns[0]})
            st.markdown('Tabelle der Radzählstationen und Zeitpunkt des ersten Wertes größer als Null:')
            st.table(stationstabelle)

        st.write('Quelle Radverkehrsdaten: [VerkehrsManagementZentrale Bremen](https://vmz.bremen.de/rad/radzaehlstationen-abfrage)')
        st.write('Quelle Wetterdaten: [Deutscher Wetterdienst](https://www.dwd.de)')

        st.write('©2022 www.moin-stefko.de / mail: hallo@moin-stefko.de')


    def overview(dataframe_list):
        st.header('Übersicht')
        for dataframe in dataframe_list:
            x = get_values(dataframe)

            st.subheader(dataframe.columns[0])
            st.write(f'vom {x.index_date_min} bis {x.index_date_max}, zwischen {x.index_time_min} Uhr und {x.index_time_max} Uhr.')
            st.write(f'Maximalwert: {x.max}, am {x.idxmax_date} um {x.idxmax_time} Uhr')

            st.line_chart(dataframe)

            with st.expander('Statistische Grundwerte'):
                st.write('Statistische Grundwerte')
                st.dataframe(data=x.stats, use_container_width=True)

            with st.expander('Daten'):
                st.dataframe(dataframe.style.highlight_max(axis=0))

    def cumsum(dataframe_list):
        st.header('Kumulierte Summen')
        st.write('Zeigt das aufsummierte Radverkehrsaufkommen an.')
        with st.expander('Mehr Informationen'):
            st.write(st_infotext.method_info.cumsum)
        for dataframe in dataframe_list:
            x = get_values(dataframe)

            st.subheader(dataframe.columns[0])
            st.write(f'{x.index_date_min} bis {x.index_date_max} zwischen {x.index_time_min} Uhr und {x.index_time_max} Uhr')

            fig = plot.linechart_cumsum(dataframe)
            st.plotly_chart(fig, theme="streamlit", use_container_width=True)

    def week_dist(dataframe_list):
        st.header('Radverkehr im Tagesverlauf')
        st.write('Die Diagramme zeigen das durchschnittliche Radverkehrsaufkommen zur jeweiligen Uhrzeit an den Wochentagen, bzw. Werktagen und Wochenendtagen an.')
        for dataframe in dataframe_list:
            x = get_values(dataframe)

            st.subheader(dataframe.columns[0])
            st.write(f'vom {x.index_date_min} bis {x.index_date_max}, zwischen {x.index_time_min} Uhr und {x.index_time_max} Uhr.')

            st.write('Wochentage')
            fig, dataframe_first_monday, dataframe_last_sunday = plot.weekdays(dataframe)
            st.plotly_chart(fig, theme="streamlit", use_container_width=True)

            st.write('Werktage & Wochenende')
            fig = plot.week_dist(dataframe)
            st.plotly_chart(fig, theme="streamlit", use_container_width=True)


    def stl(dataframe_list):
        st.header('Saison-Trend-Zerlegung')
        st.write('Zerlegt die Zeitreihe in Trend-, Saison- und Restkomponenten unter Verwendung einer lokalen linearen Kernregression.')
        with st.expander('Mehr Informationen'):
            st.write(st_infotext.method_info.stl)

        resample_option, robust_option = st_elements.stl_options()

        for dataframe in dataframe_list:
            trend, seasonal, resid = plot.stl(dataframe, resample_option, robust_option)

            x = get_values(dataframe)

            st.subheader(dataframe.columns[0])
            st.write(f'vom {x.index_date_min} bis {x.index_date_max}, zwischen {x.index_time_min} Uhr und {x.index_time_max} Uhr.')

            st.line_chart(trend)

            with st.expander('Zeige Saisonkomponente'):
                st.line_chart(seasonal)
            with st.expander('Zeige Residuen'):
                st.line_chart(resid)
            with st.expander('Zeige Daten'):
                data_to_show = pandas.merge(pandas.merge(trend, seasonal, left_index=True, right_index=True, how='outer'),
                                        resid, left_index=True, right_index=True, how='outer')
                data_to_show[dataframe.columns[0]] = data_to_show.sum(axis=1).round()
                st.write(data_to_show)

    def surface(dataframe_list):
        st.header('Oberflächendiagramm')
        st.write('Stellt das Radverkehrsaufkommen als Oberfläche dar.')
        plot_option, calc_option = st_elements.surface_options()

        for dataframe in dataframe_list:
            x = get_values(dataframe)

            st.subheader(dataframe.columns[0])
            st.write(f'vom {x.index_date_min} bis {x.index_date_max}, zwischen {x.index_time_min} Uhr und {x.index_time_max} Uhr.')

            if plot_option == 'Jahr/Monat':
                fig = plot.surface.year_month(dataframe, calc_option)
                st.write(fig)
            if plot_option == 'Wochen/Stunden':
                fig = plot.surface.week_hour(dataframe, calc_option)
                st.write(fig)

    def moving_av(dataframe_list):
        st.header('Gleitdender Mittelwert')
        st.write('Zeigt den gleitenden Mittelwert der Zeitreihe als Kurve an.')
        for dataframe in dataframe_list:
            x = get_values(dataframe)

            st.subheader(dataframe.columns[0])
            st.write(f'vom {x.index_date_min} bis {x.index_date_max}, zwischen {x.index_time_min} Uhr und {x.index_time_max} Uhr.')

            window, periods = st_elements.ma_options(dataframe)
            try:
                fig = plot.moving_av(dataframe, window, periods)
                st.plotly_chart(fig, theme="streamlit", use_container_width=True)
            except ValueError:
                st.warning(f'Fehler! Größe des sich bewegenden Fensters muss kleiner sein als die erforderliche Mindestanzahl von Beobachtungen im Fenster. Du hast {window} als Größe für das fenster und{periods} als Mindestanzahl der Messwerte im Fenster ausgewählt.', icon='⚠️')

    def wetter(dataframe_list):
        st.header('Radverkehr und Wetter')
        st.write('Zeigt das Radverkehrsaufkommen in Kombination mit den Temperatur- und Niederschlagsdaten des Deutschen' \
             ' Wetterdienst an.')
        with st.expander('Mehr Informationen'):
            st.write(st_infotext.method_info.wetter)
        for dataframe in dataframe_list:
            x = get_values(dataframe)

            st.subheader(dataframe.columns[0])
            st.write(f'vom {x.index_date_min} bis {x.index_date_max}, zwischen {x.index_time_min} Uhr und {x.index_time_max} Uhr.')

            wetter_start = str(dataframe.index.min())
            wetter_end = str(dataframe.index.max())

            wetter = preprocess.get_weather(wetter_start, wetter_end, 691)

            bikewetter = pandas.merge(dataframe, wetter, left_index=True, right_index=True, how='outer')

            st.write('Radverkehr und Temperatur')
            fig = plot.radverkehr_temperatur(bikewetter, 'D')
            st.plotly_chart(fig, theme="streamlit", use_container_width=True)

            st.write('Radverkehr und Niederschlag')
            fig = plot.radverkehr_niederschlag(bikewetter, 'D')
            st.plotly_chart(fig, theme="streamlit", use_container_width=True)

            st.write('Quelle Wetterdaten: dwd.de')

    def sankey(dataframe_list):
        st.header('Zusammensetzung Radverkehrsaufkommen')
        st.write('Zeigt den Anteil der Radzählstationen am gemessenen Radverkehrsaufkommen.')
        with st.expander('Mehr Informationen'):
            st.write(st_infotext.method_info.sankey)
            st.info('Hinweis: Die Auswahl von Radzählstationen hat keinen Einfluss auf die Darstellung.', icon='ℹ️')

        fig = plot.sankey(dataframe_list)
        st.plotly_chart(fig, theme="streamlit", use_container_width=True)






