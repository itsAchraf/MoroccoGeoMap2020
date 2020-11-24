import folium
import os
import branca
import io
import pandas as pd
import numpy as np
from folium.plugins import MarkerCluster
from folium.plugins import FastMarkerCluster
from folium.features import DivIcon

f_GeoJson = io.open("data/Maghreb/Maghreb_geo.json",'r',encoding='utf-8-sig').read()
#fGeo_csv = open(r'data/geoMap.csv', encoding="utf8")
#fData_csv= open(r'data/covid_morocco_data.csv',encoding="utf8")
fGeo_csv=pd.read_csv(r'data/Maghreb/geoMap.csv')
fData_csv=pd.read_csv(r'data/Maghreb/Maghreb_covid19_confirmed.csv')

def merge_data_and_Location(df_Geo,df_data):
    dataframe=df_data.iloc[-1:,1:].T
    dataframe.columns=['value']
    dataframe.index.name='Region'
    return dataframe.merge(df_Geo,left_on='Region',right_on='Region')

data = merge_data_and_Location(fGeo_csv,fData_csv)

def data_to_geoZone(dataframe):
    new_df = pd.DataFrame()
    for i in range(len(data)):
        row = dataframe.loc[ i][0:]
        rep = int(np.int64(row.value))
        df_T=pd.DataFrame(data=row).T
        df=df_T.sample(n=rep,replace=1)
        #new_df=pd.concat([df_T]*rep,ignore_index=True)
        new_df = new_df.append(df,ignore_index=True)
    return new_df

df_GeoZone = data_to_geoZone(data)
def createMap(data, f_GeoJson, df_GeoZone):
    map = folium.Map(location=[30,-10], zoom_start=4.9,
                    tiles='CartoDB Positron', height='90',width="70"
                    ,max_lat=-10,min_lat=-10,max_lon=31,min_lon=31)
    bins = [0,500,1000,1500,2000,2500,3000,3500,4000]
    folium.Choropleth(
        geo_data = f_GeoJson,
        name = 'Results',
        data = data,
        columns = ['Region' , 'value'],
        key_on = 'feature.properties.name',
        fill_color='Reds',
        fill_opacity=0.9,
        line_opacity=0.9,
        bins=bins,
        legend_name='Unemployment Rate (%)',
        reset=True
    ).add_to(map)

    folium.map.Marker(
        [33.714667, -2.318488],
        icon=DivIcon(
            icon_size=(150,36),
            icon_anchor=(0,0),
            html='<div style="font-size: 14pt">.</div>',
            )
        ).add_to(map)

    callback = ('function (row) {' 
                    'var circle = L.circle(new L.LatLng(row[0], row[1]), {color: "bleu",  radius: 1000});'
                    'return circle};')

    map.add_child(FastMarkerCluster(df_GeoZone[['lat', 'long']].values.tolist(), callback=callback))
    map.save('./index.html')

createMap(data, f_GeoJson, df_GeoZone)










'''
import folium
from folium.features import DivIcon
import io
import pandas as pd


f_json = io.open('D:/Pyproject/data/maGeo.json','r',encoding='utf-8-sig').read()
f_csv = open('D:/Pyproject/data/geoMap.csv', encoding="utf8")
searchRes = pd.read_csv(f_csv)

map = folium.Map(location=[29.5,-10], zoom_start=4.5, tiles='CartoDB Positron',
                    height='67', width="50",
                    max_zoom=5, min_zoom=4,
                    max_lat=31, min_lat=31,
                    max_lon=-12, min_lon=-12)


folium.Choropleth(geo_data = f_json,name = "Results", 
                    data = searchRes, columns = ["Region" , "value"],
                    key_on = "feature.properties.name_2",
                    fill_color="Reds",fill_opacity=1,
                    line_opacity=0.9,
                    legend_name="Unemployment Rate (%)",reset=True).add_to(map)

folium.map.Marker(
    [33.714667, -2.318488],
    icon=DivIcon(
        icon_size=(150,36),
        icon_anchor=(0,0),
        html='<div style="font-size: 14pt">Test</div>',
        )
    ).add_to(map)
map.save('./GeoMap/index.html')
'''