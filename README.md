# Italy-Covid19-Dashboard

Dashboard to visualise the data made available by the Italian Italian Civil Protection Department on the Covid-19 outbreak in real time.

![Dashboard screenshot](screenshot.PNG)

The dashboard worked fine when I have tested it and provides a good deal of interacivity when exploring the data. In fairness, I find it more useful than [the official one from the Italian Civil Protection Department](http://opendatadpc.maps.arcgis.com/apps/opsdashboard/index.html#/b0c68bce2cce478eaac82fe38d4138b1). 

However, I am a scientist and and engineer and I mostly use Python (... and coding in general!) to do calculations and some data viz! Hence, *my knowledge of CSS is almost non-existent - and you can definitely tell that from my code!* . So there is definitely room for improvement in terms of the appearance of the dashboard (to put it mildly!) and **any improvements/suggestions with respect fo this or any other aspect are more than welcome**. 

I am using [Open Street Map](https://www.openstreetmap.org) for the plots requiring a map. If you have a [Mapbox](https://www.mapbox.com/) token you can use it to replace Open Street Map by:
1. Insert your Mapbox token in the commented line `token = 'instert_mapbox_token_here'` and uncomment the line
2. Comment the line `mapbox_style="open-street-map"` in the two functions that are generating the map plots
3. Uncomment the line `accesstoken=token` in the two functions that are generating the map plots

## Resources
* Data is taken from (the official repository of the Italian Civil Protection Department)[https://github.com/pcm-dpc/COVID-19](https://github.com/pcm-dpc/COVID-19)
The data is updated every day around 5pm by the Italian Civil Protection Department. The dashboard checks for new data and updates itself automatically every 24 hours.

* Geojson file for Italian regions taken from: [https://github.com/Dataninja/geo-shapes/tree/master/italy] (https://github.com/Dataninja/geo-shapes/tree/master/italy)

* Data on the resident population in Italian Regions from: [http://dati.istat.it/Index.aspx?DataSetCode=DCIS_POPRES1](http://dati.istat.it/Index.aspx?DataSetCode=DCIS_POPRES1)


