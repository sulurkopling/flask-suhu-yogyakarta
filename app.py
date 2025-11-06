import matplotlib
matplotlib.use('Agg')
from flask import Flask, render_template
import requests
import pandas as pd
import matplotlib.pyplot as plt

app = Flask(__name__)

@app.route('/')
def home():
    # Ambil data suhu Yogyakarta dari API Open Meteo
    url = "https://api.open-meteo.com/v1/forecast?latitude=-7.7972&longitude=110.3688&hourly=temperature_2m"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        
        # Buat DataFrame dari data JSON
        df = pd.DataFrame({
            'Waktu': data['hourly']['time'],
            'Suhu (°C)': data['hourly']['temperature_2m']
        })
        df['Waktu'] = pd.to_datetime(df['Waktu'])
        
        # Buat grafik suhu dan simpan di folder static
        plt.figure(figsize=(9,4))
        plt.plot(df['Waktu'], df['Suhu (°C)'], color='tomato', linewidth=2)
        plt.title('Perubahan Suhu Realtime di Yogyakarta', fontsize=13, fontweight='bold')
        plt.xlabel('Waktu')
        plt.ylabel('Suhu (°C)')
        plt.xticks(rotation=45)
        plt.grid(alpha=0.4)
        plt.tight_layout()
        plt.savefig('static/grafik_suhu.png', dpi=300)
        plt.close()
        
        # Ambil 10 data terakhir untuk ditampilkan di tabel
        table_data = df.tail(10).to_html(classes='table table-striped text-center', index=False)
        return render_template('index.html', table_data=table_data)
    else:
        return f"Terjadi kesalahan koneksi ke API: {response.status_code}"

if __name__ == '__main__':
    app.run(debug=True)
