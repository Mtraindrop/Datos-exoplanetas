import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Usar un backend que no dependa de una GUI
import matplotlib.pyplot as plt
import base64
from io import BytesIO

def main():
    archivo_csv = 'exoplaneta.csv'  # Asegúrate de que este archivo esté en la misma carpeta que este script
    datos = pd.read_csv(archivo_csv, comment='#', on_bad_lines='skip')

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

    plt.subplot(2, 1, 2)
    for planeta in exoplanetas_habitables['pl_name']:
        datos_planeta = exoplanetas_habitables[exoplanetas_habitables['pl_name'] == planeta]
        if not datos_planeta.empty:
            plt.plot(datos_planeta['releasedate'], datos_planeta['pl_orbper'], marker='o', label=planeta)
    plt.title('Evolución del Período Orbital de los Exoplanetas Habitables')
    plt.xlabel('Fecha de Publicación/Actualización')
    plt.ylabel('Período Orbital [días]')
    plt.legend()
    plt.grid(True)

    plt.tight_layout()
    plt.savefig('grafico1.png')  # Guardar el gráfico como imagen
    plt.close()

    # Gráfico 2: Temperatura Efectiva de la Estrella vs. Radio del Planeta
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
    plt.savefig('grafico2.png')  # Guardar el gráfico como imagen
    plt.close()

    # Gráfico 3: Mapa Estelar de Exoplanetas Cercanos
    datos_filtrados = datos[['ra', 'dec', 'sy_vmag']].dropna()
    tamanio_puntos = 100 / (datos_filtrados['sy_vmag'] + 1)

    plt.figure(figsize=(10, 8))
    plt.scatter(datos_filtrados['ra'], datos_filtrados['dec'], s=tamanio_puntos, c='white', edgecolors='blue')
    plt.gca().invert_xaxis()
    plt.title('Mapa Estelar de Exoplanetas Cercanos')
    plt.xlabel('Ascensión Recta (RA) [grados]')
    plt.ylabel('Declinación (Dec) [grados]')
    plt.grid(True)
    plt.savefig('grafico3.png')  # Guardar el gráfico como imagen
    plt.close()

    # Gráfico 4: Mapa Estelar de Exoplanetas Habitables
    habitables = datos[(datos['pl_rade'] >= 0.5) & (datos['pl_rade'] <= 2)]
    habitables_filtrados = habitables[['ra', 'dec', 'sy_vmag']].dropna()
    tamanio_puntos_habitables = 100 / (habitables_filtrados['sy_vmag'] + 1)

    plt.figure(figsize=(10, 8))
    plt.scatter(habitables_filtrados['ra'], habitables_filtrados['dec'], 
                s=tamanio_puntos_habitables, c='green', edgecolors='black')
    plt.gca().invert_xaxis()
    plt.title('Mapa Estelar de Exoplanetas Habitables')
    plt.xlabel('Ascensión Recta (RA) [grados]')
    plt.ylabel('Declinación (Dec) [grados]')
    plt.grid(True)
    plt.savefig('grafico4.png')  # Guardar el gráfico como imagen
    plt.close()

if __name__ == "__main__":
    main()


