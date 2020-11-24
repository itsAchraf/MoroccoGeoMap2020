import folium
import os
import branca
import io
import pandas as pd
import numpy as np
from folium.plugins import MarkerCluster
from folium.plugins import FastMarkerCluster
from folium.features import DivIcon

class Map:

    def __init__(self,f_GeoJson,fGeo_csv,fData_csv):
        self.f_GeoJson = io.open(f_GeoJson,'r',encoding='utf-8-sig').read()
        #fGeo_csv = open(r'data/geoMap.csv', encoding="utf8")
        #fData_csv= open(r'data/covid_morocco_data.csv',encoding="utf8")
        self.df_Geo=pd.read_csv(fGeo_csv)
        self.df_Data=pd.read_csv(fData_csv)

    def merge_data_and_Location(self,columns=1):
        dataframe=self.df_Data.iloc[-1:,columns:].T
        dataframe.columns=['value']
        dataframe.index.name='Region'
        return dataframe.merge(self.df_Geo,left_on='Region',right_on='Region')

    def data_to_geoZone(self,dataframe):
        new_df = pd.DataFrame()
        for i in range(len(dataframe)):
            row = dataframe.loc[ i][0:]
            rep = int(np.int64(row.value))
            df_T=pd.DataFrame(data=row).T
            df=df_T.sample(n=rep,replace=1)
            #new_df=pd.concat([df_T]*rep,ignore_index=True)
            new_df = new_df.append(df,ignore_index=True)
        return new_df

    def createMap(self,map_style='CartoDB Positron',s_zoom=4.9,map_dim=['90','70']):
        self.map = folium.Map(location=[self.df_Geo.lat.mean(),self.df_Geo.long.mean()], zoom_start=s_zoom,max_zoom=(s_zoom+1),min_zoom=(s_zoom-1),
                        tiles=map_style)
                        #height=map_dim[0],width=map_dim[1]
        bins = [0,500,1000,1500,2000,2500,3000,3500,4000]
        #bins = [0,500,2000,4000,6000,8000,10000]
        
        folium.Choropleth(
            geo_data = self.f_GeoJson,
            name = 'Results',
            data = self.merge_data_and_Location(),
            columns = ['Region' , 'value'],
            key_on = 'feature.properties.name',
            fill_color='Reds',
            fill_opacity=0.9,
            line_opacity=0.9,
            bins=bins,
            legend_name='Unemployment Rate (%)'
        ).add_to(self.map)
    def markerZone(self):     
        callback = ('function (row) {' 
                    'var circle = L.circle(new L.LatLng(row[0], row[1]), {color: "bleu",  radius: 1});'
                    'return circle};')
        self.map.add_child(FastMarkerCluster(self.data_to_geoZone(self.merge_data_and_Location())[['lat', 'long']].values.tolist(), callback=callback, popup="Laurelhurst Park"))
#        self.map.save('./index.html')

    def save(self,path='THE_MAP.html'):
        self.map.save(path)
    
    def jsMarker(self):
        folium.map.Marker(
            [33.714667, -2.318488],
            icon=DivIcon(
                icon_size=(150,36),
                icon_anchor=(0,0),
                html='<span align="center" style="height: 50px;width: 50px;background-color: #bbb;border-radius: 50%;display: inline-block;" class="dot">100</span>',
            )
        ).add_to(self.map)


'''
        
    '''    