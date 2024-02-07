Proyecto1-Henry
Procesamiento y Análisis de Datos de Juegos en Steam
Este proyecto se centra en el procesamiento, análisis y recomendación de juegos de Steam utilizando diversas bibliotecas de Python y FastAPI para la creación de endpoints API.

Importación de Módulos
En esta sección, importamos todas las librerías necesarias para nuestras tareas de procesamiento y análisis de datos. Esto incluye librerías para manejar estructuras de datos (pandas, numpy), visualización (matplotlib, seaborn), trabajo con archivos JSON y comprimidos (json, gzip), y procesamiento de texto (nltk, re).

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import json
import gzip
import ast
import re
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
from fastapi import FastAPI
import pyarrow


Descarga de Palabras Comunes (Stopwords)

# nltk.download('vader_lexicon')
# nltk.download('stopwords')
# nltk.download('punkt')


Optimización de Tipos de Datos en DataFrames
La función optimize_dataframe_types optimiza los tipos de datos en un DataFrame de pandas para reducir el uso de memoria.


Importación de Datasets

Dataset de Juegos

Aquí, cargamos y preprocesamos el dataset que contiene información sobre varios juegos. Esto involucra la lectura de un archivo .gz comprimido, decodificación de objetos JSON y limpieza de datos eliminando filas que estén completamente nulas.


file_path_games = r"PI MLOps - STEAM\steam_games.json.gz"
# Eliminación de Columnas Innecesarias
# Conversión y Limpieza de Datos
# Análisis de Sentimientos con NLTK
# FastAPI para Análisis y Recomendaciones


Endpoints Implementados

Implementamos varios endpoints utilizando FastAPI para realizar análisis específicos y proporcionar recomendaciones de juegos basadas en géneros, desarrolladores, y análisis de sentimientos de reseñas.

/developer/{desarrollador}: Calcula estadísticas de un desarrollador específico.

/userdata/{user_id}: Proporciona datos agregados sobre los juegos de un usuario específico.

/user_for_genre/{genre}: Encuentra el usuario con más horas jugadas para un género específico.

/best_developer_year/{year}: Determina el mejor desarrollador para un año específico basado en reseñas positivas.

/developer_reviews_analysis/{developer}: Realiza un análisis de las reseñas de los juegos de un desarrollador específico.

/recommendations/{game_id}: Recomienda juegos basados en géneros similares al juego de entrada.


Recomendaciones Incorporadas

Las recomendaciones para el endpoint /recommendations/{game_id} se han incorporado en la función correspondiente. Esta función devuelve una lista de juegos similares al juego especificado por game_id, basado en los géneros de los juegos. Cada recomendación se realiza utilizando la similitud de coseno entre los géneros del juego de entrada y los demás juegos en el dataset.