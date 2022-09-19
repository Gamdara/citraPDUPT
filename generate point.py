# import processing
#processing.run("native:pointstopath", {'INPUT':'D:/_CITRA PDUPT/koordinat surabaya (1).kml|layername=koordinat surabaya|geometrytype=Point25D','CLOSE_PATH':True,'ORDER_EXPRESSION':'','NATURAL_SORT':False,'GROUP_EXPRESSION':'','OUTPUT':'TEMPORARY_OUTPUT'})
import os
from qgis.core import (
    QgsVectorLayer
)

#files = [f for f in os.listdir('.') ]
#for f in files:
#    print(f)
#
rumusGDAL = {
    "ndvi" : ' ( C - B )  /  ( C  + B) ',
    "ndbi" : ' ( D - C )  /  ( D  + C) ',
    "ndisi" : '(F - 1/3*(A+C+E)) / (F + 1/3*(A+C+E))',
    "albedo" : '(0.356  *  A+ 0.13 * B + 0.373 * C + 0.085 * D + 0.072 * E - 0.0018)'
}

rumus = {
    "ndvi" : ' ( B5@1 - B4@1)  /  ( B5@1  + B4@1) ',
    "ndbi" : ' ( B6@1- B5@1 )  /  ( B6@1 + B5@1) ',
    "ndisi" : '(B10@1 - 1/3*(B2@1+B5@1+ B7@1 )) / (B10@1 + 1/3*(B2@1+B5@1+ B7@1 ))',
    "albedo" : '(0.356  *  B2@1+ 0.13 * B4@1+ 0.373 * B5@1 + 0.085 * B6@1+ 0.072 * B7@1 - 0.0018)'
}

types = ['ndvi','ndbi','ndisi','albedo','lst']

dates = [
    '7/28/2013',
    '6/29/2014',
    '6/16/2015',
    '7/4/2016',
    '7/23/2017',
    '7/26/2018',
    '7/13/2019',
    '7/31/2020',
    '5/15/2021'
]

QgsProject.instance().clear()
entries = []
folder = os.listdir("citra")[0]
for file in os.listdir("citra"+"\\"+folder):
    if file.startswith(folder+"_SR_B") or (file.startswith(folder+"_ST_B") and file.endswith("TIF")):
        print(file)
        lyr = QgsRasterLayer("citra"+"\\"+folder+"\\"+file)
        ras = QgsRasterCalculatorEntry()
        ras.ref = file.split("_")[-1][:-4] 
        ras.raster = QgsRasterLayer("citra"+"\\"+folder+"\\"+file)
        ras.bandNumber = 1
        entries.append(ras)
        iface.addRasterLayer("citra"+"\\"+folder+"\\"+file, file.split("_")[-1][:-4])


for type in types[0:4]:
    processing.run("qgis:rastercalculator", {
        'EXPRESSION':' ("B5@1" - "B4@1"  )  /  ( "B5@1" + "B4@1" ) ',
        'LAYERS':[
        "citra"+"\\"+folder+"\\"+folder+"_SR_B2.TIF",
        "citra"+"\\"+folder+"\\"+folder+"_SR_B4.TIF",
        "citra"+"\\"+folder+"\\"+folder+"_SR_B5.TIF",
        "citra"+"\\"+folder+"\\"+folder+"_SR_B6.TIF",
        "citra"+"\\"+folder+"\\"+folder+"_SR_B7.TIF",
        "citra"+"\\"+folder+"\\"+folder+"_ST_B10.TIF",
        ],
        'CELLSIZE':0,'EXTENT':'682031.481400000,704331.481400000,-812752.242500000,-793152.242500000 [EPSG:32649]','CRS':None,'OUTPUT':type+'.tif'})
    iface.addRasterLayer(type+'.tif', type)
    print(rumusGDAL[type])