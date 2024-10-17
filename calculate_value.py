import ee
from datetime import datetime
import geemap.foliumap as geemap
from datetime import datetime
from dateutil.relativedelta import relativedelta
import math
import json

geemap.ee_initialize(
    token_name="4/1AQlEd8yH0xfMAYqZzI7lGJhAXgHFuCO2p-5olv4eVBaZcllee8gp_YxzcVM")
ee.Initialize()


# # สร้างพื้นที่ประเทศไทย (region of interest - ROI)

# สร้าง Polygon ของพื้นที่กรุงเทพมหานคร
# ต้องการเป็น coordinate เป็น key
def calculate(polygon: list[int]):
    # polygon = [[[100.46697782333419, 13.495665330651736], [100.4007799199477, 13.490637567256401], [100.41157677574756, 13.512069607026717], [100.38951093987794, 13.611805120709732], [100.34594770712096, 13.656918647077873], [100.32698245577569, 13.751073105739238], [100.33566409712034, 13.79871877675015], [100.48836795531685, 13.798098660025119], [100.5217509299614, 13.848198961313017], [100.5515165552448, 13.94785696152951], [100.6785889023559, 13.918039659402723], [100.90482832236916, 13.94979482696965], [100.89692182827969, 13.846803697332746], [100.92358686724009, 13.813420721788873], [100.8492761581681, 13.709163520280242], [100.85537397712733, 13.691981106542812], [100.71321211134983, 13.711514796870347], [100.68587527882102, 13.660019233400874], [100.66401614762708, 13.652965400033167], [100.59823205026885, 13.658391425423929], [100.58526126509526, 13.666763007506802], [100.59590661030177, 13.69714874951518], [100.56138675319608, 13.703582465258535], [100.51937381405025, 13.662783922040376], [100.49922000519905, 13.665445257892316], [100.49379397980829, 13.59984202678811], [100.46304650259395, 13.583512275571024],[100.46697782333419,13.495665330651736]]]
    bangkok_roi = ee.Geometry.Polygon(polygon)

    # Define the BANDS dictionary
    BANDS = {
        'solar_radiation': {'topic': 'surface_net_solar_radiation_sum', 'unit': 'W/m^2', 'location': 'Bangkok'},
        'precipitation': {'topic': 'surface_latent_heat_flux_sum', 'unit': 'mm', 'location': 'Bangkok'},
        'wind': {'topic': 'u_component_of_wind_10m', 'unit': 'm/s', 'location': 'Bangkok'},
        'pressure': {'topic': 'surface_pressure', 'unit': 'pa', 'location': 'Bangkok'},
        'temperature': {'topic': 'temperature_2m', 'unit': 'Celsius', 'location': 'Bangkok'}
    }

    # Define the date range
    start_date = datetime.now()+relativedelta(days=-10)
    end_date = datetime.now()+relativedelta(days=-9)

    # Function to calculate the mean for a given band
    def calculate_mean_for_band(band_name):
        dataset = ee.ImageCollection("ECMWF/ERA5_LAND/DAILY_AGGR") \
                    .select(band_name) \
                    .filterBounds(bangkok_roi) \
                    .filterDate(start_date, end_date)
        
        # Reduce the ImageCollection to a single image (mean across all images)
        mean_image = dataset.mean()
        
        # Calculate the mean for the region of interest
        mean_value = mean_image.reduceRegion(
            reducer=ee.Reducer.mean(),
            geometry=bangkok_roi,
            scale=10000,  # Scale in meters
            maxPixels=1e9
        )
        
        return mean_value.get(band_name).getInfo()

    real_output = {'response': []}
    # Calculate mean for each band and print the results
    for band_key, band_name in BANDS.items():
        output = {}
        mean_value = calculate_mean_for_band(band_name['topic'])
        print(band_name['topic'])
        print(f'Mean value for {band_key} ({band_name["topic"]}): {int(mean_value)}')
        output['band'] = band_name["topic"]
        output['value'] = math.ceil(mean_value)
        output['unit'] = band_name["unit"]
        output['loaction'] = band_name["location"]
        real_output['response'].append(output)
    
    print(json.dumps(real_output, indent=4))
    
    return real_output['response']

if __name__ == '__main__':
   
    # example
    array = [[[100.46697782333419, 13.495665330651736], [100.4007799199477, 13.490637567256401], [100.41157677574756, 13.512069607026717], [100.38951093987794, 13.611805120709732], [100.34594770712096, 13.656918647077873], [100.32698245577569, 13.751073105739238], [100.33566409712034, 13.79871877675015], [100.48836795531685, 13.798098660025119], [100.5217509299614, 13.848198961313017], [100.5515165552448, 13.94785696152951], [100.6785889023559, 13.918039659402723], [100.90482832236916, 13.94979482696965], [100.89692182827969, 13.846803697332746], [100.92358686724009, 13.813420721788873], [100.8492761581681, 13.709163520280242], [100.85537397712733, 13.691981106542812], [100.71321211134983, 13.711514796870347], [100.68587527882102, 13.660019233400874], [100.66401614762708, 13.652965400033167], [100.59823205026885, 13.658391425423929], [100.58526126509526, 13.666763007506802], [100.59590661030177, 13.69714874951518], [100.56138675319608, 13.703582465258535], [100.51937381405025, 13.662783922040376], [100.49922000519905, 13.665445257892316], [100.49379397980829, 13.59984202678811], [100.46304650259395, 13.583512275571024],[100.46697782333419,13.495665330651736]]]
     # array = [[['your', 'long']]]
    response = calculate(array)

    if response:
        with open('./streamlit_version_1/output.json', 'w') as json_file:
            json.dump(response, json_file, indent=4)






