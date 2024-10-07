@app.route('/')
def home():
    archivo_csv = 'exoplaneta.csv'
    datos = pd.read_csv(archivo_csv)

    # Filtrar exoplanetas habitables
    exoplanetas_habitables = datos[(datos['pl_rade'] >= 0.5) & (datos['pl_rade'] <= 2.5)]

    # Gráfico simple
    plt.figure(figsize=(10, 6))
    plt.scatter(exoplanetas_habitables['st_teff'], exoplanetas_habitables['pl_rade'], alpha=0.6)
    plt.title('Temperatura Efectiva vs Radio Planetario')
    plt.xlabel('Temperatura Efectiva (K)')
    plt.ylabel('Radio Planetario (Radio de la Tierra)')
    
    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()

    return render_template('index.html', plot_url=plot_url)




