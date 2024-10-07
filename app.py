from flask import Flask, render_template
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Usar un backend que no dependa de una GUI
import matplotlib.pyplot as plt
import base64
from io import BytesIO

app = Flask(__name__)

@app.route('/')
def home():
    archivo_csv = 'exoplaneta.csv'  # Asegúrate de que el archivo esté en la ubicación correcta
    datos = pd.read_csv(archivo_csv, comment='#', on_bad_lines='skip')

    # Imprimir los datos para verificar que se están cargando
    print(datos.head())  # Esto imprimirá las primeras filas del DataFrame en la consola

    # Limpieza de nombres de columnas
    datos.columns = datos.columns.str.strip()

    # Filtrado de estrellas tipo solar
    estrellas_tipo_solar = datos[(datos['st_teff'] >= 5000) & (datos['st_teff'] <= 6000) & 
                                  (datos['st_rad'] >= 0.7) & (datos['st_rad'] <= 1.5)]
    
    # Filtrado de exoplanetas habitables
    exoplanetas_habitables = estrellas_tipo_solar[(estrellas_tipo_solar['pl_rade'] >= 0.5) & 
                                                  (estrellas_tipo_solar['pl_rade'] <= 2.5)]

    # Gráfico 1: Evolución del Radio Planetario
    plt.figure(figsize=(14, 8))
    plt.subplot(2, 1, 1)
    for planeta in exoplanetas_habitables['pl_name']:
        datos_planeta = exoplanetas_habitables[exoplanetas_habitables['pl_name'] == planeta]
        if not datos_planeta.empty:
            plt.plot(datos_planeta['releasedate'], datos_planeta['pl_rade'], marker='o', label=planeta)
    plt.title('Evolución del Radio Planetario de los Exoplanetas Habitables')
    plt.xlabel('Fecha de Publicación/Actualización')
    plt.ylabel('Radio Planetario [Radio de la Tierra]')
    plt.legend()
    plt.grid(True)

    # Gráfico 2: Temperatura Efectiva de la Estrella vs. Radio del Planeta
    plt.subplot(2, 1, 2)
    plt.scatter(exoplanetas_habitables['st_teff'], exoplanetas_habitables['pl_rade'], alpha=0.6)
    plt.title('Temperatura Efectiva de la Estrella vs. Radio del Planeta')
    plt.xlabel('Temperatura Efectiva de la Estrella (K)')
    plt.ylabel('Radio del Planeta (Radio de la Tierra)')
    plt.grid(True)
    plt.xlim(4000, 7000)
    plt.ylim(0, 3)
    plt.axhline(y=1, color='r', linestyle='--', label='Radio de la Tierra')
    plt.legend()

    plt.tight_layout()

    # Convertir el gráfico a imagen base64
    img1 = BytesIO()
    plt.savefig(img1, format='png')
    img1.seek(0)
    plot_url1 = base64.b64encode(img1.getvalue()).decode()
    print("Gráfico 1 generado")  # Verifica que se generó correctamente

    # Aquí puedes agregar el código para generar otros gráficos y convertirlos a base64

    # Pasar los gráficos y exoplanetas habitables al template
    return render_template('index.html', plot_url1=plot_url1, exoplanetas=exoplanetas_habitables)

if __name__ == '__main__':
    app.run(debug=True)



