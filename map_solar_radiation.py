import datetime
import ee
import geemap.foliumap as geemap
import os
from dotenv import load_dotenv

load_dotenv(verbose=True)

geemap.ee_initialize(
    token_name=os.getenv('EARTH_ENGINE_TOKEN'))
ee.Initialize()

c = ee.Geometry.Polygon([[[100.46697782333419, 13.495665330651736], [100.4007799199477, 13.490637567256401], [100.41157677574756, 13.512069607026717], [100.38951093987794, 13.611805120709732], [100.34594770712096, 13.656918647077873], [100.32698245577569, 13.751073105739238], [100.33566409712034, 13.79871877675015], [100.48836795531685, 13.798098660025119], [100.5217509299614, 13.848198961313017], [100.5515165552448, 13.94785696152951], [100.6785889023559, 13.918039659402723], [100.90482832236916, 13.94979482696965], [100.89692182827969, 13.846803697332746], [100.92358686724009, 13.813420721788873], [100.8492761581681, 13.709163520280242], [100.85537397712733, 13.691981106542812], [100.71321211134983, 13.711514796870347], [100.68587527882102, 13.660019233400874], [100.66401614762708, 13.652965400033167], [100.59823205026885, 13.658391425423929], [100.58526126509526, 13.666763007506802], [100.59590661030177, 13.69714874951518], [100.56138675319608, 13.703582465258535], [100.51937381405025, 13.662783922040376], [100.49922000519905, 13.665445257892316], [100.49379397980829, 13.59984202678811], [100.46304650259395, 13.583512275571024],[100.46697782333419,13.495665330651736]]])
S2 = ee.ImageCollection('COPERNICUS/S2').filterDate('2023-04-01', '2023-12-31').filterBounds(c)

# file = open('polygon_800.geojson', encoding="utf-8")
# ee_data = geojson_to_ee('yes_camp_MDC_2.geojson', encoding="utf-8")

# def maskcloud1(image):
#     QA60 = image.select(['QA60'])
#     return image.updateMask(QA60.lt(1))

image = S2.median().select(['B2', 'B3', 'B4', 'B8'], [
    'blue', 'green', 'red', 'nir'])

evi = image.expression(
    "2.5 * ((nir - red) / (nir + 6 * red - 7.5 * blue + 1))",
    {
        'nir': image.select('nir').divide(10000),
        'red': image.select('red').divide(10000),
        'blue': image.select('blue').divide(10000),
    })

legend_dict = {
    "percentage of W/m^2 <100%": "ff0000",
    "percentage of W/m^2 <89%": "ff500d",
    "percentage of W/m^2 <78%": "ff6e08",
    "percentage of W/m^2 <67%": "ff8b13",
    "percentage of W/m^2 <56%": "ffb613",
    "percentage of W/m^2 <45%": "ffd611",
    "percentage of W/m^2 <34%": "fff705",
    "percentage of W/m^2 <23%": "b5e22e",
    "percentage of W/m^2 <12%": "86e26f",
}
# encode_lengend_dict = legend_dict
act_legend = {
    '41< temperature <39': 'ff0000',
    '38< temperature <37': 'ff500d',
    '37< temperature <36': '#ff6e08',
    '35< temperature <33': 'ffb613',
    '32< temperature <31': 'ffd611',
    '30< temperature <29': 'fff705',
    '28< temperature <27': 'b5e22e',
    '26< temperature <25': '3ae237',
    '24< temperature <23': '86e26f',
}

pal = [
    '040274', 'd6e21f','fff705', 'ffd611', 'ffb613', 'ff8b13', 
    'ff6e08', 'ff500d','ff0000', 'de0101', 'c21301', 'a71001',
    '040281', '0502a3', '0502b8', '0502ce', '0502e6',
    '0602ff', '235cb1', '307ef3', '269db1', '30c8e2', '32d3ef', 
    '911003', '3be285', '3ff38f', '86e26f', '3ae237', 'b5e22e', ]
params = {'min': -0.1, 'max': 1, 'palette': pal}

style = {
    'border-radius': '18px',
    'padding': '18px',
    'font-size': '16px',
    'bottom': '20px',
    'right': '20px',
    'left': '20px'
}

# print(evi)
# Map = geemap.Map()
# # Map.centerObject(c, 6)
# Map.setOptions("SATELLITE")

# Map.add_legend(title="Solar Radiation",
#             legend_dict=legend_dict, position='bottomleft', draggable=False)




# Map.add_legend(title="solar rediation",
#             legend_dict=legend_dict, position='bottomleft', draggable=False)



# # Map.to_streamlit()
# Map.add_legend(title="temperature per day",
#             legend_dict=act_legend, position='bottomright', draggable=False, style=style)

# left_layer = geemap.ee_tile_layer(EVI.clip(c), params, 'EVI')
# right_layer = 'ROADMAP'
# Map.split_map(left_layer, right_layer)

# Map.to_streamlit(height=800, width=800)