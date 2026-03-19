# 🚢 Analizador Titanic — Proyecto Final Python

**Enfoque:** Supervivencia por Puerto de Embarque y Nivel de Tarifa

---

## 📋 Descripción del proyecto

Aplicación de consola en Python que carga, limpia, analiza y genera reportes sobre el dataset del Titanic. El análisis se centra en comprender cómo el **puerto de embarque** y el **nivel de tarifa** influyeron en la supervivencia de los pasajeros.

---

## 🗂️ Estructura del proyecto

```
proyecto_titanic/
├── main.py          # Menú interactivo — punto de entrada
├── clases.py        # Clase TitanicAnalyzer (POO)
├── analisis.py      # Funciones reutilizables de análisis
├── data/
│   └── Titanic-Dataset.csv
├── outputs/         # Archivos generados por el programa
│   ├── titanic_clean.csv
│   └── reporte_titanic.txt
├── README.md
└── requirements.txt
```

---

## ▶️ Instrucciones de ejecución

### 1. Clona el repositorio
```bash
git clone https://github.com/tu-usuario/proyecto-titanic.git
cd proyecto-titanic
```

### 2. Instala las dependencias
```bash
pip install -r requirements.txt
```

### 3. Coloca el dataset
Asegúrate de que `Titanic-Dataset.csv` esté en la carpeta `data/`.

### 4. Ejecuta el programa
```bash
python main.py
```

---

## 🧭 Opciones del menú

| Opción | Descripción |
|--------|-------------|
| 1 | Cargar dataset |
| 2 | Limpiar datos |
| 3 | Ver resumen general |
| 4 | Supervivencia por puerto de embarque |
| 5 | Supervivencia por nivel de tarifa |
| 6 | Gráfico de supervivencia por sexo |
| 7 | Gráfico de supervivencia por clase |
| 8 | Buscar pasajero por nombre |
| 9 | Exportar reporte (CSV + TXT) |
| 0 | Salir |

---

## 🔍 Preguntas que responde el análisis

1. ¿Qué porcentaje total de pasajeros sobrevivió?
2. ¿Influyó el puerto de embarque en la supervivencia?
3. ¿A mayor tarifa, mayor probabilidad de sobrevivir?
4. ¿Sobrevivieron más mujeres que hombres?
5. ¿Influyó la clase del boleto en la tasa de supervivencia?

---

## 🏗️ Componentes técnicos

- **POO:** Clase `TitanicAnalyzer` con métodos para cargar, limpiar, analizar y exportar.
- **Módulos:** Código separado en `main.py`, `clases.py` y `analisis.py`.
- **Funciones:** Todas las tareas divididas en funciones reutilizables con type hints y docstrings.
- **Manejo de errores:** `try/except` en carga de archivo, menú y búsquedas.
- **Visualización:** Gráficos con `matplotlib`.
- **Exportación:** CSV limpio + reporte TXT con conclusiones.

---

## 📚 Lo que aprendí

- Cómo aplicar POO para organizar lógica compleja en una clase coherente.
- La importancia de separar el código en módulos para facilitar el mantenimiento.
- Cómo limpiar e imputar datos reales con pandas.
- Que el puerto de embarque y la tarifa están fuertemente relacionados con la clase social y la supervivencia.

---

## 👤 Autor

**[Edward Ramon Torres Alvarez]**  
Proyecto Final — Curso de Python y Análisis de Datos  
[2026]
