import pandas as pd
import seaborn as sns
import plotly.express as px
import os

def main():
    # Carrego dataset
    df = sns.load_dataset("flights")

    # Agrupo per any
    df_agrupat = df.groupby("year")["passengers"].sum().reset_index()

    # Creo el bar plot
    fig = px.bar(
        df_agrupat,
        x="year",
        y="passengers",
        text="passengers",
        title="Nombre total de passatgers per any (1949-1960)",
        labels={
            "year": "Any",
            "passengers": "Nombre total de passatgers"
        }
    )

    # Mostro els valors sobre les barres
    fig.update_traces(textposition="outside")

    # Guardo com HTML
    fitxer_sortida = os.path.join(os.getcwd(), "timeline_bar_passatgers.html")
    fig.write_html(fitxer_sortida)

    print(f"He creat el timeline amb barres i l'he guardat com a: {fitxer_sortida}")

if __name__ == "__main__":
    main()

