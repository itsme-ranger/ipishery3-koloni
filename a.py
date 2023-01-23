import streamlit as st
import pandas as pd
import numpy as np

def rgb_to_hex(rgb):
    return '%02x%02x%02x' % rgb

def style_specific_cell(x, i, rgb_color):
    color = f'background-color: #{rgb_to_hex(rgb_color)}'
    df1 = pd.DataFrame('', index=x.index, columns=x.columns)
    df1["colour"].iloc[i] = color
    return df1

colours = [
    (69,60,62),
    (151,139,58)
]

df = pd.DataFrame(
    {
        'colour': ["", ""],
        'area_total_px': [1230, 900],
        'occurences' : [200,50]
    }
)
for i, row in enumerate(colours):
    df.style.apply(lambda x: style_specific_cell(x, i, row), axis = 0)

# df = pd.DataFrame(
#    np.random.randn(50, 20),
#    columns=('col %d' % i for i in range(20)))

from PIL import Image

image = Image.open('4-57-vibrio-annotated-pseudo.jpg')

st.image(image, caption='4-57-vibrio-annotated-pseudo')
st.dataframe(df)  # Same as st.write(df)