import pickle
import streamlit as st
from PIL import Image
import mysql.connector
import pandas as pd

# load saved model
knn_model = pickle.load(open('knn_model.sav', 'rb'))

# Header


# Menu
app_mode = st.sidebar.selectbox('Aplikasi Klasifikasi', [
                                'Home', 'Proses Klasifikasi', 'Data'])

if app_mode == 'Home':
    st.title('Aplikasi Klasifikasi Status Gizi Balita')
    st.text("""Status gizi adalah keadaan yang diakibatkan oleh keseimbangan antara 
            asupan zat gizi dari makanan dengan kebutuhan zat gizi yang diperlukan 
            untuk metabolisme tubuh.""")
    image = Image.open('gizi.jpg')
    st.image(image)


elif app_mode == 'Proses Klasifikasi':
    st.title('Klasifikasi Status Gizi Balita')
    Nama = st.text_input('Nama Balita')
    JK = st.text_input('Jenis Kelamin')
    Alamat = st.text_input('Alamat')
    Usia = st.number_input('Usia', format="%0f")
    Berat = st.number_input('Berat', format="%0f")
    Tinggi = st.number_input('Tinggi', format="%0f")
    prediction = ''

    # Button Proses Klasifikasi
    if st.button('Proses Klasifikasi'):
        prediction = knn_model.predict([[Berat, Tinggi]])

        if prediction == 'Gizi Baik':
            st.success('Status Gizi: Gizi Baik')
        elif prediction == 'Gizi Kurang':
            st.success('Status Gizi: Gizi Kurang')
        else:
            st.success('Status Gizi: Gizi Lebih')

        st.write('Nama : ', Nama)
        st.write('Jenis Kelamin : ', JK)
        st.write('Alamat : ', Alamat)
        st.write('Usia : ', Usia)
        st.write('Berat : ', Berat)
        st.write('Tinggi : ', Tinggi)
        st.write('Status Gizi : ', prediction)

        db = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="",
            database="db_gizi"
        )

        cursor = db.cursor()
        sql = "INSERT INTO tbl_balita(Nama, JK, Alamat, Usia, Berat, Tinggi, prediction) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        val = (Nama, JK, Alamat, Usia, Berat, Tinggi, prediction)
        cursor.execute(sql, val)
        st.success("Data berhasil disimpan")
        db.commit()

elif app_mode == 'Data':
    try:
        # Membuat koneksi ke database
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="",
            database="db_gizi"
        )

        # Membuat cursor
        cursor = db.cursor()

        # Menjalankan pernyataan SQL SELECT
        sql = "SELECT Nama, JK, Alamat, Usia, Berat, Tinggi, prediction FROM tbl_balita"
        cursor.execute(sql)

      # Mengambil semua data dari hasil query
        data = cursor.fetchall()

        # Menampilkan data dalam bentuk DataFrame
        df = pd.DataFrame(data, columns=[
                          "Nama", "Jenis Kelamin", "Alamat", "Usia", "Berat", "Tinggi", "Prediction"])

        # Menampilkan data dalam bentuk tabel HTML tanpa indeks
        st.write(df.to_html(index=False, escape=False), unsafe_allow_html=True)

    except mysql.connector.Error as e:
        st.error(
            f"Terjadi kesalahan dalam mengambil data dari database: {str(e)}")

    finally:
        # Menutup koneksi ke database
        if db.is_connected():
            cursor.close()
            db.close()
