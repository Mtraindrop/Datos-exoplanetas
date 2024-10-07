from flask import Flask, render_template
import pandas as pd
import matplotlib.pyplot as plt
import base64
from io import BytesIO

app = Flask(__name__)

@app.route('/')
def home():
    # Cargar y procesar datos
    archivo_csv = 'exoplaneta.csv'
    datos = pd.read_csv(archivo_csv, comment='#', on_bad_lines='skip')

    # Filtrar datos
    estrellas_tipo_solar = datos[(datos['st_teff'] >= 5000) & (datos['st_teff'] <= 6000) & 
                                  (datos['st_rad'] >= 0.7) & (datos['st_rad'] <= 1.5)]
    exoplanetas_habitables = estrellas_tipo_solar[(estrellas_tipo_solar['pl_rade'] >= 0.5) & 
                                                  (estrellas_tipo_solar['pl_rade'] <= 2.5)]
    
    # Generar gráfico
    plt.figure(figsize=(10, 6))
    plt.scatter(exoplanetas_habitables['st_teff'], exoplanetas_habitables['pl_rade'], alpha=0.6)
    plt.title('Exoplanetas Habitables')
    plt.xlabel('Temperatura Efectiva de la Estrella (K)')
    plt.ylabel('Radio del Planeta (Radio de la Tierra)')
    plt.grid(True)
    plt.xlim(4000, 7000)
    plt.ylim(0, 3)
    plt.axhline(y=1, color='r', linestyle='--', label='Radio de la Tierra')
    plt.legend()

    # Convertir a base64
    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()

    return render_template('index.html', plot_url=plot_url, exoplanetas=exoplanetas_habitables)

if __name__ == '__main__':
    app.run(debug=True)


