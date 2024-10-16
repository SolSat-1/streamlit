import datetime
import ee
import streamlit as st
import geemap.foliumap as geemap
from map_solar_radiation import evi, legend_dict, act_legend, style, params, c

st.set_page_config(layout="wide")

st.sidebar.title('เกร็ดความรู้เกี่ยวกับดาวเทียม ERA5 !! 🌍')
st.sidebar.info(
    """
    - เป็นชุดข้อมูลการวิเคราะห์ย้อนหลัง (Reanalysis) เกี่ยวกับภูมิอากาศที่พัฒนาโดย European Centre for Medium-Range Weather Forecasts (ECMWF) โดยเป็นหนึ่งในชุดข้อมูลสากลที่ใช้กันอย่างแพร่หลายในการวิเคราะห์และคาดการณ์ภูมิอากาศ ERA5 ครอบคลุมตั้งแต่ปี 1950 ถึงปัจจุบัน โดยเป็นข้อมูลรายชั่วโมงของพารามิเตอร์ที่หลากหลาย เช่น อุณหภูมิ ความชื้น ความดัน ลม และข้อมูลด้านรังสีพลังงานอื่นๆ
    - ใน Google Earth Engine (GEE) ERA5 จัดเก็บข้อมูลที่สามารถใช้งานได้สะดวก โดยเฉพาะอย่างยิ่งเมื่อทำการวิเคราะห์การเปลี่ยนแปลงของภูมิอากาศในระดับพื้นที่ที่สนใจ
    """
)


st.sidebar.title("Contact")
st.sidebar.info(
    """
    งานวิจัยอ้างอิง:
    - https://ieeexplore.ieee.org/abstract/document/8725564
    - https://journals.ametsoc.org/view/journals/clim/34/10/JCLI-D-20-0300.1.xml

    """
)

st.title("PEA BIZ-Tech Hackathon 2024 🌍🌐🫨")
st.markdown(''' แผนที่ฉบับนี้เป็นชุดข้อมูลการวิเคราะห์ย้อนหลัง (Reanalysis) ซึ่งหาค่า 5 ชนิดได้แค้
            1. รังสีพลังงาน
            2. ปริมาณน้ำฝน
            3. ความเร็วลม
            4. ความดันที่ระดับน้ำทะเล
            5. อุณหภูมิอากาศ
            ของจังหวัด กรุงเทพมหานครฯ โดยค่าที่ได้จะเป็นค่าเฉลี่ยของรายเดือน''')

col1, col2 = st.columns([4, 1])

markdown = """"""
# ---------------------------------------------------------------------------------------------------------------------------
#  TODO something
Map = geemap.Map(center=[13.5, 100.5], zoom=12)
# Map.centerObject(c, 6)
Map.setOptions("ROADMAP")

Map.add_legend(title="Solar Radiation",
            legend_dict=legend_dict, position='bottomleft', draggable=False)


Map.add_legend(title="temperature per day",
            legend_dict=act_legend, position='bottomright', draggable=False, style=style)

regions = '../geojson/PEA_Hackathon.geojson'
Map.add_geojson(regions, layer_name='ASIA Regions')

left_layer = geemap.ee_tile_layer(evi.clip(c), params, 'EVI')
right_layer = 'Maps'
Map.split_map(left_layer, right_layer)


# tab1, tab2, tab3 = st.tabs(['data', 'map', 'chart'])

# ----------------------------------------------------------------------------------------------------------------------

with col2:

    longitude = st.number_input("Longitude", -180.0, 180.0, 100.5)
    latitude = st.number_input("Latitude", -90.0, 90.0, 13.5)
    zoom = st.number_input("Zoom", 0, 20, 11)

    Map.setCenter(longitude, latitude, zoom)

    start = st.date_input("Start Date for Dynamic World", datetime.date(2020, 1, 1))
    end = st.date_input("End Date for Dynamic World", datetime.date(2021, 1, 1))

    start_date = start.strftime("%Y-%m-%d")
    end_date = end.strftime("%Y-%m-%d")


    # layers = {
    #     "Dynamic World": geemap.ee_tile_layer(dw, {}, "Dynamic World Land Cover"),
    #     "ESA Land Cover": geemap.ee_tile_layer(esa, esa_vis, "ESA Land Cover"),
    #     "ESRI Land Cover": geemap.ee_tile_layer(esri, esri_vis, "ESRI Land Cover"),
    # }

    layers = {
        "รังสีพลังงาน": 1,
        "ปริมาณน้ำฝน": 2,
        "ความเร็วลม": 3,
    }

    options = list(layers.keys())
    # left = st.selectbox("Select a left layer", options, index=1)
    # right = st.selectbox("Select a right layer", options, index=0)

    # left_layer = layers[left]
    # right_layer = layers[right]

    # Map.split_map(left_layer, right_layer)

    # legend = st.selectbox("พารามิเตอร์ที่ต้องการแสดง", options, index=options.index(right))
    legend = st.selectbox("พารามิเตอร์ที่ต้องการแสดง", options)
    if legend == "Dynamic World":
        Map.add_legend(
            title="Dynamic World Land Cover",
            builtin_legend="Dynamic_World",
        )
    elif legend == "ESA Land Cover":
        Map.add_legend(title="ESA Land Cover", builtin_legend="ESA_WorldCover")
    elif legend == "ESRI Land Cover":
        Map.add_legend(title="ESRI Land Cover", builtin_legend="ESRI_LandCover")

    with st.expander("Data sources"):
        st.markdown(markdown)


with col1:
    Map.to_streamlit(height=750)
