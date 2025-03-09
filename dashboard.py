import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Set page configuration
st.set_page_config(
    page_title="Bike Sharing Dashboard",
    page_icon="🚲",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS untuk tampilan yang lebih minimalis dengan perbaikan warna insight
st.markdown("""
<style>
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    .st-emotion-cache-16txtl3 h1 {
        font-weight: 700;
        margin-bottom: 1rem;
    }
    .st-emotion-cache-10trblm {
        margin-bottom: 1rem;
    }
    .insight-box {
        background-color: #f8f9fa;
        border-left: 4px solid #4e78a8;
        padding: 1rem;
        border-radius: 0.3rem;
        margin: 1rem 0;
        color: #333333;  /* Warna teks gelap untuk memastikan terlihat */
    }
    .conclusion-box {
        background-color: #f0f7ff;
        border-left: 4px solid #3366cc;
        padding: 1rem;
        border-radius: 0.3rem;
        margin: 1rem 0;
        color: #333333;  /* Warna teks gelap */
    }
    .recommendation-box {
        background-color: #f0fff7;
        border-left: 4px solid #33cc99;
        padding: 1rem;
        border-radius: 0.3rem;
        margin: 1rem 0;
        color: #333333;  /* Warna teks gelap */
    }
    /* Tambahan style untuk insight header */
    .insight-header {
        background-color: #4e78a8;
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 0.3rem 0.3rem 0 0;
        margin-bottom: 0;
        font-weight: bold;
    }
    /* Style tambahan untuk text di dalam insight */
    .insight-content {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 0 0 0.3rem 0.3rem;
        color: #333333;
    }
</style>
""", unsafe_allow_html=True)

# Definisikan mapping
season_mapping = {1: "Spring", 2: "Summer", 3: "Fall", 4: "Winter"}
weathersit_mapping = {1: "Clear", 2: "Misty", 3: "Light Rain/Snow", 4: "Heavy Rain/Snow"}
weekday_mapping = {0: 'Minggu', 1: 'Senin', 2: 'Selasa', 3: 'Rabu', 4: 'Kamis', 5: 'Jumat', 6: 'Sabtu'}

# Load data
@st.cache_data
def load_data():
    day_df = pd.read_csv("https://raw.githubusercontent.com/fenia-k/Bike-Sharing-Dataset/refs/heads/main/day.csv")
    hour_df = pd.read_csv("https://raw.githubusercontent.com/fenia-k/Bike-Sharing-Dataset/refs/heads/main/hour.csv")
    
    # Mengubah tipe data
    day_df['dteday'] = pd.to_datetime(day_df['dteday'])
    hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])
    
    # Mengubah nilai kategorik
    day_df["season_name"] = day_df["season"].map(season_mapping)
    day_df["weathersit_name"] = day_df["weathersit"].map(weathersit_mapping)
    day_df["weekday_name"] = day_df["weekday"].map(weekday_mapping)
    
    hour_df["season_name"] = hour_df["season"].map(season_mapping)
    hour_df["weathersit_name"] = hour_df["weathersit"].map(weathersit_mapping)
    
    # Menambahkan kolom bulan untuk analisis
    day_df['month'] = day_df['dteday'].dt.month
    day_df['month_name'] = day_df['dteday'].dt.strftime('%b')
    
    return day_df, hour_df

day_df, hour_df = load_data()

# Sidebar
with st.sidebar:
    st.title("Bike Sharing Analysis")
    
    st.subheader("Filter Data")
    
    # Date filter
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Tanggal Mulai", day_df['dteday'].min().date())
    with col2:
        end_date = st.date_input("Tanggal Akhir", day_df['dteday'].max().date())
    
    # Season filter
    season_options = list(season_mapping.values())
    selected_seasons = st.multiselect("Musim", 
                                     options=season_options,
                                     default=season_options)
    
    # Weather filter
    weather_options = list(weathersit_mapping.values())
    selected_weather = st.multiselect("Kondisi Cuaca", 
                                     options=weather_options,
                                     default=weather_options)
    
    # About section
    st.markdown("---")
    st.caption("Dibuat oleh: Fenia Kerenina br Surbakti")
    st.caption("ID Dicoding: MC185D5X0359")

