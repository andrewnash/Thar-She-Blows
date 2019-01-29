import sys
import pandas as pd 
from gmplot import gmplot

def heatPlots(mapLat, mapLong, minSpeed, minDepth):    
    # create blank map
    gmap = gmplot.GoogleMapPlotter(mapLat, mapLong, 10)

    ############### Heatmap #####################
    # store .xlsx in panda database
    data = pd.read_excel("aec.xlsx",sheet_name="wind-data")
    
    lats = data.columns.values[1:]
    longs = data[list(data)[0]].tolist()
    
    Wweights = []
    WbigLong = []
    WbigLat = []
    for i in range(0, len(lats) - 1):
        for j in range(1, len(longs) - 1):
            Wweights.append(data.iloc[i][j])
            for val in range(minSpeed, int(Wweights[-1])):
                WbigLat.append(lats[i])
                WbigLong.append(longs[j])
    
    # def heatmap(self, lats, lngs, threshold=10, radius=10, gradient=None, opacity=0.6, maxIntensity=1, dissipating=True):
    gmap.heatmap(WbigLat, WbigLong, 10, 14, None, 0.6, max(Wweights))   
    gmap.draw("heatmap.html")
     
    ################# Depth Map ###################
    data = pd.read_excel("aec.xlsx",sheet_name="depth-data")
    
    lats = data.columns.values[1:]
    longs = data[list(data)[0]].tolist()
    
    weights = []
    bigLong = []
    bigLat = []
    for i in range(0, len(lats) - 1):
        for j in range(1, len(longs) - 1):
            weights.append(data.iloc[i][j])
            for val in range(0 , int(weights[-1]) - minDepth):
                bigLat.append(lats[i])
                bigLong.append(longs[j])
    
    gmap.heatmap(bigLat, bigLong, 10, 14, None, 0.6, max(weights))
    gmap.draw("depthmap.html")
