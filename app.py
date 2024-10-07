from flask import Flask, render_template
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import base64
from io import BytesIO

app = Flask(__name__)

@app.route('/')
def home():
    archivo_csv = 'exoplaneta.csv'
    datos = pd.read_csv(archivo_csv, comment='#', on_bad_lines='skip')

    # Limpieza de nombres de columnas
    datos.columns = datos.columns.str.strip()

    # Filtrado de los 50 exoplanetas más cercanos
    exoplanetas_cercanos = datos.nsmallest(50, 'st_dist')  # Asegúrate de que 'st_dist' exista en tu CSV

    # Gráfico 1: Evolución del Radio Planetario de los 50 exoplanetas más cercanos
    plt.figure(figsize=(14, 8))
    for planeta in exoplanetas_cercanos['pl_name']:
        datos_planeta = exoplanetas_cercanos[exoplanetas_cercanos['pl_name'] == planeta]
        if not datos_planeta.empty:
            plt.plot(datos_planeta['releasedate'], datos_planeta['pl_rade'], marker='o', label=planeta)
    plt.title('Evolución del Radio Planetario de los 50 Exoplanetas Más Cercanos')
    plt.xlabel('Fecha de Publicación/Actualización')
    plt.ylabel('Radio Planetario [Radio de la Tierra]')
    plt.legend()
    plt.grid(True)

    # Convertir el gráfico a imagen base64
    img1 = BytesIO()
    plt.savefig(img1, format='png')
    img1.seek(0)
    plot_url1 = base64.b64encode(img1.getvalue()).decode()

    # Gráfico 2: Temperatura Efectiva de la Estrella vs. Radio del Planeta de los 50 exoplanetas más cercanos
    plt.figure(figsize=(10, 6))
    plt.scatter(exoplanetas_cercanos['st_teff'], exoplanetas_cercanos['pl_rade'], alpha=0.6)
    plt.title('Temperatura Efectiva de la Estrella vs. Radio del Planeta')
    plt.xlabel('Temperatura Efectiva de la Estrella (K)')
    plt.ylabel('Radio del Planeta (Radio de la Tierra)')
    plt.grid(True)
    plt.xlim(4000, 7000)
    plt.ylim(0, 3)
    plt.axhline(y=1, color='r', linestyle='--', label='Radio de la Tierra')
    plt.legend()

    # Convertir el gráfico a imagen base64
    img2 = BytesIO()
    plt.savefig(img2, format='png')
    img2.seek(0)
    plot_url2 = base64.b64encode(img2.getvalue()).decode()

    # Pasar los gráficos al template
    return render_template('index.html', plot_url1=plot_url1, plot_url2=plot_url2, exoplanetas=exoplanetas_cercanos)

if __name__ == '__main__':
    app.run(debug=True)