# Filter data berdasarkan input
filtered_day_df = day_df[
    (day_df['dteday'].dt.date >= start_date) & 
    (day_df['dteday'].dt.date <= end_date) &
    (day_df['season_name'].isin(selected_seasons)) &
    (day_df['weathersit_name'].isin(selected_weather))
]

filtered_hour_df = hour_df[
    (hour_df['dteday'].dt.date >= start_date) & 
    (hour_df['dteday'].dt.date <= end_date) &
    (hour_df['season_name'].isin(selected_seasons)) &
    (hour_df['weathersit_name'].isin(selected_weather))
]

# Main content
st.title("🚲 Bike Sharing Analysis Dashboard")
st.markdown("Dashboard untuk menganalisis pola peminjaman sepeda berdasarkan musim, cuaca, dan jenis pengguna.")

# Metrics overview
st.subheader("Overview")
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Peminjaman", f"{filtered_day_df['cnt'].sum():,}")
with col2:
    st.metric("Rata-rata Harian", f"{filtered_day_df['cnt'].mean():.1f}")
with col3:
    st.metric("Pengguna Casual", f"{filtered_day_df['casual'].sum():,}")
with col4:
    st.metric("Pengguna Registered", f"{filtered_day_df['registered'].sum():,}")

# Pertanyaan 1
st.markdown("---")
st.header("Pertanyaan 1: Bagaimana pola peminjaman sepeda berubah berdasarkan musim dan kondisi cuaca?")

# Tab untuk berbagai visualisasi pertanyaan 1
tab1, tab2, tab3 = st.tabs(["Peminjaman per Musim & Cuaca", "Tren Bulanan", "Pola Peminjaman Harian"])

with tab1:
    col1, col2 = st.columns(2)
    
    with col1:
        # Visualisasi musim dengan Matplotlib
        st.subheader("Rata-rata Peminjaman per Musim")
        season_data = filtered_day_df.groupby("season_name")["cnt"].mean().reset_index()
        fig1, ax1 = plt.subplots(figsize=(10, 6))
        sns.barplot(x="season_name", y="cnt", data=season_data, ax=ax1, order=["Spring", "Summer", "Fall", "Winter"])
        ax1.set_title("Rata-rata Peminjaman Sepeda per Musim")
        ax1.set_xlabel("Musim")
        ax1.set_ylabel("Rata-rata Jumlah Peminjaman")
        st.pyplot(fig1)

    with col2:
        # Visualisasi kondisi cuaca dengan Matplotlib
        st.subheader("Rata-rata Peminjaman per Kondisi Cuaca")
        weather_data = filtered_day_df.groupby("weathersit_name")["cnt"].mean().reset_index()
        fig2, ax2 = plt.subplots(figsize=(10, 6))
        sns.barplot(x="weathersit_name", y="cnt", data=weather_data, ax=ax2)
        ax2.set_title("Rata-rata Peminjaman Sepeda per Kondisi Cuaca")
        ax2.set_xlabel("Kondisi Cuaca")
        ax2.set_ylabel("Rata-rata Jumlah Peminjaman")
        st.pyplot(fig2)
    
    # Visualisasi interaksi musim dan cuaca
    st.subheader("Interaksi Musim dan Kondisi Cuaca")
    season_weather_data = filtered_day_df.groupby(["season_name", "weathersit_name"])["cnt"].mean().reset_index()
    fig3, ax3 = plt.subplots(figsize=(12, 6))
    sns.barplot(x="season_name", y="cnt", hue="weathersit_name", data=season_weather_data, ax=ax3, order=["Spring", "Summer", "Fall", "Winter"])
    ax3.set_title("Interaksi Musim dan Kondisi Cuaca terhadap Peminjaman Sepeda")
    ax3.set_xlabel("Musim")
    ax3.set_ylabel("Rata-rata Jumlah Peminjaman")
    st.pyplot(fig3)

