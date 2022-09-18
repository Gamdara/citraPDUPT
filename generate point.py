# import processing
#processing.run("native:pointstopath", {'INPUT':'D:/_CITRA PDUPT/koordinat surabaya (1).kml|layername=koordinat surabaya|geometrytype=Point25D','CLOSE_PATH':True,'ORDER_EXPRESSION':'','NATURAL_SORT':False,'GROUP_EXPRESSION':'','OUTPUT':'TEMPORARY_OUTPUT'})
import os
from qgis.core import (
    QgsVectorLayer
)
rumus = {
    "ndvi" : ""
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

folder = os.listdir("citra")[0]
for file in os.listdir("citra"+"\\"+folder):
    if file.startswith(folder+"_SR_B") or file.startswith(folder+"_ST_B"):
        print(file)
        rlayer = QgsRasterLayer("citra"+"\\"+folder+"\\"+file, file.split("_")[-1][:-4])
        if not rlayer.isValid():
            print("Layer failed to load!")
            continue
        QgsProject.instance().addMapLayer(rlayer, False)