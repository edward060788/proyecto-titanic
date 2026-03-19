"""
main.py — Punto de entrada del Analizador Titanic
Proyecto Final Python — Enfoque: Puerto de Embarque y Tarifas

Uso:
    python main.py
"""

from pathlib import Path
from clases import TitanicAnalyzer
from analisis import (
    tabla_nulos_consola,
    survival_by,
    grafico_supervivencia_sexo,
    grafico_supervivencia_clase,
)

# ── Ruta del dataset ──────────────────────────────────────
DATA_PATH = Path("data/Titanic-Dataset.csv")
OUTPUT_DIR = Path("outputs")


def mostrar_menu() -> None:
    print("\n" + "═" * 45)
    print("     🚢  ANALIZADOR TITANIC — MENÚ PRINCIPAL")
    print("═" * 45)
    print("  1. Cargar dataset")
    print("  2. Limpiar datos")
    print("  3. Ver resumen general")
    print("  4. Supervivencia por puerto de embarque")
    print("  5. Supervivencia por nivel de tarifa")
    print("  6. Supervivencia por sexo (gráfico)")
    print("  7. Supervivencia por clase (gráfico)")
    print("  8. Buscar pasajero por nombre")
    print("  9. Exportar reporte (CSV + TXT)")
    print("  0. Salir")
    print("═" * 45)


def main() -> None:
    analyzer = TitanicAnalyzer()

    print("\n🚢  Bienvenido al Analizador del Titanic")
    print("   Enfoque: Puerto de Embarque y Tarifas\n")

    while True:
        mostrar_menu()

        try:
            opcion = input("  Selecciona una opción: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\n\n👋 Hasta luego.")
            break

        if opcion == "1":
            # ── Cargar dataset ─────────────────────────
            try:
                analyzer.cargar_datos(DATA_PATH)
                tabla_nulos_consola(analyzer.df)
            except FileNotFoundError as e:
                print(e)
            except ValueError as e:
                print(e)

        elif opcion == "2":
            # ── Limpiar datos ──────────────────────────
            try:
                analyzer.limpiar_datos()
            except RuntimeError as e:
                print(e)

        elif opcion == "3":
            # ── Resumen general ────────────────────────
            try:
                analyzer.resumen_general()
            except RuntimeError as e:
                print(e)

        elif opcion == "4":
            # ── Supervivencia por puerto ───────────────
            try:
                analyzer.supervivencia_por_puerto()
                analyzer.graficar_puerto()
            except RuntimeError as e:
                print(e)

        elif opcion == "5":
            # ── Supervivencia por tarifa ───────────────
            try:
                analyzer.supervivencia_por_tarifa()
                analyzer.graficar_tarifa()
            except RuntimeError as e:
                print(e)

        elif opcion == "6":
            # ── Gráfico por sexo ───────────────────────
            try:
                analyzer._check_clean()
                grafico_supervivencia_sexo(analyzer.df_clean)
            except RuntimeError as e:
                print(e)

        elif opcion == "7":
            # ── Gráfico por clase ──────────────────────
            try:
                analyzer._check_clean()
                grafico_supervivencia_clase(analyzer.df_clean)
            except RuntimeError as e:
                print(e)

        elif opcion == "8":
            # ── Buscar pasajero ────────────────────────
            try:
                nombre = input("  Ingresa el nombre a buscar: ").strip()
                analyzer.buscar_pasajero(nombre)
            except RuntimeError as e:
                print(e)

        elif opcion == "9":
            # ── Exportar reporte ───────────────────────
            try:
                analyzer.exportar_reporte(OUTPUT_DIR)
            except RuntimeError as e:
                print(e)

        elif opcion == "0":
            print("\n👋 ¡Hasta luego! Gracias por usar el Analizador Titanic.\n")
            break

        else:
            print("⚠️  Opción inválida. Por favor elige entre 0 y 9.")

        input("\n  Presiona Enter para continuar...")


if __name__ == "__main__":
    main()