with tab2:
    # Tren peminjaman bulanan berdasarkan musim
    st.subheader("Tren Peminjaman Sepeda Bulanan berdasarkan Musim")
    monthly_season_data = filtered_day_df.groupby(['month', 'month_name', 'season_name'])['cnt'].mean().reset_index()
    
    fig4, ax4 = plt.subplots(figsize=(12, 6))
    
    for season in season_mapping.values():
        season_data = monthly_season_data[monthly_season_data['season_name'] == season]
        ax4.plot(season_data['month'], season_data['cnt'], marker='o', label=season)
    
    # Custom x-axis labels
    month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    ax4.set_xticks(range(1, 13))
    ax4.set_xticklabels(month_names)
    ax4.set_xlabel('Bulan')
    ax4.set_ylabel('Rata-rata Jumlah Peminjaman')
    ax4.set_title('Tren Peminjaman Sepeda Bulanan berdasarkan Musim')
    ax4.legend()
    ax4.grid(True, alpha=0.3)
    
    st.pyplot(fig4)
    
    # Tren peminjaman bulanan berdasarkan kondisi cuaca
    st.subheader("Tren Peminjaman Sepeda Bulanan berdasarkan Kondisi Cuaca")
    monthly_weather_data = filtered_day_df.groupby(['month', 'month_name', 'weathersit_name'])['cnt'].mean().reset_index()
    
    fig5, ax5 = plt.subplots(figsize=(12, 6))
    
    for weather in weather_options:
        weather_data = monthly_weather_data[monthly_weather_data['weathersit_name'] == weather]
        ax5.plot(weather_data['month'], weather_data['cnt'], marker='o', label=weather)
    
    ax5.set_xticks(range(1, 13))
    ax5.set_xticklabels(month_names)
    ax5.set_xlabel('Bulan')
    ax5.set_ylabel('Rata-rata Jumlah Peminjaman')
    ax5.set_title('Tren Peminjaman Sepeda Bulanan berdasarkan Kondisi Cuaca')
    ax5.legend()
    ax5.grid(True, alpha=0.3)
    
    st.pyplot(fig5)

with tab3:
    # Analisis pola harian
    st.subheader("Pola Peminjaman Sepeda Berdasarkan Jam")
    hourly_data = filtered_hour_df.groupby('hr')['cnt'].mean().reset_index()
    
    fig6, ax6 = plt.subplots(figsize=(12, 6))
    sns.lineplot(x='hr', y='cnt', data=hourly_data, marker='o', ax=ax6)
    ax6.set_title("Pola Peminjaman Sepeda Berdasarkan Jam")
    ax6.set_xlabel("Jam")
    ax6.set_ylabel("Rata-rata Jumlah Peminjaman")
    ax6.grid(True, alpha=0.3)
    
    st.pyplot(fig6)
    
    # Heatmap jam dan hari
    st.subheader("Heatmap Peminjaman Sepeda berdasarkan Jam dan Hari")
    hour_weekday_data = filtered_hour_df.groupby(['hr', 'weekday'])['cnt'].mean().reset_index()
    hour_weekday_pivot = hour_weekday_data.pivot(index='hr', columns='weekday', values='cnt')
    
    fig7, ax7 = plt.subplots(figsize=(12, 8))
    sns.heatmap(
        hour_weekday_pivot, 
        cmap="viridis", 
        ax=ax7,
        cbar_kws={'label': 'Jumlah Peminjaman'}
    )
    ax7.set_title("Heatmap Peminjaman Sepeda berdasarkan Jam dan Hari")
    ax7.set_xlabel("Hari")
    ax7.set_ylabel("Jam")
    ax7.set_xticklabels([weekday_mapping[i] for i in range(7)])
    
    st.pyplot(fig7)

