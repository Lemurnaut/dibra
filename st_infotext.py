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

    cumsum = 'Mehr zur Berechnung und Darstellung der kumulativen Summe bei [statologie.de](https://' \
             'statologie.de/kumulative-summe-r/).'


    sankey = 'Hinweis: Die Auswahl von Radzählstationen hat keinen Einfluss auf die Darstellung.'

