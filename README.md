# Italy-Covid19-Dashboard

Dashboard to visualise the data made available by the Italian government on the Covid-19 outbreak in real time.

Data is taken from: [https://github.com/pcm-dpc/COVID-19](https://github.com/pcm-dpc/COVID-19)
The data are updated every day around 6pm by the Italian Government. The dashboard checks for new data and updates itself automatically every 24 hours.

Geojson file for Italy with regions taken from: [https://github.com/Dataninja/geo-shapes/tree/master/italy] (https://github.com/Dataninja/geo-shapes/tree/master/italy)

Data on the resident population in Italian Regions from: [http://dati.istat.it/Index.aspx?DataSetCode=DCIS_POPRES1](http://dati.istat.it/Index.aspx?DataSetCode=DCIS_POPRES1)

The dashboard worked fine when I have tested it and provides a good deal of interacivity when exploring the data. In fairness, I find it more useful than the official one from the Italian government [http://opendatadpc.maps.arcgis.com/apps/opsdashboard/index.html#/b0c68bce2cce478eaac82fe38d4138b1](http://opendatadpc.maps.arcgis.com/apps/opsdashboard/index.html#/b0c68bce2cce478eaac82fe38d4138b1). 

However I am a scientist and and engineer and I mostly use Pyhon (... and coding in general) to do calculations and some data viz! Hence, *my knowledge of CSS if very close to non-existent - and you can definitely tell that from my code!*

There is room for improvement in terms of the appearance of the dashboard (to put it mildly...) - any improvements/suggestions with respect fo this or any other aspect are more than welcome. 

I am using [https://www.openstreetmap.org/](Open Street Map) for the geo plots. If you have [https://www.mapbox.com/](Mapbox) token you can use it to replace Open Street Map by:
1. Insert your Mapbox token in the commented line starting `token = 'instert_mapbox_token_here'` and uncomment the line
2. Comment the line `mapbox_style="open-street-map"` in the two functions that are generating the Map plots
3. Uncomment the line `accesstoken=token` in the two functions that are generating the Map plots
