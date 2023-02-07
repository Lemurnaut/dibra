from functools import reduce
import pandas

from wetterdienst.provider.dwd.observation import DwdObservationRequest, DwdObservationDataset, DwdObservationPeriod, \
    DwdObservationResolution
from wetterdienst import Settings


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
    import pandas

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
    import pandas as pd
    from functools import reduce

    dataframe = reduce(lambda a, b: a.add(b, fill_value=0), dataframe_list)
    dataframe = pd.DataFrame(dataframe.sum(axis=1))
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


def get_weather(start_date: str, end_date: str, station_id: int):
    """
    for wetterdienst==0.42.0
    """

    Settings.tidy = True
    Settings.humanize = True
    Settings.si_units = False

    import pandas

    request = DwdObservationRequest(
        parameter=[DwdObservationDataset.TEMPERATURE_AIR, DwdObservationDataset.PRECIPITATION],
        resolution=DwdObservationResolution.HOURLY,
        start_date=start_date,
        end_date=end_date,
    ).filter_by_station_id(station_id=(station_id))

    for result in request.values.query():
        niederschlag = result.df[result.df['parameter'] == 'precipitation_height']
        temperatur = result.df[result.df['parameter'] == 'temperature_air_mean_200']

    pandas.to_datetime(niederschlag['date'], format='%Y-%m-%d %H:%M:%S').copy()
    niederschlag.set_index(pandas.DatetimeIndex(niederschlag['date']), inplace=True)

    niederschlag = niederschlag.rename(columns={'value': 'Niederschlag'})
    niederschlag = niederschlag.drop(columns={'station_id', 'dataset', 'parameter', 'date', 'quality'})

    pandas.to_datetime(temperatur['date'], format='%Y-%m-%d %H:%M:%S').copy()
    temperatur.set_index(pandas.DatetimeIndex(temperatur['date']), inplace=True)

    temperatur = temperatur.rename(columns={'value': 'Temperatur'})
    temperatur = temperatur.drop(columns={'station_id', 'dataset', 'parameter', 'date', 'quality'})

    weather = pandas.merge(niederschlag, temperatur, left_index=True, right_index=True, how='outer')
    weather.index = weather.index.tz_localize(tz=None)  # delete timezone from df index

    return weather