# Insight untuk pertanyaan 1
st.markdown("""
<div class="insight-header">Insight:</div>
<div class="insight-content">
<ul>
    <li>Musim Gugur (Fall) menunjukkan jumlah peminjaman sepeda tertinggi, diikuti oleh Musim Panas (Summer).</li>
    <li>Musim Semi (Spring) dan Musim Dingin (Winter) memiliki peminjaman lebih rendah.</li>
    <li>Cuaca Cerah (Clear) konsisten menghasilkan peminjaman tertinggi, sementara peminjaman menurun signifikan pada cuaca buruk/hujan.</li>
    <li>Bulan Mei hingga September (musim panas dan gugur) menunjukkan aktivitas tertinggi, sedangkan Januari-Februari terendah.</li>
    <li>Terdapat dua puncak peminjaman harian: pagi hari (7-9) dan sore hari (17-19), menunjukkan pola komuter.</li>
</ul>
</div>
""", unsafe_allow_html=True)

# Pertanyaan 2
st.markdown("---")
st.header("Pertanyaan 2: Bagaimana perbedaan perilaku antara pengguna biasa (casual) dan pengguna terdaftar (registered) dalam peminjaman sepeda?")

# Tab untuk berbagai visualisasi pertanyaan 2
tab1, tab2, tab3 = st.tabs(["Perbandingan Total", "Pola Mingguan", "Analisis Segmen"])

with tab1:
    # Perbandingan total casual vs registered
    st.subheader("Perbandingan Total Peminjaman Berdasarkan Tipe Pengguna")
    total_casual = filtered_day_df['casual'].sum()
    total_registered = filtered_day_df['registered'].sum()
    
    comparison_data = pd.DataFrame({
        'Tipe Pengguna': ['Casual', 'Registered'],
        'Jumlah Peminjaman': [total_casual, total_registered]
    })
    
    fig8, ax8 = plt.subplots(figsize=(10, 6))
    ax8.pie(
        comparison_data['Jumlah Peminjaman'],
        labels=comparison_data['Tipe Pengguna'],
        autopct='%1.1f%%',
        startangle=90,
        colors=['#1f77b4', '#ff7f0e']
    )
    ax8.axis('equal')
    ax8.set_title('Perbandingan Total Peminjaman Berdasarkan Tipe Pengguna')
    
    st.pyplot(fig8)
    
    # Tren peminjaman per musim
    st.subheader("Perbandingan Peminjaman berdasarkan Musim dan Tipe Pengguna")
    seasonal_user_data = filtered_day_df.groupby('season_name')[['casual', 'registered']].mean().reset_index()
    seasonal_user_data_melted = seasonal_user_data.melt(
        id_vars='season_name',
        value_vars=['casual', 'registered'],
        var_name='Tipe Pengguna',
        value_name='Rata-rata Peminjaman'
    )
    
    fig9, ax9 = plt.subplots(figsize=(12, 6))
    sns.barplot(
        x='season_name',
        y='Rata-rata Peminjaman',
        hue='Tipe Pengguna',
        data=seasonal_user_data_melted,
        ax=ax9,
        order=["Spring", "Summer", "Fall", "Winter"]
    )
    ax9.set_title('Perbandingan Peminjaman berdasarkan Musim dan Tipe Pengguna')
    ax9.set_xlabel('Musim')
    ax9.set_ylabel('Rata-rata Jumlah Peminjaman')
    
    st.pyplot(fig9)

