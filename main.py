import streamlit as st
import st_elements
import st_graphs
import preprocess
import datetime as dt

version = '0.0.9_alpha'

# setup streamlit  menu and layout
menu_items = {
    'About': '''
    ## 
    Bremer Radzählstationen Analysetool

    made by stefko

    www.moin-stefko.de
    '''
    }
st.set_page_config(layout="wide",
                   menu_items=menu_items
                   )

col1, col2 = st.columns(2)


@st.experimental_memo
def download(end_date):
    dataframe = preprocess.download_data(end_date)  # end_date is required to get fresh data from VMZ server
    return dataframe


def main():
    dataframe_source = download(end_date=(dt.date.today()
                                          - dt.timedelta(1)
                                          )
                                )  # download data from VMZ
    dataframe_list_source = preprocess.dataframe_to_list(dataframe_source)  # make a list from orig dfs

    startdate, enddate = st_elements.sidebar_date()  # get start,end date from widget
    starttime, endtime = st_elements.sidebar_time()  # get start, end time from widget

    selected_dataframes = st_elements.sidebar_station_select(dataframe_list_source)  # get user input from widget
    selected_dataframes = [(dataframe.loc[startdate: enddate].between_time(starttime, endtime))
                           for dataframe in selected_dataframes]  # get user input

    graph_type = st_elements.sidebar_graph_select()  # get user input graph

    if graph_type == 'Info':
        st_graphs.SelectGraph.info()
    elif graph_type == 'Übersicht':
        st_graphs.SelectGraph.overview(selected_dataframes)
    elif graph_type == 'Kumulationen':
        st_graphs.SelectGraph.cumsum(selected_dataframes)
    elif graph_type == 'Tagesverlauf':
        st_graphs.SelectGraph.week_dist(selected_dataframes)
    elif graph_type == 'Saison-Trend-Zerlegung':
        st_graphs.SelectGraph.stl(selected_dataframes)
    elif graph_type == 'Oberflächendiagramm':
        st_graphs.SelectGraph.surface(selected_dataframes)
    elif graph_type == 'gleitender Mittelwert':
        st_graphs.SelectGraph.moving_av(selected_dataframes)
    elif graph_type == 'Radverkehr und Wetter':
        st_graphs.SelectGraph.wetter(selected_dataframes)
    elif graph_type == 'Sankey-Diagramm':
        sankey_source = preprocess.dataframe_to_list(dataframe_source)
        sankey_dataframes = [(dataframe.loc[startdate: enddate].between_time(starttime, endtime))
                             for dataframe in sankey_source]
        st_graphs.SelectGraph.sankey(sankey_dataframes)


if __name__ == '__main__':
    main()
