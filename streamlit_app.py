import time
import streamlit as st
import zipfile
import os
import pandas as pd
from urllib.request import urlopen
from PIL import Image


st.title('Welcome to the toy project')
st.markdown(
    '''
## based on the [_Wonders of the world_]\
(https://www.kaggle.com/datasets/karnikakapoor/wonders-of-world) \
dataset

    ''')

if not os.path.exists('data\wonders_of_world.csv'):
    with zipfile.ZipFile("data\wonders_of_the_world.zip","r") as zip_ref:
        zip_ref.extractall("data")
        st.write('Data extracted!')
        st.balloons()
        time.sleep(2)

df = pd.read_csv('data\wonders_of_world.csv')
df.drop(columns=['Type'], inplace=True)
df.drop_duplicates(inplace=True)
df.reset_index(drop=True, inplace=True)
st.subheader('Initial dataframe')
st.dataframe(df.head())

name = st.sidebar.selectbox('Choose a wonder to explore', sorted(df['Name'].unique()))

if name:
    with st.spinner('Please wait...'):
        time.sleep(0.75)
        idx = df[df['Name'] == name].index.values
        caption = df['Name'].iloc[idx].values[0]
        link = df['Picture link'].iloc[idx].values[0]
        st.subheader('Here is an information of your choice ')
        try:
            img = Image.open(urlopen(link))
            st.write(f'A picture of {caption}:')
            st.write(img)
            time.sleep(0.75)
            st.write(f'Link to the picture: {link}')
            st.success('Done!')
        except Exception as err:
            st.error(f'Picture was not found. Due to the following error: {err}')
details = st.sidebar.checkbox(f'More details about {caption}')

if details:
    sub_df = df.iloc[idx].transpose()
    col_to_rename = sub_df.columns.values[0]
    sub_df.rename(columns={col_to_rename: 'Additional info'}, inplace=True)
    st.dataframe(sub_df)
