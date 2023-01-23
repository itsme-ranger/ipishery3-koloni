import streamlit as st
from PIL import Image
from streamlit_drawable_canvas import st_canvas
# from io import StringIO

import os
import pandas as pd
import numpy as np
from sklearn.mixture import GaussianMixture
import csv

DEFAULT_WIDTH_IMG = 720
PETRI_DISH_AREA_MM = 7854
RADIUS_COLOR_MIN_PX = 8
SD_RGB_MAX = 10

def rgb_to_hex(rgb):
    return '%02x%02x%02x' % rgb

def style_specific_cell(x, i, rgb_color):
    color = f'background-color: #{rgb_to_hex(rgb_color)}'
    df1 = pd.DataFrame('', index=x.index, columns=x.columns)
    df1["colour"].iloc[i] = color
    return df1

def generate_results(img_path, is_auto_threshold, RoI):
    # pass
    n_species = st.sidebar.slider("Number of species (or distinguishable colours): ", 1, 20, 1)
    command = f"opencfu -i {img_path}"
    if is_auto_threshold:
        command = command+" -a"
    os.system(command)
    
    # read results 
    with open('results.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        # line_count = 0
        # skip header
        next(csv_reader, None)
        # next(csv_reader, None)

        color_mean = [] # np.array()
        data = []
        for row in csv_reader:

            # COLORS GENERATION
            # filtering validity
            # 1st: whether considered as valid or not
            # 2nd: whether in RoI or not
            if int(row[0]) & (int(row[3])):
                data.append(row)
                # 3rd: whether radius above= RADIUS_COLOR_MIN_PX
                # 4,5,6th: whether under RGB SD under SD_COLOR_MAX_PX
                if (int(row[7]) >= RADIUS_COLOR_MIN_PX) \
                    & (float(row[13]) <SD_RGB_MAX ) & (float(row[14])<SD_RGB_MAX) & (float(row[15])<SD_RGB_MAX):
                    color_mean.append([row[10], row[11], row[12]])
    
    color_mean = np.array(color_mean).astype(float)
    gm = GaussianMixture(n_components=n_species, random_state=0).fit(color_mean)
    colors = gm.means_

    # output = { str([R,G,B]) of vibrio : [ { "center of X", "Y", "diameter" } ] }
    output = {}
    for color in colors:
        output[str(color)] = []
    for row in data:
        color = gm.predict([row[10], row[11], row[12]])
        output[str(color)].append({
            'x' : float(row[1]),
            'y' : float(row[2]),
            'area_mm' : int(row[6])*PETRI_DISH_AREA_MM/RoI['area_px']
            'radius_px' : int(row[7])
            'colony_count' : int(row[5])
        })

    # draw results onto image in streamlit
    df = pd.DataFrame(output)
    for i, row in enumerate(colors):
        df.style.apply(lambda x: style_specific_cell(x, i, row), axis = 0)
    st.dataframe(df)

# class 

def input_params_infer(img_path, RoI_pd):
    # generate ROI image
    assert len(RoI_pd) == 1
    roi_x = RoI_pd["originX"].iloc(0)
    roi_y = RoI_pd["originY"].iloc(0)
    roi_area_px = RoI_pd["area"].iloc(0)
    RoI = {
       'x' : roi_x,
       'y' : roi_y,
       'area_px' : roi_area_px
    }
    
    is_auto_threshold = st.sidebar.checkbox("Automatic thresholding? thresholding slider will not work", True)
    # threshold_ = st.sidebar.slider("Point display radius: ", 1, 25, 3)
    stroke_width = st.sidebar.slider("Stroke width: ", 1, 25, 3)
    # if drawing_mode == 'point':
        
    #     stroke_color = st.sidebar.color_picker("Stroke color hex: ")
    #     bg_color = st.sidebar.color_picker("Background color hex: ", "#eee")
    #     bg_image = st.sidebar.file_uploader("Background image:", type=["png", "jpg"])
    # realtime_update = st.sidebar.checkbox("Update in realtime", True)
    # pass
    st.button('input params done?', on_click=lambda: generate_results(img_path, is_auto_threshold))


def ROI_creation(img_path):
    if img_path != "":
        # To read file as bytes:
        # image = uploaded_file.getvalue()
        # st.write(bytes_data)

        image = Image.open(img_path)
        im_width, im_height = image.size

        # Specify canvas parameters in application
        drawing_mode = st.sidebar.selectbox(
            "Drawing tool:",
            ("circle", "transform"),
        )

        canvas_result = st_canvas(
            fill_color="rgba(255, 165, 0, 0.3)",  # Fixed fill color with some opacity
            stroke_width=2,
            background_image=image,
            update_streamlit=True,
            height=im_height*im_width/DEFAULT_WIDTH_IMG,
            width=DEFAULT_WIDTH_IMG,
            drawing_mode=drawing_mode,
            display_toolbar=True,
            key="full_app",
        )

        # Do something interesting with the image data and paths
        # if canvas_result.image_data is not None:
        #     st.image(canvas_result.image_data)
        if canvas_result.json_data is not None:
            objects = pd.json_normalize(canvas_result.json_data["objects"])
            for col in objects.select_dtypes(include=["object"]).columns:
                objects[col] = objects[col].astype("str")
            # st.dataframe(objects)
        
        st.button('ROI generation done?', on_click=lambda: input_params_infer(img_path, objects))
            
        # st.image(image, caption='Sunrise by the mountains')

# uploaded_file = st.file_uploader("Choose an image")
img_path = st.text_input("Image file path")
st.button('Process image', on_click=lambda: ROI_creation(img_path))