with tab2:
    # Pola peminjaman berdasarkan hari dalam seminggu
    st.subheader("Pola Peminjaman Berdasarkan Hari dalam Seminggu")
    weekday_data = filtered_day_df.groupby('weekday_name')[['casual', 'registered']].mean().reset_index()
    weekday_data_melted = weekday_data.melt(
        id_vars='weekday_name',
        value_vars=['casual', 'registered'],
        var_name='Tipe Pengguna',
        value_name='Rata-rata Peminjaman'
    )
    
    # Custom weekday order
    weekday_order = ['Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu', 'Minggu']
    weekday_data_melted['weekday_name'] = pd.Categorical(
        weekday_data_melted['weekday_name'], 
        categories=weekday_order, 
        ordered=True
    )
    weekday_data_melted = weekday_data_melted.sort_values('weekday_name')
    
    fig10, ax10 = plt.subplots(figsize=(12, 6))
    sns.barplot(
        x='weekday_name',
        y='Rata-rata Peminjaman',
        hue='Tipe Pengguna',
        data=weekday_data_melted,
        ax=ax10
    )
    ax10.set_title('Pola Peminjaman Berdasarkan Hari dalam Seminggu')
    ax10.set_xlabel('Hari')
    ax10.set_ylabel('Rata-rata Jumlah Peminjaman')
    
    st.pyplot(fig10)
    
    # Pola peminjaman berdasarkan jam
    st.subheader("Pola Peminjaman Berdasarkan Jam dan Tipe Pengguna")
    hourly_user_data = filtered_hour_df.groupby('hr')[['casual', 'registered']].mean().reset_index()
    hourly_user_data_melted = hourly_user_data.melt(
        id_vars='hr',
        value_vars=['casual', 'registered'],
        var_name='Tipe Pengguna',
        value_name='Rata-rata Peminjaman'
    )
    
    fig11, ax11 = plt.subplots(figsize=(12, 6))
    sns.lineplot(
        x='hr',
        y='Rata-rata Peminjaman',
        hue='Tipe Pengguna',
        data=hourly_user_data_melted,
        marker='o',
        ax=ax11
    )
    ax11.set_title('Pola Peminjaman Berdasarkan Jam dan Tipe Pengguna')
    ax11.set_xlabel('Jam')
    ax11.set_ylabel('Rata-rata Jumlah Peminjaman')
    ax11.grid(True, alpha=0.3)
    
    st.pyplot(fig11)

with tab3:
    # Analisis segmentasi pengguna
    st.subheader("Visualisasi segmentasi pengguna")
    
    # Analisis workingday vs holiday untuk casual/registered
    st.subheader("Peminjaman Berdasarkan Tipe Hari dan Tipe Pengguna")
    workingday_data = filtered_day_df.groupby(['workingday'])[['casual', 'registered']].mean().reset_index()
    workingday_data['workingday'] = workingday_data['workingday'].map({0: 'Libur/Akhir Pekan', 1: 'Hari Kerja'})
    workingday_data_melted = workingday_data.melt(
        id_vars='workingday',
        value_vars=['casual', 'registered'],
        var_name='Tipe Pengguna',
        value_name='Rata-rata Peminjaman'
    )
    
    fig12, ax12 = plt.subplots(figsize=(10, 6))
    sns.barplot(
        x='workingday',
        y='Rata-rata Peminjaman',
        hue='Tipe Pengguna',
        data=workingday_data_melted,
        ax=ax12
    )
    ax12.set_title('Peminjaman Berdasarkan Tipe Hari dan Tipe Pengguna')
    ax12.set_xlabel('Tipe Hari')
    ax12.set_ylabel('Rata-rata Jumlah Peminjaman')
    
    st.pyplot(fig12)
    
    # Proporsi casual vs registered berdasarkan kondisi cuaca
    st.subheader("Pengaruh Kondisi Cuaca terhadap Tipe Pengguna")
    weather_user_data = filtered_day_df.groupby('weathersit_name')[['casual', 'registered']].mean().reset_index()
    weather_user_data_melted = weather_user_data.melt(
        id_vars='weathersit_name',
        value_vars=['casual', 'registered'],
        var_name='Tipe Pengguna',
        value_name='Rata-rata Peminjaman'
    )
    
    fig13, ax13 = plt.subplots(figsize=(12, 6))
    sns.barplot(
        x='weathersit_name',
        y='Rata-rata Peminjaman',
        hue='Tipe Pengguna',
        data=weather_user_data_melted,
        ax=ax13
    )
    ax13.set_title('Pengaruh Kondisi Cuaca terhadap Tipe Pengguna')
    ax13.set_xlabel('Kondisi Cuaca')
    ax13.set_ylabel('Rata-rata Jumlah Peminjaman')
    
    st.pyplot(fig13)

