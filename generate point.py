# import processing
#processing.run("native:pointstopath", {'INPUT':'D:/_CITRA PDUPT/koordinat surabaya (1).kml|layername=koordinat surabaya|geometrytype=Point25D','CLOSE_PATH':True,'ORDER_EXPRESSION':'','NATURAL_SORT':False,'GROUP_EXPRESSION':'','OUTPUT':'TEMPORARY_OUTPUT'})
import os
from qgis.core import (
    QgsVectorLayer
)

files = [f for f in os.listdir('.') ]
for f in files:
    print(f)

rumusGDAL = {
    "ndvi" : ' ( C - B )  /  ( C  + B) ',
    "ndbi" : ' ( D - C )  /  ( D  + C) ',
    "ndisi" : '(F - 1/3*(A+C+E)) / (F + 1/3*(A+C+E))',
    "albedo" : '(0.356  *  A+ 0.13 * B + 0.373 * C + 0.085 * D + 0.072 * E - 0.0018)'
}

rumus = {
    "ndvi" : ' ( B5 - B4)  /  ( B5  + B4) ',
    "ndbi" : ' ( B6- B5 )  /  ( B6 + B5) ',
    "ndisi" : '(B10 - 1/3(B2+B5+ B7 )) / (B10 + 1/3(B2+B5+ B7 ))',
    "albedo" : '(0.356  *  B2+ 0.13 * B4+ 0.373 * B5 + 0.085 * B6+ 0.072 * B7 - 0.0018)'
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

entries = []
folder = os.listdir("citra")[0]
for file in os.listdir("citra"+"\\"+folder):
    if file.startswith(folder+"_SR_B") or file.startswith(folder+"_ST_B"):
        print(file)
        lyr = QgsRasterLayer("citra"+"\\"+folder+"\\"+file)
        ras = QgsRasterCalculatorEntry()
        ras.ref = file.split("_")[-1][:-4] 
        ras.raster = QgsRasterLayer("citra"+"\\"+folder+"\\"+file)
        ras.bandNumber = 1
        entries.append(ras)
        iface.addRasterLayer("citra"+"\\"+folder+"\\"+file, file.split("_")[-1][:-4])


for type in types[0:1]:
    calc = QgsRasterCalculator(rumus[type], type+'.tif', 'GTiff', lyr.extent(), lyr.width(), lyr.height(),entries )
    calc.processCalculation()
#     processing.run("gdal:rastercalculator", {
#         'INPUT_A':'citra/LC08_L2SP_118065_20130728_20200912_02_T1/LC08_L2SP_118065_20130728_20200912_02_T1_SR_B2.TIF','BAND_A':1,
#         'INPUT_B':'citra/LC08_L2SP_118065_20140629_20200911_02_T1/LC08_L2SP_118065_20140629_20200911_02_T1_SR_B4.TIF','BAND_B':1,
#         'INPUT_C':'citra/LC08_L2SP_118065_20130728_20200912_02_T1/LC08_L2SP_118065_20130728_20200912_02_T1_SR_B5.TIF','BAND_C':1,
#         'INPUT_D':'citra/LC08_L2SP_118065_20130728_20200912_02_T1/LC08_L2SP_118065_20130728_20200912_02_T1_SR_B6.TIF','BAND_D':1,
#         'INPUT_E':'citra/LC08_L2SP_118065_20140629_20200911_02_T1/LC08_L2SP_118065_20140629_20200911_02_T1_SR_B7.TIF','BAND_E':1,
#         'INPUT_F':'citra/LC08_L2SP_118065_20130728_20200912_02_T1/LC08_L2SP_118065_20130728_20200912_02_T1_ST_B10.TIF','BAND_F':1,
#         'FORMULA':rumusGDAL[type],'NO_DATA':None,'PROJWIN':None,'RTYPE':5,'OPTIONS':'','EXTRA':'',
#    'OUTPUT': type+'.tif'})
    iface.addRasterLayer(type+'.tif', type)
    print(type)