"""
clases.py — Clase principal del Analizador Titanic
Proyecto Final Python — Enfoque: Puerto de Embarque y Tarifas
"""

from __future__ import annotations
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime


class TitanicAnalyzer:
    """
    Clase principal para cargar, limpiar y analizar el dataset Titanic.
    Enfoque: Supervivencia por Puerto de Embarque y Nivel de Tarifa.
    """

    REQUIRED_COLS = {"Survived", "Pclass", "Sex", "Age", "SibSp", "Parch",
                     "Fare", "Embarked", "Name"}

    PORT_NAMES = {"C": "Cherbourg", "Q": "Queenstown", "S": "Southampton"}

    def __init__(self) -> None:
        self.df: pd.DataFrame | None = None
        self.df_clean: pd.DataFrame | None = None
        self._loaded = False

    # ─────────────────────────────────────────────
    # 1. CARGA
    # ─────────────────────────────────────────────
    def cargar_datos(self, path: str | Path) -> None:
        """Carga el CSV del Titanic y valida columnas requeridas."""
        p = Path(path)
        if not p.exists():
            raise FileNotFoundError(f"❌ No se encontró el archivo: {p}")
        df = pd.read_csv(p)
        faltantes = self.REQUIRED_COLS - set(df.columns)
        if faltantes:
            raise ValueError(f"❌ Faltan columnas: {sorted(faltantes)}")
        self.df = df
        self._loaded = True
        print(f"✅ Dataset cargado correctamente — {df.shape[0]} filas, {df.shape[1]} columnas.")

    # ─────────────────────────────────────────────
    # 2. LIMPIEZA
    # ─────────────────────────────────────────────
    def limpiar_datos(self) -> None:
        """Imputa nulos en Age, Embarked y Fare. Crea variables derivadas."""
        self._check_loaded()
        d = self.df.copy()

        # Imputaciones
        d["Age"] = d["Age"].fillna(d.groupby("Pclass")["Age"].transform("median"))
        d["Embarked"] = d["Embarked"].fillna(d["Embarked"].mode()[0])
        d["Fare"] = d["Fare"].fillna(d["Fare"].median())

        # Variables derivadas
        d["PortName"] = d["Embarked"].map(self.PORT_NAMES)
        d["Fare_Category"] = pd.qcut(d["Fare"], 3, labels=["Bajo", "Medio", "Alto"])
        d["FamilySize"] = d["SibSp"] + d["Parch"] + 1
        d["IsAlone"] = (d["FamilySize"] == 1).astype(int)

        self.df_clean = d
        print("✅ Limpieza completada. Variables derivadas creadas: PortName, Fare_Category, FamilySize, IsAlone.")

    # ─────────────────────────────────────────────
    # 3. ESTADÍSTICAS GENERALES
    # ─────────────────────────────────────────────
    def resumen_general(self) -> None:
        """Muestra KPIs generales del dataset."""
        self._check_clean()
        d = self.df_clean
        total = len(d)
        sobrevivieron = d["Survived"].sum()
        tasa = d["Survived"].mean() * 100

        print("\n" + "═" * 45)
        print("        📊 RESUMEN GENERAL — TITANIC")
        print("═" * 45)
        print(f"  Total de pasajeros   : {total}")
        print(f"  Sobrevivieron        : {sobrevivieron}")
        print(f"  Fallecieron          : {total - sobrevivieron}")
        print(f"  Tasa de supervivencia: {tasa:.2f}%")
        print(f"  Edad promedio        : {d['Age'].mean():.1f} años")
        print(f"  Tarifa promedio      : ${d['Fare'].mean():.2f}")
        print("═" * 45)

    # ─────────────────────────────────────────────
    # 4. ANÁLISIS POR PUERTO
    # ─────────────────────────────────────────────
    def supervivencia_por_puerto(self) -> pd.DataFrame:
        """Retorna tabla de supervivencia por puerto de embarque."""
        self._check_clean()
        d = self.df_clean
        tabla = d.groupby("PortName").agg(
            Total=("Survived", "size"),
            Sobrevivieron=("Survived", "sum"),
            Fallecieron=("Survived", lambda x: (x == 0).sum()),
            Tasa_Supervivencia=("Survived", "mean")
        ).reset_index()
        tabla["Tasa_Supervivencia"] = (tabla["Tasa_Supervivencia"] * 100).round(2)
        tabla = tabla.sort_values("Tasa_Supervivencia", ascending=False)

        print("\n" + "═" * 50)
        print("   ⚓ SUPERVIVENCIA POR PUERTO DE EMBARQUE")
        print("═" * 50)
        print(tabla.to_string(index=False))
        print("═" * 50)
        return tabla

    # ─────────────────────────────────────────────
    # 5. ANÁLISIS POR TARIFA
    # ─────────────────────────────────────────────
    def supervivencia_por_tarifa(self) -> pd.DataFrame:
        """Retorna tabla de supervivencia por nivel de tarifa."""
        self._check_clean()
        d = self.df_clean
        tabla = d.groupby("Fare_Category", observed=True).agg(
            Total=("Survived", "size"),
            Sobrevivieron=("Survived", "sum"),
            Tasa_Supervivencia=("Survived", "mean")
        ).reset_index()
        tabla["Tasa_Supervivencia"] = (tabla["Tasa_Supervivencia"] * 100).round(2)

        print("\n" + "═" * 45)
        print("   💰 SUPERVIVENCIA POR NIVEL DE TARIFA")
        print("═" * 45)
        print(tabla.to_string(index=False))
        print("═" * 45)
        return tabla

    # ─────────────────────────────────────────────
    # 6. BÚSQUEDA DE PASAJERO
    # ─────────────────────────────────────────────
    def buscar_pasajero(self, nombre: str) -> None:
        """Busca pasajeros cuyo nombre contenga el texto ingresado."""
        self._check_clean()
        if not nombre.strip():
            print("⚠️  Por favor ingresa un nombre válido.")
            return
        resultado = self.df_clean[
            self.df_clean["Name"].str.contains(nombre, case=False, na=False)
        ][["Name", "Sex", "Age", "Pclass", "Fare", "Embarked", "Survived"]]

        if resultado.empty:
            print(f"⚠️  No se encontraron pasajeros con '{nombre}'.")
        else:
            print(f"\n🔍 Resultados para '{nombre}':")
            print(resultado.to_string(index=False))

    # ─────────────────────────────────────────────
    # 7. GRÁFICOS
    # ─────────────────────────────────────────────
    def graficar_puerto(self) -> None:
        """Gráfico de barras: supervivencia por puerto."""
        self._check_clean()
        datos = self.df_clean.groupby("PortName")["Survived"].mean() * 100
        plt.figure(figsize=(7, 4))
        bars = plt.bar(datos.index, datos.values, color=["#2196F3", "#4CAF50", "#FF9800"])
        plt.title("Tasa de Supervivencia por Puerto de Embarque", fontsize=13, fontweight="bold")
        plt.ylabel("Tasa de Supervivencia (%)")
        plt.xlabel("Puerto")
        plt.ylim(0, 100)
        for bar, val in zip(bars, datos.values):
            plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 1,
                     f"{val:.1f}%", ha="center", fontsize=11)
        plt.tight_layout()
        plt.show()

    def graficar_tarifa(self) -> None:
        """Gráfico de barras: supervivencia por nivel de tarifa."""
        self._check_clean()
        datos = self.df_clean.groupby("Fare_Category", observed=True)["Survived"].mean() * 100
        plt.figure(figsize=(7, 4))
        bars = plt.bar(datos.index.astype(str), datos.values,
                       color=["#1f77b4", "#ffcc00", "#ff69b4"])
        plt.title("Tasa de Supervivencia por Nivel de Tarifa", fontsize=13, fontweight="bold")
        plt.ylabel("Tasa de Supervivencia (%)")
        plt.xlabel("Nivel Económico")
        plt.ylim(0, 100)
        for bar, val in zip(bars, datos.values):
            plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 1,
                     f"{val:.1f}%", ha="center", fontsize=11)
        plt.tight_layout()
        plt.show()

    # ─────────────────────────────────────────────
    # 8. EXPORTAR REPORTE
    # ─────────────────────────────────────────────
    def exportar_reporte(self, outdir: str | Path = "outputs") -> None:
        """Exporta CSV limpio y reporte TXT con conclusiones."""
        self._check_clean()
        out = Path(outdir)
        out.mkdir(parents=True, exist_ok=True)

        # CSV limpio
        csv_path = out / "titanic_clean.csv"
        self.df_clean.to_csv(csv_path, index=False)

        # Reporte TXT
        d = self.df_clean
        tasa_global = d["Survived"].mean() * 100
        por_puerto = d.groupby("PortName")["Survived"].mean() * 100
        por_tarifa = d.groupby("Fare_Category", observed=True)["Survived"].mean() * 100

        reporte = []
        reporte.append("=" * 50)
        reporte.append("   REPORTE FINAL — ANÁLISIS TITANIC")
        reporte.append(f"   Generado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        reporte.append("=" * 50)
        reporte.append(f"\nTotal de pasajeros   : {len(d)}")
        reporte.append(f"Tasa de supervivencia: {tasa_global:.2f}%")
        reporte.append(f"Edad promedio        : {d['Age'].mean():.1f} años")
        reporte.append(f"Tarifa promedio      : ${d['Fare'].mean():.2f}")
        reporte.append("\n--- Supervivencia por Puerto ---")
        for puerto, tasa in por_puerto.items():
            reporte.append(f"  {puerto:<15}: {tasa:.2f}%")
        reporte.append("\n--- Supervivencia por Nivel de Tarifa ---")
        for nivel, tasa in por_tarifa.items():
            reporte.append(f"  {str(nivel):<10}: {tasa:.2f}%")
        reporte.append("\n--- Conclusiones ---")
        reporte.append("  1. Los pasajeros de Cherbourg tuvieron mayor tasa de supervivencia.")
        reporte.append("  2. A mayor tarifa, mayor probabilidad de sobrevivir.")
        reporte.append("  3. La clase y el puerto están relacionados con el nivel económico.")
        reporte.append("=" * 50)

        txt_path = out / "reporte_titanic.txt"
        txt_path.write_text("\n".join(reporte), encoding="utf-8")

        print(f"\n✅ Reporte exportado:")
        print(f"   📄 CSV  → {csv_path}")
        print(f"   📝 TXT  → {txt_path}")

    # ─────────────────────────────────────────────
    # HELPERS INTERNOS
    # ─────────────────────────────────────────────
    def _check_loaded(self) -> None:
        if not self._loaded or self.df is None:
            raise RuntimeError("⚠️  Primero debes cargar el dataset (opción 1).")

    def _check_clean(self) -> None:
        if self.df_clean is None:
            raise RuntimeError("⚠️  Primero debes limpiar los datos (opción 2).")