# Insight untuk pertanyaan 2
st.markdown("""
<div class="insight-header">Insight:</div>
<div class="insight-content">
<ul>
    <li>Pengguna registered mendominasi total peminjaman dengan pola penggunaan yang lebih konsisten sepanjang tahun.</li>
    <li>Pengguna casual menunjukkan peningkatan signifikan pada akhir pekan, sementara registered lebih stabil pada hari kerja.</li>
    <li>Pola harian registered menunjukkan dua puncak (pagi dan sore) yang mencerminkan pola komuter, sementara casual memiliki puncak tunggal di siang hingga sore hari.</li>
    <li>Cuaca memiliki dampak lebih besar pada pengguna casual dibandingkan registered, dengan penurunan lebih tajam saat cuaca buruk.</li>
    <li>Hari libur dan akhir pekan menunjukkan peningkatan peminjaman casual sebesar 2x lipat, sementara registered cenderung menurun.</li>
</ul>
</div>
""", unsafe_allow_html=True)

# Kesimpulan dan rekomendasi
st.markdown("---")
st.header("Kesimpulan dan Rekomendasi")

# Kesimpulan
st.markdown("""
<div class="conclusion-box">
<h3>Kesimpulan:</h3>
<p>Peminjaman sepeda mencapai puncak pada musim gugur (211.53) dan musim panas (189.46), dengan penurunan signifikan pada musim semi (108.41) dan musim dingin (180.87). Cuaca cerah konsisten menghasilkan peminjaman tertinggi (185.31), sementara cuaca mendung (162.06) dan hujan (106.05) mengurangi jumlah peminjaman secara bertahap. Bulan Mei-September menunjukkan aktivitas tertinggi, sedangkan Januari-Februari terendah. Faktor cuaca memiliki dampak lebih besar pada musim dingin, dengan penurunan ekstrem saat hujan.</p>

<p>Pengguna registered mendominasi total peminjaman dengan pola penggunaan yang lebih konsisten sepanjang tahun dan lebih stabil pada hari kerja, menunjukkan penggunaan untuk komuter rutin. Pengguna casual menunjukkan fluktuasi lebih ekstrem berdasarkan musim, meningkat pada akhir pekan dan menurun drastis saat musim dingin atau cuaca buruk, mengindikasikan penggunaan rekreasional. Analisis pola menunjukkan sebagian besar pengguna termasuk kategori aktif, dengan perbedaan waktu penggunaan yang jelas antara kedua segmen.</p>
</div>
""", unsafe_allow_html=True)

# Rekomendasi
st.markdown("""
<div class="recommendation-box">
<h3>Rekomendasi:</h3>
<h4>1. Strategi Marketing:</h4>
<ul>
    <li>Meningkatkan promosi untuk mengkonversi pengguna casual menjadi registered dengan penawaran khusus pada akhir musim semi.</li>
    <li>Membuat "Weekend Pass" dengan insentif khusus untuk pengguna casual yang sering bersepeda pada akhir pekan.</li>
    <li>Program loyalitas musiman dengan diskon untuk pengguna registered selama musim dingin dan cuaca buruk.</li>
</ul>

<h4>2. Manajemen Operasional:</h4>
<ul>
    <li>Distribusi sepeda berbasis lokasi dan waktu - fokus pada area perkantoran pagi/sore hari dan area rekreasi siang/akhir pekan.</li>
    <li>Mengurangi armada beroperasi saat cuaca buruk dan mengalokasikan untuk pemeliharaan.</li>
    <li>Meningkatkan ketersediaan sepeda di area transit pada jam puncak pengguna registered (7-9 pagi, 17-19 sore).</li>
</ul>

<h4>3. Pengembangan Produk:</h4>
<ul>
    <li>Penambahan fitur perlindungan cuaca sederhana pada sepeda untuk meminimalkan dampak cuaca mendung/hujan ringan.</li>
    <li>Pengembangan paket langganan fleksibel untuk casual users dengan opsi penggunaan akhir pekan.</li>
    <li>Implementasi teknologi untuk memudahkan transisi dari pengguna casual ke registered, seperti upgrade membership langsung dari aplikasi.</li>
</ul>
</div>
""", unsafe_allow_html=True)

# Footer
st.markdown("---")
st.caption("© 2025 Bike Sharing Analysis Project | MC185D5X0359")