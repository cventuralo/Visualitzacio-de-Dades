import plotly.express as px
import seaborn as sns
import os


def main():
    # Dataset dels pingüins (de seaborn)
    df = sns.load_dataset("penguins").dropna(subset=["species", "body_mass_g"])

    # Boxplot comparant el pes corporal segons l'espècie
    fig = px.box(
        df,
        x="species",
        y="body_mass_g",
        title="Distribució del pes corporal segons l'espècie de pingüí",
        labels={
            "species": "Espècies",
            "body_mass_g": "Pes corporal (gr)"
        }
    )

    # Guardo el gràfic com a fitxer HTML
    output_file = os.path.join(os.getcwd(), "boxplot_plot.html")
    fig.write_html(output_file)

    print(f"He creat el gràfic i l'he guardat com a: {output_file}")


if __name__ == "__main__":
    main()

