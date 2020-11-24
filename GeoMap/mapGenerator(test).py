from Map import Map
t=Map('data/Morocco/maGeo.json','data/Morocco/geoMap.csv','data/Morocco/covid_morocco_data.csv')
t.createMap(s_zoom=6)
t.markerZone()
t.jsMarker()
t.save('C:/Program Files/Ampps/www/Dashboard/Maps/Morocco.html')
'''

t=Map('data/Maghreb/Maghreb_geo.json','data/Maghreb/geoMap.csv','data/Maghreb/Maghreb_covid19_confirmed.csv')
t.createMap(s_zoom=3)
t.markerZone()
t.save('C:/Program Files/Ampps/www/Dashboard/Maps/Maghreb_confirmed.html')


t=Map('data/Maghreb/Maghreb_geo.json','data/Maghreb/geoMap.csv','data/Maghreb/Maghreb_covid19_recovered.csv')
t.createMap(s_zoom=4)
t.markerZone()
t.save('C:/Program Files/Ampps/www/Dashboard/Maps/Maghreb_recovered.html')


t=Map('data/Maghreb/Maghreb_geo.json','data/Maghreb/geoMap.csv','data/Maghreb/Maghreb_covid19_deaths.csv')
t.createMap(s_zoom=4)
t.markerZone()
t.save('C:/Program Files/Ampps/www/Dashboard/Maps/Maghreb_deaths.html')
'''