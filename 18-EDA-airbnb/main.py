"""Airbnb Copenhagen Data Processing & EDA Pipeline."""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px
import seaborn as sns


def load_raw_data(filepath: Path) -> pd.DataFrame:
    """Загрузка исходного архива gzip."""
    if not filepath.exists():
        raise FileNotFoundError(f"Файл {filepath} не найден!")
    print(f"-> Загрузка данных из {filepath}...")
    return pd.read_csv(filepath, compression="gzip")


def clean_airbnb_data(df: pd.DataFrame) -> pd.DataFrame:
    """Пайплайн очистки, фильтрации фичей и импутации пропусков."""
    print("-> Очистка и предобработка данных...")
    columns_to_keep = [
        "id",
        "name",
        "room_type",
        "neighbourhood_cleansed",
        "latitude",
        "longitude",
        "accommodates",
        "bedrooms",
        "beds",
        "bathrooms_text",
        "price",
        "minimum_nights",
        "host_is_superhost",
        "number_of_reviews",
        "reviews_per_month",
    ]
    df_clean = df[columns_to_keep].copy()

    # Парсинг числовых и строковых полей
    df_clean["price"] = (
        df_clean["price"]
        .astype(str)
        .str.replace(r"[\$,]", "", regex=True)
        .astype(float)
    )
    df_clean["bathrooms"] = (
        df_clean["bathrooms_text"]
        .astype(str)
        .str.extract(r"(\d+\.?\d*)")[0]
        .astype(float)
    )
    df_clean = df_clean.drop(columns=["bathrooms_text"])

    # Обработка пропусков (Imputation)
    df_clean = df_clean.dropna(subset=["price"]).copy()
    df_clean["reviews_per_month"] = df_clean["reviews_per_month"].fillna(0.0)
    df_clean["bedrooms"] = df_clean["bedrooms"].fillna(1.0)
    df_clean["beds"] = df_clean["beds"].fillna(df_clean["accommodates"])
    df_clean["bathrooms"] = df_clean["bathrooms"].fillna(df_clean["bathrooms"].median())
    df_clean["host_is_superhost"] = (
        df_clean["host_is_superhost"].map({"t": True, "f": False}).fillna(False)
    )

    return df_clean


def generate_figures(df: pd.DataFrame, output_dir: Path) -> None:
    """Генерация и сохранение всех визуализаций в папку figures."""
    output_dir.mkdir(parents=True, exist_ok=True)
    sns.set_theme(style="whitegrid")

    p99 = df["price"].quantile(0.99)
    df_viz = df[df["price"] <= p99].copy()

    # 1. Распределение цен
    print("-> Генерация price_distribution.png...")
    fig, (ax_box, ax_hist) = plt.subplots(
        2, 1, figsize=(10, 6), sharex=True, gridspec_kw={"height_ratios": [0.3, 0.7]}
    )
    sns.boxplot(data=df_viz, x="price", ax=ax_box, color="lightcoral")
    sns.histplot(
        data=df_viz, x="price", kde=True, ax=ax_hist, color="steelblue", bins=40
    )
    fig.tight_layout()
    fig.savefig(output_dir / "price_distribution.png", dpi=300, bbox_inches="tight")
    plt.close(fig)

    # 2. Матрица корреляций
    print("-> Генерация correlation_matrix.png...")
    num_cols = [
        "price",
        "accommodates",
        "bedrooms",
        "beds",
        "bathrooms",
        "number_of_reviews",
    ]
    corr = df[num_cols].corr(method="spearman")
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", vmin=-1, vmax=1, ax=ax)
    fig.tight_layout()
    fig.savefig(output_dir / "correlation_matrix.png", dpi=300, bbox_inches="tight")
    plt.close(fig)

    # 3. Инсайты 1 и 2
    print("-> Генерация insights_1_2.png...")
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
    sns.boxplot(
        data=df_viz,
        x="room_type",
        y="price",
        hue="room_type",
        palette="Set2",
        legend=False,
        ax=ax1,
    )
    top_n = (
        df_viz.groupby("neighbourhood_cleansed")["price"]
        .median()
        .sort_values(ascending=False)
    )
    sns.barplot(
        x=top_n.values,
        y=top_n.index,
        hue=top_n.index,
        palette="viridis",
        legend=False,
        ax=ax2,
    )
    fig.tight_layout()
    fig.savefig(output_dir / "insights_1_2.png", dpi=300, bbox_inches="tight")
    plt.close(fig)

    # 4. Инсайты 3 и 4
    print("-> Генерация insights_3_4.png...")
    df_viz["host_type"] = df_viz["host_is_superhost"].map(
        {False: "Обычный хост", True: "Superhost"}
    )
    fig, (ax3, ax4) = plt.subplots(1, 2, figsize=(16, 6))
    sns.boxplot(
        data=df_viz,
        x="host_type",
        y="price",
        hue="host_type",
        order=["Обычный хост", "Superhost"],
        palette="pastel",
        legend=False,
        ax=ax3,
    )
    sns.lineplot(
        data=df_viz[df_viz["accommodates"] <= 8],
        x="accommodates",
        y="price",
        hue="room_type",
        marker="o",
        errorbar=None,
        ax=ax4,
    )
    fig.tight_layout()
    fig.savefig(output_dir / "insights_3_4.png", dpi=300, bbox_inches="tight")
    plt.close(fig)

    # 5. Карта Plotly (современный синтаксис Plotly 5.24+)
    print("-> Генерация copenhagen_map.html...")
    fig_map = px.scatter_map(
        df_viz.sample(min(3000, len(df_viz)), random_state=42),
        lat="latitude",
        lon="longitude",
        color="price",
        size="accommodates",
        color_continuous_scale="Viridis",
        range_color=[df_viz["price"].min(), p99],
        hover_name="name",
        hover_data=["neighbourhood_cleansed", "room_type", "price"],
        zoom=10.5,
        title="Географическая карта цен аренды в Копенгагене",
        map_style="carto-positron",
    )
    fig_map.write_html(output_dir / "copenhagen_map.html")


def main() -> None:
    base_dir = Path(__file__).resolve().parent
    raw_data_path = base_dir / "data" / "raw" / "listings.csv.gz"
    figures_dir = base_dir / "figures"

    df_raw = load_raw_data(raw_data_path)
    df_clean = clean_airbnb_data(df_raw)
    generate_figures(df_clean, figures_dir)
    print("\n Пайплайн успешно выполнен! Все графики обновлены в папке figures/.")


if __name__ == "__main__":
    main()
