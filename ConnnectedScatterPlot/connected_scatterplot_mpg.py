import pandas as pd
import seaborn as sns
import plotly.express as px
import os

def main():
    # Carrego el dataset "mpg" de Seaborn
    df = sns.load_dataset("mpg").dropna(subset=["mpg", "model_year", "manufacturer"])

    # Com puc tenir més claredat, agrupo per any i marca
    df_grouped = df.groupby(["model_year", "manufacturer"])["mpg"].mean().reset_index()

    # Creo el Connected Scatterplot
    fig = px.scatter(
        df_grouped,
        x="model_year",
        y="mpg",
        color="manufacturer",
        text="mpg",
        title="Evolució del consum de combustible per marca",
        labels={
            "model_year": "Any del model",
            "mpg": "Consum mitjà (mpg)",
            "manufacturer": "Marca"
        }
    )

    # Connecto els punts amb línia
    fig.update_traces(mode="lines+markers+text", textposition="top center")

    # Guardo el gràfic com a fitxer HTML
    output_file = os.path.join(os.getcwd(), "connected_scatterplot_mpg.html")
    fig.write_html(output_file)

    print(f"He creat el Connected Scatterplot i l'he guardat com a: {output_file}")

if __name__ == "__main__":
    main()

