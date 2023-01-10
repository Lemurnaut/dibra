import streamlit as st
import st_elements
import st_graphs
import preprocess

version = '0.0.9_alpha'

# setup streamlit layout
menu_items = {
    'About': '''
    ## RaStA 
    Bremer Radzählstationen Analysetool

    made by stefko

    www.moin-stefko.de
    '''
}
st.set_page_config(layout="wide", menu_items=menu_items)
col1, col2 = st.columns(2)


@st.cache
def download():
    dataframe = preprocess.download_data()
    return dataframe

def main():
    dataframe_source = download()
    dataframe_list =  preprocess.dataframe_to_list(dataframe_source)

    startdate, enddate = st_elements.sidebar_date()
    starttime, endtime = st_elements.sidebar_time()

    selected_dataframes = st_elements.sidebar_station_select(dataframe_list)
    selected_dataframes = [(dataframe.loc[startdate : enddate].between_time(starttime, endtime)) for dataframe in selected_dataframes]

    graph_type = st_elements.sidebar_graph_select()

    if graph_type == 'Info':
        st_graphs.SelectGraph.info()
    elif graph_type == 'Übersicht':
        st_graphs.SelectGraph.overview(selected_dataframes)
    elif graph_type == 'Kummulationen':
        st_graphs.SelectGraph.cumsum(selected_dataframes)
    elif graph_type == 'Tagesverlauf':
        st_graphs.SelectGraph.week_dist(selected_dataframes)
    elif graph_type == 'Saison-Trend-Zerlegung':
        st_graphs.SelectGraph.stl(selected_dataframes)
    elif graph_type == 'Oberflächendiagramm':
        st_graphs.SelectGraph.surface(selected_dataframes)
    elif graph_type == 'gleitender Mittelwert':
        st_graphs.SelectGraph.moving_av(selected_dataframes)






if __name__ == '__main__':
    main()

