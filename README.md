
![wp9013291-status-logo-wallpapers](https://github.com/fcuerdo/Project1-Henry/assets/33520476/9d66c3fb-2544-4002-a2c5-1bbeec270cea)


# Steam Insight Engine


### En un mundo digital en constante evolución, "Steam Data Analysis y API" surge como una iniciativa clave para desentrañar y mejorar la interacción de los usuarios en Steam, una plataforma líder en la distribución de videojuegos. Este proyecto se centra en analizar y proporcionar una comprensión accesible de los datos de Steam, ofreciendo análisis de reseñas, recomendaciones de juegos y estadísticas de desarrolladores para enriquecer la experiencia de los usuarios.

## ¿Por Qué Steam?

Elegimos Steam por su rica base de datos y su comunidad diversa, lo que permite extraer insights valiosos para mejorar la experiencia de jugadores y desarrolladores. Los jugadores se benefician al descubrir juegos que se alinean con sus gustos, mientras que los desarrolladores obtienen información clave para crear juegos más atractivos.

## Problemas que Resuelve

Este proyecto aborda el desafío del descubrimiento de juegos en una biblioteca vasta, ayudando a los usuarios a encontrar juegos que coincidan con sus preferencias y proporcionando a los desarrolladores datos esenciales para optimizar sus creaciones.

## Objetivo

El objetivo principal de este proyecto es proporcionar a los usuarios una manera conveniente de interactuar con datos relacionados con juegos en la plataforma Steam, ofreciendo funcionalidades como análisis de reseñas, recomendaciones de juegos y estadísticas de desarrolladores.

## Endpoints de la API

### GET /developer/{developer_name}

**Descripción:** Obtiene estadísticas para un desarrollador específico.<br>
**Parámetro:** developer_name (nombre del desarrollador).<br>
**Respuesta:** Devuelve un conjunto de estadísticas del desarrollador, incluyendo la cantidad de juegos, contenido gratuito y el porcentaje de contenido gratuito por año. Si el desarrollador no se encuentra, devuelve un error 404.

### GET /userdata/{user_id}

**Descripción:** Recupera datos del usuario, incluyendo el gasto total, el porcentaje de recomendaciones y el número de ítems.<br>
**Parámetro:** user_id (identificador del usuario).<br>
**Respuesta:** Información detallada del usuario. Si el user_id no se encuentra, devuelve un error 404.

### GET /user_for_genre/{genre}

**Descripción:** Encuentra al usuario con más horas jugadas para un género específico.<br>
**Parámetro:** genre (género del juego).<br>
**Respuesta:** Devuelve el usuario con más horas jugadas en ese género, las horas totales jugadas y las horas jugadas por año. Si el género no se encuentra, devuelve un mensaje de error.

### GET /best_developer_year/{year}

**Descripción:** Identifica los mejores desarrolladores en un año específico.<br>
**Parámetro:** year (año de interés).<br>
**Respuesta:** Lista de los mejores desarrolladores y sus recomendaciones positivas en ese año. Si no hay datos para ese año, devuelve un mensaje de error.

### GET /developer_reviews_analysis/{developer}

**Descripción:** Realiza un análisis de las reseñas para un desarrollador específico.<br>
**Parámetro:** developer (nombre del desarrollador).<br>
**Respuesta:** Conteo de reseñas positivas y negativas para el desarrollador. Si el desarrollador no se encuentra, devuelve un mensaje de error.

### GET /recommendations/{game_id}

**Descripción:** Proporciona recomendaciones de juegos basadas en la similitud de géneros.<br>
**Parámetro:** game_id (identificador del juego) y opcionalmente num_recommendations (número de recomendaciones a devolver).<br>
**Respuesta:** Lista de juegos recomendados. Si el juego no se encuentra, devuelve un error 404.


Estos endpoints proporcionan una interfaz rica y versátil para interactuar con los datos de Steam, facilitando el acceso a información valiosa para los desarrolladores y los usuarios de la plataforma.

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

