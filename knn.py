import pickle
import streamlit as st
from PIL import Image
import mysql.connector
import numpy as np
from sklearn.neighbors import KNeighborsClassifier
from streamlit_option_menu import option_menu

# load save model
knn_model = pickle.load(open('knn_model.sav', 'rb'))

# header

app_mode = st.sidebar.selectbox('Select Page', ['Home', 'Proses Klasifikasi'])

if app_mode == 'Home':
    st.title('Aplikasi Klasifikasi Status Gizi Balita')
    st.text("""             Status gizi adalah keadaan yang diakibatkan oleh keseimbangan antara 
            asupan zat gizi dari makanan dengan kebutuhan zat gizi yang diperlukan 
            untuk metabolisme tubuh.""")
    image = Image.open('gizi.jpg')
    st.image(image)

elif app_mode == 'Proses Klasifikasi':
    st.title('Aplikasi Klasifikasi Status Gizi')

    Nama = st.text_input('Nama Balita')
    JK = st.text_input('Jenis Kelamin')
    Alamat = st.text_input('Alamat')
    Usia = st.text_input('Usia')
    Berat = st.number_input('Berat', format="%0f")
    Tinggi = st.number_input('Tinggi', format="%0f")
    prediction = ''

    # membuat button proses
    if st.button('Proses Klasfikasi'):
        knn_model = knn_model.predict([[Berat, Tinggi]])

        if (knn_model == 'Gizi Baik'):
            prediction = 'Status Gizi yaitu Gizi Baik'
        elif (knn_model == 'Gizi Kurang'):
            prediction = 'Status Gizi yaitu Gizi Kurang'
        else:
            prediction = 'Status Gizi yaitu Gizi Lebih'

        st.success(prediction)
