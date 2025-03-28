from functools import reduce
import pandas


def download_data(end_date):
    station_id = ['100044202',
                  '100000575',
                  '100002926',
                  '100002927',
                  '100002930',
                  '100002931',
                  '100002932',
                  '100002933',
                  '100002934',
                  '100002935',
                  '100047799',
                  '100047805',
                  ]

    data_startdate = '2012-01-01'
    data_enddate = end_date

    source = f'https://vmz.bremen.de/radzaehler-api/?action=Values&apiFormat=csv&resolution=hourly&startDate=' \
             f'{data_startdate}&endDate={data_enddate}'

    IDs = []
    for x in station_id:
        IDs.append('&stationId%5B%5D=' + x)

    IDs = ''.join(IDs)

    URL = source + IDs

    dataframe = pandas.read_csv(URL, header=0, sep=';')

    dataframe = dataframe.rename(columns={dataframe.columns[0]: "Datetime"})

    dataframe['Datetime'] = pandas.DatetimeIndex(dataframe.Datetime)
    # fix to avoid streamlit timezone/ambiguous errors 
    # its not a fix anymore
    # dataframe['Datetime'] = dataframe['Datetime'].dt.tz_localize('UTC')

    dataframe.set_index(dataframe.Datetime, inplace=True)
    dataframe = dataframe.drop(columns={dataframe.columns[0]})
    dataframe.set_index(dataframe.index.floor('H'), inplace=True)
    dataframe = dataframe.sort_index()

    return dataframe


def dataframe_to_list(dataframe):
    """
    takes pd.Dataframe creates list of dataframes from columns
    :param dataframe: pd.Dataframe
    :return: list
    """
    column_names = dataframe.columns.tolist()
    dataframe_list = []

    for i in column_names:
        dataframe_list.append(pandas.DataFrame(dataframe[i]))

    dataframe_proceed = []
    for dataframe in dataframe_list:
        dataframe = dataframe.truncate(before=(dataframe.gt(0).idxmax()[0]), copy=True)
        dataframe_proceed.append(dataframe)

    return dataframe_proceed


def sumDataframe(dataframe_list):
    """
    takes list of pandas dataframe
    reduce a list of pandas dataframes to one frame
    sum the rows
    returns pandas dataframe
    """
    dataframe = reduce(lambda a, b: a.add(b, fill_value=0), dataframe_list)
    dataframe = pandas.DataFrame(dataframe.sum(axis=1))
    return dataframe


def combine_stations_sides(dataframe_list):
    wkb = reduce(lambda a, b: a.add(b, fill_value=0), [dataframe_list[0], dataframe_list[1]])
    wkb = pandas.DataFrame(wkb.sum(axis=1))
    wkb.set_axis(['Wilhelm-Kaisen-Brücke'], axis=1, inplace=True)
    wkb = pandas.merge(pandas.merge(wkb, dataframe_list[0], left_index=True, right_index=True, how='outer'),
                       dataframe_list[1], left_index=True, right_index=True, how='outer')

    lngm = reduce(lambda a, b: a.add(b, fill_value=0), [dataframe_list[2], dataframe_list[3]])
    lngm = pandas.DataFrame(lngm.sum(axis=1))
    lngm.set_axis(['Langemarckstraße'], axis=1, inplace=True)
    lngm = pandas.merge(pandas.merge(lngm, dataframe_list[2], left_index=True, right_index=True, how='outer'),
                        dataframe_list[3], left_index=True, right_index=True, how='outer')

    grfm = reduce(lambda a, b: a.add(b, fill_value=0), [dataframe_list[5], dataframe_list[6]])
    grfm = pandas.DataFrame(grfm.sum(axis=1))
    grfm.set_axis(['Graf-Moltke-Straße'], axis=1, inplace=True)
    grfm = pandas.merge(pandas.merge(grfm, dataframe_list[5], left_index=True, right_index=True, how='outer'),
                        dataframe_list[6], left_index=True, right_index=True, how='outer')

    wms = reduce(lambda a, b: a.add(b, fill_value=0), [dataframe_list[8], dataframe_list[9]])
    wms = pandas.DataFrame(wms.sum(axis=1))
    wms.set_axis(['Wachmannstraße'], axis=1, inplace=True)
    wms = pandas.merge(pandas.merge(wms, dataframe_list[8], left_index=True, right_index=True, how='outer'),
                       dataframe_list[9], left_index=True, right_index=True, how='outer')

    dataframe_list_simple = [wkb,
                             lngm,
                             dataframe_list[4],
                             grfm,
                             dataframe_list[7],
                             wms,
                             dataframe_list[10],
                             dataframe_list[11]]
    return dataframe_list_simple


# https://wetterdienst.readthedocs.io/en/latest/usage/python-api/
# https://wetterdienst.readthedocs.io/en/latest/data/parameters/

from wetterdienst.provider.dwd.observation import DwdObservationRequest
from wetterdienst import Settings

def get_weather(weather_start_date, weather_end_date):

    # if no settings are provided, default settings are used which are
    # Settings(ts_shape="long", ts_humanize=True, ts_si_units=True)
    request = DwdObservationRequest(
        parameters=[("hourly", "temperature_air", "temperature_air_mean_2m"),
                    ("hourly", "wind", "wind_speed"),
                    ("hourly", "precipitation", "precipitation_height"), 
                     ],
        start_date = weather_start_date, 
        end_date = weather_end_date,
    )
    stations = request.filter_by_station_id(station_id=("00691"))

    # Query data all together
    df = stations.values.all().df.drop_nulls()
    df = df.to_pandas()
    df['parameter'] = df['parameter'].replace({"temperature_air_mean_2m" : 'Temperatur', "wind_speed" : 'Windgeschwindigkeit', "precipitation_height": "Niederschlag"})

    df.set_index(df.date, inplace=True)
    df.index = df.index.tz_localize(None)
    
    return df

def combine_weather_bikedata(bike_df, weather_df):
    weather_parameter_list = weather_df['parameter'].unique().tolist()

    df_final = None

    for i in weather_parameter_list:
        df_parameter = weather_df[weather_df['parameter'] == i]
        df_parameter = df_parameter.set_index('date')
        df_parameter.index = df_parameter.index.tz_localize(None)
        if df_final is None:
            df_final = bike_df.join(df_parameter['value'])
            df_final = df_final.rename(columns={'value' : i})
        else:
            df_final = df_final.join(df_parameter['value'])
            df_final = df_final.rename(columns={'value' : i})
    return df_final
