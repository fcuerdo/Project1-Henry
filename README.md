
![wp9013291-status-logo-wallpapers](https://github.com/fcuerdo/Project1-Henry/assets/33520476/9d66c3fb-2544-4002-a2c5-1bbeec270cea)


# Proyecto Steam Data Analysis y API

## Descripción Detallada

En un mundo digital en constante evolución, "Steam Data Analysis y API" surge como una iniciativa clave para desentrañar y mejorar la interacción de los usuarios en Steam, una plataforma líder en la distribución de videojuegos. Este proyecto se centra en analizar y proporcionar una comprensión accesible de los datos de Steam, ofreciendo análisis de reseñas, recomendaciones de juegos y estadísticas de desarrolladores para enriquecer la experiencia de los usuarios.

## ¿Por Qué Steam?

Elegimos Steam por su rica base de datos y su comunidad diversa, lo que permite extraer insights valiosos para mejorar la experiencia de jugadores y desarrolladores. Los jugadores se benefician al descubrir juegos que se alinean con sus gustos, mientras que los desarrolladores obtienen información clave para crear juegos más atractivos.

## Problemas que Resuelve

Este proyecto aborda el desafío del descubrimiento de juegos en una biblioteca vasta, ayudando a los usuarios a encontrar juegos que coincidan con sus preferencias y proporcionando a los desarrolladores datos esenciales para optimizar sus creaciones.

## Objetivo

El objetivo principal de este proyecto es proporcionar a los usuarios una manera conveniente de interactuar con datos relacionados con juegos en la plataforma Steam, ofreciendo funcionalidades como análisis de reseñas, recomendaciones de juegos y estadísticas de desarrolladores.

## Funcionalidades Principales

- **Análisis de Reseñas de Usuarios:** El proyecto incluye funciones para analizar las reseñas de los usuarios, incluyendo el análisis de sentimientos utilizando el analizador VADER.
  
- **Recomendaciones de Juegos:** Se ha implementado un modelo de recomendación basado en similitud de género para recomendar juegos similares a uno dado.

- **Estadísticas de Desarrolladores:** La API proporciona estadísticas detalladas sobre los desarrolladores de juegos, incluyendo el porcentaje de contenido gratuito y el número de juegos lanzados por año.

## Módulos y Bibliotecas Utilizadas

### Python

- **Pandas:** Para manipulación y análisis de datos.
- **NumPy:** Para cálculos numéricos.
- **Matplotlib y Seaborn:** Para visualización de datos.
- **NLTK:** Para procesamiento de texto y análisis de sentimientos.
- **FastAPI:** Para la implementación de la API.
- **PyArrow:** Para el manejo de archivos Parquet.

## Estructura del Proyecto

El proyecto está estructurado en los siguientes componentes principales:

- **data/:** Contiene los conjuntos de datos utilizados en el proyecto.
- **datasets/:** Directorio donde se almacenan los conjuntos de datos procesados y limpios en formato Parquet.
- **api/:** Contiene los archivos relacionados con la implementación de la API utilizando FastAPI.
- **notebooks/:** Jupyter Notebooks utilizados para análisis exploratorio y desarrollo de modelos.
- **README.md:** Este archivo, que proporciona una descripción general del proyecto, sus objetivos y funcionalidades.

## Despliegue

Este proyecto está desplegado en [Render](https://render.com/). Puedes acceder a la API en la siguiente URL: [fcuerdo/](https://fastapi-app-pupd.onrender.com).

## Guía de Uso

1. Clona este repositorio en tu máquina local.
2. Instala las dependencias requeridas utilizando `pip install -r requirements.txt`.
3. Ejecuta la API utilizando el comando `uvicorn api.main:app --reload`.
4. Visita `http://localhost:8000/docs` en tu navegador para ver la documentación interactiva de la API y realizar consultas.

## Contribución

Las contribuciones son bienvenidas. Si deseas contribuir al proyecto, por favor sigue los siguientes pasos:

1. Haz un fork del repositorio.
2. Crea una nueva rama (`git checkout -b feature/feature-name`).
3. Realiza tus cambios y haz commit de ellos (`git commit -am 'Add new feature'`).
4. Haz push de la rama (`git push origin feature/feature-name`).
5. Crea un nuevo Pull Request.

## Autor

- **Facundo Cuerdo**
- GitHub: [fcuerdo](https://github.com/fcuerdo)
- LinkedIn: [fcuerdo](https://www.linkedin.com/in/fcuerdo/)

