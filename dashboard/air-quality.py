import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the data
data = pd.read_csv('PRSA_Data_Aotizhongxin_20130301-20170228.csv')

# Set up the page
st.title("Dashboard Harian Kualitas Udara Aotizhongxin (2013-2017)")
st.sidebar.title("Pilih Menu")
menu = st.sidebar.radio("Menu", ["Dashboard Harian", "Hasil Analisis Kualitas Udara"])

# Memilih menu
if menu == "Dashboard Harian":
    # Header untuk informasi AQI
    st.header("Dashboard Harian Kualitas Udara Aotizhongxin")
    selected_date = st.date_input("Pilih Tanggal", value=pd.to_datetime("2013-03-01"))

    # Filter data berdasarkan tanggal
    filtered_data = data[(data['year'] == selected_date.year) & 
                         (data['month'] == selected_date.month) & 
                         (data['day'] == selected_date.day)]

    if not filtered_data.empty:
        # Tampilkan nilai AQI (contoh menggunakan PM2.5 sebagai AQI)
        pm25_value = filtered_data['PM2.5'].mean()  # Mengambil nilai rata-rata PM2.5 untuk tanggal tersebut
        aqi_status = "GOOD"  # Status bisa ditentukan berdasarkan nilai PM2.5
        if pm25_value > 35:  # Misal threshold untuk status MODERATE
            aqi_status = "MODERATE"
        if pm25_value > 55:  # Misal threshold untuk status UNHEALTHY
            aqi_status = "UNHEALTHY"

        # Tampilkan nilai AQI
        st.metric(label="AQI (PM2.5)", value=pm25_value, delta=f"{(pm25_value - filtered_data['PM2.5'].min()):.2f}%")
        st.write(f"Status Kualitas Udara: **{aqi_status}**")

        # Tampilkan tingkat polutan lainnya
        st.subheader("Tingkat Polutan")
        st.write(f"Tingkat PM10: {filtered_data['PM10'].mean():.2f} μg/m³")
        st.write(f"Tingkat SO2: {filtered_data['SO2'].mean():.2f} μg/m³")
        st.write(f"Tingkat NO2: {filtered_data['NO2'].mean():.2f} μg/m³")
        st.write(f"Tingkat CO: {filtered_data['CO'].mean():.2f} μg/m³")
        st.write(f"Tingkat O3: {filtered_data['O3'].mean():.2f} μg/m³")
        st.write(f"Suhu: {filtered_data['TEMP'].mean():.2f} °C")
        st.write(f"Kelembaban: {filtered_data['DEWP'].mean():.2f} °C")
    else:
        st.write("Data tidak ditemukan untuk tanggal yang dipilih.")

    # Sumber Data
    st.write("Sumber Data: Stasiun Aotizhongxin (2013-2017)")

    # Keterangan Status Kualitas Udara
    st.subheader("Keterangan Status Kualitas Udara:")
    status_descriptions = {
        "GOOD": "Kualitas udara baik dan tidak berbahaya bagi kesehatan.",
        "MODERATE": "Kualitas udara masih dapat ditoleransi, tetapi beberapa individu mungkin mengalami efek sementara.",
        "UNHEALTHY": "Kualitas udara sangat buruk dan dapat mempengaruhi kesehatan secara umum."
    }

    # Menampilkan deskripsi status berdasarkan nilai AQI
    st.write(f"Status Kualitas Udara: **{aqi_status}**")
    st.write(status_descriptions[aqi_status])

    # Sumber
    st.write("Sumber: EPA Air Quality Index (AQI)")

