class method_info(object):
    def __init__(self):
        self.stl = stl
        self.wetter = wetter
        self.cumsum = cumsum
        self.sankey = sankey

    stl = 'Das Radverkehrsaufkommen ist saisonal unterschiedlich ausgeprägt. ' \
          'Es schwankt im tages-, wochen- und Jahresverlauf. Mit der verwendeten Methode ist es möglich den Trend und' \
          ' die saisonalen Unterschiede einzeln anzuzeigen. Mehr dazu [hier]' \
          '(https://www.statsmodels.org/devel/examples/notebooks/generated/stl_decomposition.html). Eine multiple ' \
          'Saison-Trend-Zerlegung (MSTL) steht in der verwendeten Version des Statistikmoduls noch nicht zu Verfügung.' \
          'Diagrammoptionen:'

    wetter = 'Den stündlichen Messwerten der Radverkehrsdaten werden die stündlichen ' \
             'Temperaturen und die stündliche Niederschlagsmenge zu geordnet. Das Radverkehrsaufkommen und der ' \
             'Niederschlag werden als tägliche Summe, die Temperatur ' \
             'als Tagesdurchschnitt im Diagramm angezeigt. Hinweis: Bei einer großen Menge an Datenpunkten, zeigt das ' \
             'Diagramm nicht das volle Datum an.'

    cumsum = 'Sofern mehr als eine Station ausgewählt wird, zeigt das Didagramm eine zusätliche Kurve mit der ' \
             'Gesamtsumme.Mehr zur Berechnung und Darstellung der kumulativen Summe bei [statologie.de](https://' \
             'statologie.de/kumulative-summe-r/).'


    sankey = 'Die *Quellen* zeigen das absolute Radverkehrsaufkommen an. Die *Links* zeigen das prozentuale Radverkehrsaufkommen an.'

class common(object):
    def __init__(self):
        self.data_info = data_info
        self.table_stations = table_stations

    data_info = 'Die Rohdaten der Verkehrsmangagementzentrale werden für die Weiterverarbeitung in dieser App nur' \
                ' minimal und wenn notwendig vorbearbeitet:' \
                'Die Datumsangaben der Zeitreihe werden als Datum/Zeit Index formatiert.' \
                'Messerwerte deren Zeitangabe nicht dem Üblichen entspricht werden auf die volle Stunde auf  bzw. ab' \
                'gerundet.' \
                'Der erste Zeitpunkt mit einem Messwert über Null wird als Beginn der Zeitreihe gesetzt. Siehe *Stationstabelle / Beginn der Messungen*.'

    table_stations = {'Stationsname': ['Wilhelm-Kaisen-Brücke (West)',
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
                       'Erster Messwert > 0 am': ['2012-01-01 00:00:00',
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

