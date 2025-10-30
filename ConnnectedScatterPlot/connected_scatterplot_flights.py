import pandas as pd
import seaborn as sns
import plotly.express as px
import os

def main():
    # Carrego el dataset "flights"
    df = sns.load_dataset("flights")

    # Ordeno els mesos perquè estiguin en ordre cronològic
    mesos_ordenats = [
        "Jan", "Feb", "Mar", "Apr", "May", "Jun", 
        "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
    ]
    df['month'] = pd.Categorical(df['month'], categories=mesos_ordenats, ordered=True)

    # Creo el Connected Scatterplot
    fig = px.scatter(
        df,
        x="year",
        y="passengers",
        color="month",
        text="passengers",
        title="Nombre de passatgers per mes i any (1949-1960)",
        labels={
            "year": "Any",
            "passengers": "Nombre de passatgers",
            "month": "Mes"
        }
    )

    # Connecto els punts amb línia i mostro els valors
    fig.update_traces(mode="lines+markers+text", textposition="top center")

    # Guardo el gràfic com a fitxer HTML
    fitxer_sortida = os.path.join(os.getcwd(), "connected_scatterplot_flights.html")
    fig.write_html(fitxer_sortida)

    print(f"He creat el Connected Scatterplot i l'he guardat com a: {fitxer_sortida}")

if __name__ == "__main__":
    main()