elif menu == "Hasil Analisis Kualitas Udara":
    st.header("Analisis Kualitas Udara Bulanan")
    
    # Data polusi udara bulanan
    monthly_pollution = pd.DataFrame({
        'month': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
        'PM2.5': [84.44, 79.61, 94.97, 78.31, 66.71, 70.43, 74.86, 55.85, 64.21, 91.15, 93.54, 90.47],
        'PM10': [107.41, 100.12, 144.79, 129.09, 113.35, 86.32, 84.68, 72.07, 87.07, 118.06, 119.66, 121.78],
        'SO2': [27.32, 24.29, 25.57, 15.71, 14.93, 8.35, 5.71, 4.45, 7.03, 10.35, 14.89, 23.68],
        'NO2': [65.08, 54.28, 63.01, 52.75, 48.90, 49.27, 47.72, 48.48, 59.21, 72.99, 72.32, 70.02],
        'CO': [1598.03, 1306.38, 1300.67, 843.60, 791.84, 902.07, 828.32, 779.97, 909.32, 1159.14, 1626.42, 1625.14],
        'O3': [27.14, 43.15, 47.29, 64.05, 84.82, 89.49, 90.98, 81.67, 51.00, 27.71, 17.10, 20.29]
    })

    # Plotting
    st.subheader("Rata-rata Polusi Udara Berdasarkan Bulan")
    monthly_pollution.set_index('month')[['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3']].plot(kind='bar', figsize=(10, 6))
    plt.title('Rata-rata Polusi Udara Berdasarkan Bulan')
    plt.ylabel('Konsentrasi Polutan (µg/m³)')
    plt.xlabel('Bulan')
    
    # Tampilkan grafik di Streamlit
    st.pyplot(plt)
    plt.clf()  # Clear the figure after displaying it

        # Data kualitas udara tahunan
    yearly_pollution = pd.DataFrame({
        'year': [2013, 2014, 2015, 2016, 2017],
        'PM2.5': [80.459504, 85.406085, 77.406254, 71.189658, 83.369192],
        'PM10': [111.640114, 118.458710, 108.062078, 92.187785, 99.873234],
        'SO2': [19.970371, 17.394235, 13.208761, 10.272484, 18.824859],
        'NO2': [63.137587, 62.784810, 60.329914, 48.227630, 65.413489],
        'CO': [1113.021446, 1110.981735, 1223.584475, 1077.248406, 1300.423729],
        'O3': [46.251400, 47.723858, 61.104532, 59.855988, 47.436088]
    })

    # Plotting
    st.subheader("Rata-rata Polusi Udara Berdasarkan Tahun")
    yearly_pollution.set_index('year')[['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3']].plot(kind='bar', figsize=(10, 6))
    plt.title('Rata-rata Polusi Udara Berdasarkan Tahun')
    plt.ylabel('Konsentrasi Polutan (µg/m³)')
    plt.xlabel('Tahun')
    
    # Tampilkan grafik di Streamlit
    st.pyplot(plt)

        # Menghitung matriks korelasi
    corr_matrix = yearly_pollution[['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3']].corr()

    # Membuat heatmap dengan seaborn
    plt.figure(figsize=(10, 8))
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', vmin=-1, vmax=1)
    plt.title('Matriks Korelasi Polutan Udara')
    
    # Tampilkan heatmap di Streamlit
    st.pyplot(plt)
 
     # Batas AQI untuk PM2.5
    bins = [0, 50, 100, 150, 200, 300, float('inf')]
    labels = ['Good', 'Moderate', 'Unhealthy for Sensitive Groups', 'Unhealthy', 'Very Unhealthy', 'Hazardous']
    
    # Mengkategorikan kualitas udara berdasarkan PM2.5 untuk seluruh dataset
    data['PM2.5_AQI'] = pd.cut(data['PM2.5'], bins=bins, labels=labels)
    
    # Mengelompokkan berdasarkan tahun dan kategori AQI
    annual_aqi_counts = data.groupby(['year', 'PM2.5_AQI']).size().unstack(fill_value=0)
    
    # Menentukan warna sesuai standar AQI
    colors = {
        'Good': '#00E400',                       # Hijau
        'Moderate': '#FFFF00',                  # Kuning
        'Unhealthy for Sensitive Groups': '#FFA500',  # Jingga
        'Unhealthy': '#FF0000',                 # Merah
        'Very Unhealthy': '#800080',            # Ungu
        'Hazardous': '#7E0023'                  # Merah Marun
    }
    
    # Membuat plot
    plt.figure(figsize=(12, 6))
    annual_aqi_counts.plot(kind='bar', stacked=True, color=[colors[label] for label in annual_aqi_counts.columns], figsize=(12, 6))
    
    # Menambahkan judul dan label
    plt.title('Kualitas Udara tahunan berdasarkan jumlah PM2.5 setiap harinya', fontsize=16)
    plt.xlabel('Tahun', fontsize=12)
    plt.ylabel('frekuensi nilai PM2.5', fontsize=12)
    plt.xticks(rotation=45)
    
    # Menyesuaikan tata letak dan menampilkan plot
    plt.tight_layout()
    plt.show()
    
    # Print jumlah harian per kategori AQI per tahun
    print(annual_aqi_counts)
    
    # Print seluruh data dengan kategori AQI untuk dilihat
    print(data[['PM2.5', 'PM2.5_AQI']])
    st.pyplot(plt)
