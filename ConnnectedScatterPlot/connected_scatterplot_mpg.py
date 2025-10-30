import pandas as pd
import seaborn as sns
import plotly.express as px
import os

def main():
    # Carrego el dataset "mpg" de Seaborn
    df = sns.load_dataset("mpg").dropna(subset=["mpg", "model_year", "name"])

    # Creo columna 'marca' a partir del nom del cotxe
    df['marca'] = df['name'].apply(lambda x: x.split()[0].lower())

    # Marques seleccionades
    marques_seleccionades = ['audi', 'bmw', 'peugeot', 'volkswagen', 'opel', 'mercedes-benz']

    # Filtra només aquestes marques
    df_filtrat = df[df['marca'].isin(marques_seleccionades)]

    # Agrupo per any i marca per calcular el consum mitjà
    df_agrupat = df_filtrat.groupby(["model_year", "marca"])["mpg"].mean().reset_index()

    # Arrodonim el consum a 2 decimals
    df_agrupat["mpg"] = df_agrupat["mpg"].round(2)

    # Creo el Connected Scatterplot
    fig = px.scatter(
        df_agrupat,
        x="model_year",
        y="mpg",
        color="marca",
        text="mpg",
        title="Consum mitjà de combustible per marques seleccionades",
        labels={
            "model_year": "Any del model",
            "mpg": "Consum mitjà (mpg)",
            "marca": "Marca"
        }
    )

    # Connecto els punts amb línia i mostro els valors
    fig.update_traces(mode="lines+markers+text", textposition="top center")

    # Guardo el gràfic com a fitxer HTML
    fitxer_sortida = os.path.join(os.getcwd(), "connected_scatterplot_marques.html")
    fig.write_html(fitxer_sortida)

    print(f"He creat el Connected Scatterplot i l'he guardat com a: {fitxer_sortida}")

if __name__ == "__main__":
    main()

