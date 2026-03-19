"""
analisis.py — Funciones reutilizables de análisis para el dataset Titanic
Proyecto Final Python — Enfoque: Puerto de Embarque y Tarifas
"""

from __future__ import annotations
import pandas as pd
import matplotlib.pyplot as plt


def show_missing(df: pd.DataFrame) -> pd.DataFrame:
    """
    Retorna tabla de nulos con conteo y porcentaje por columna.

    Args:
        df: DataFrame a inspeccionar.

    Returns:
        DataFrame con columnas: nulos, pct_nulos, dtype.
    """
    out = pd.DataFrame({
        "nulos": df.isna().sum(),
        "pct_nulos": (df.isna().mean() * 100).round(2),
        "dtype": df.dtypes.astype(str),
    }).sort_values("pct_nulos", ascending=False)
    return out[out["nulos"] > 0]


def survival_rate(df: pd.DataFrame) -> float:
    """
    Calcula la tasa de supervivencia global.

    Args:
        df: DataFrame con columna 'Survived'.

    Returns:
        Tasa de supervivencia como float entre 0 y 1.
    """
    if "Survived" not in df.columns:
        raise ValueError("❌ Falta la columna 'Survived'.")
    return float(df["Survived"].mean())


def survival_by(df: pd.DataFrame, col: str) -> pd.DataFrame:
    """
    Calcula tasa de supervivencia agrupada por una columna.

    Args:
        df: DataFrame limpio con columna 'Survived'.
        col: Nombre de la columna para agrupar.

    Returns:
        DataFrame con tasa_supervivencia y conteo n por grupo.
    """
    if col not in df.columns:
        raise ValueError(f"❌ No existe la columna: '{col}'.")
    out = (
        df.groupby(col, dropna=False)
          .agg(
              tasa_supervivencia=("Survived", "mean"),
              n=("Survived", "size")
          )
          .sort_values("tasa_supervivencia", ascending=False)
    )
    out["tasa_supervivencia"] = (out["tasa_supervivencia"] * 100).round(2)
    return out


def tabla_nulos_consola(df: pd.DataFrame) -> None:
    """
    Imprime en consola una tabla de nulos formateada.

    Args:
        df: DataFrame a inspeccionar.
    """
    missing = show_missing(df)
    if missing.empty:
        print("✅ No hay valores nulos en el dataset.")
        return
    print("\n" + "═" * 45)
    print("   📋 TABLA DE NULOS")
    print("═" * 45)
    print(f"{'Columna':<20} {'Nulos':>8} {'Porcentaje':>12}")
    print("─" * 45)
    for col, row in missing.iterrows():
        print(f"{col:<20} {int(row['nulos']):>8} {row['pct_nulos']:>11.2f}%")
    print("═" * 45)


def grafico_supervivencia_sexo(df: pd.DataFrame) -> None:
    """
    Gráfico de barras: tasa de supervivencia por sexo.

    Args:
        df: DataFrame limpio con columnas 'Sex' y 'Survived'.
    """
    datos = df.groupby("Sex")["Survived"].mean() * 100
    plt.figure(figsize=(6, 4))
    bars = plt.bar(datos.index, datos.values, color=["#ff69b4", "#1f77b4"])
    plt.title("Tasa de Supervivencia por Sexo", fontsize=13, fontweight="bold")
    plt.ylabel("Tasa de Supervivencia (%)")
    plt.ylim(0, 100)
    for bar, val in zip(bars, datos.values):
        plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 1,
                 f"{val:.1f}%", ha="center", fontsize=11)
    plt.tight_layout()
    plt.show()


def grafico_supervivencia_clase(df: pd.DataFrame) -> None:
    """
    Gráfico de barras: tasa de supervivencia por clase.

    Args:
        df: DataFrame limpio con columnas 'Pclass' y 'Survived'.
    """
    datos = df.groupby("Pclass")["Survived"].mean() * 100
    plt.figure(figsize=(6, 4))
    bars = plt.bar(datos.index.astype(str), datos.values,
                   color=["#4CAF50", "#FF9800", "#F44336"])
    plt.title("Tasa de Supervivencia por Clase", fontsize=13, fontweight="bold")
    plt.ylabel("Tasa de Supervivencia (%)")
    plt.xlabel("Clase (1 = Primera, 3 = Tercera)")
    plt.ylim(0, 100)
    for bar, val in zip(bars, datos.values):
        plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 1,
                 f"{val:.1f}%", ha="center", fontsize=11)
    plt.tight_layout()
    plt.show()
