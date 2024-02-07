from fastapi import FastAPI, HTTPException
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import StandardScaler
import pyarrow




app = FastAPI()


# Datasets uploading
#df_ga = pd.read_parquet("./datasets/steam_games_cleaned.parquet")
#df_re = pd.read_parquet("./datasets/steam_reviews_cleaned.parquet")
#df_it = pd.read_parquet("./datasets/steam_items_cleaned.parquet")

@app.get('/developer/{desarrollador}')
async def calculate_developer_stats(developer_name):
    # Filtrar el DataFrame por el desarrollador específico
    developer_games = df_ga[df_ga['developer'] == developer_name]

    # Agrupar por año
    yearly_data = developer_games.groupby('release_date').agg(
        cantidad_items=('id', 'count'),
        contenido_free=('price', lambda x: (x == 0.00).sum())
    ).reset_index()

    # Calcular el porcentaje de contenido gratuito
    yearly_data['porcentaje_contenido_free'] = (
        yearly_data['contenido_free'] / yearly_data['cantidad_items']
    ) * 100

    # Renombrar las columnas para coincidir con la salida deseada
    yearly_data = yearly_data.rename(columns={
        'release_date': 'Año',
        'cantidad_items': 'Cantidad de Items',
        'porcentaje_contenido_free': 'Contenido Free'
    })

    # Formatear la columna de porcentaje a un string con 2 decimales seguido de un signo de porcentaje
    yearly_data['Contenido Free'] = yearly_data['Contenido Free'].apply(lambda x: f"{x:.2f}%")

    # Ordenar los resultados por año
    yearly_data = yearly_data.sort_values('Año', ascending=False)

    # Convertir el DataFrame en una lista de diccionarios para el retorno
    result = yearly_data[['Año', 'Cantidad de Items', 'Contenido Free']].to_dict(orient='records')
    
    return result

@app.get("/userdata/{user_id}")
async def userdata(user_id: str):
    # Filtrar items por user_id
    user_items = df_it[df_it['user_id'] == user_id]
    
    # Unir df_it con df_ga para obtener los precios de los juegos que el usuario posee
    user_games_prices = user_items.merge(df_ga, left_on='item_id', right_on='id')
    
    # Calcular el total gastado
    total_spent = user_games_prices['price'].sum()
    
    # Unir df_it con df_re para obtener las recomendaciones de los juegos que el usuario posee
    user_games_reviews = user_items.merge(df_re, left_on='item_id', right_on='item_id')
    
    # Calcular el porcentaje de recomendación como la cantidad de True sobre el total
    total_reviews = len(user_games_reviews)
    if total_reviews > 0:
        recommend_count = user_games_reviews['recommend'].sum()
        recommend_percentage = (recommend_count / total_reviews) * 100
    else:
        recommend_percentage = 0  # Si no hay reviews, el porcentaje es 0
    
    # Contar la cantidad de items
    number_of_items = len(user_items)
    
    # Preparar y devolver el resultado
    result = {
        "Usuario X": user_id,
        "Dinero gastado": f"{total_spent:.2f} USD",
        "% de recomendación": f"{recommend_percentage:.2f}%",
        "cantidad de items": number_of_items
    }
    
    return result




# Assuming df_ga and df_it are already defined and properly loaded

@app.get("/user_for_genre/{genre}")
async def user_for_genre(genre: str):
    # Verify if the genre column exists
    genre_column = f'genre_{genre}'
    if genre_column not in df_ga.columns:
        return {"error": f"Genre '{genre}' not found."}

    # Filter games by genre
    genre_games = df_ga[df_ga[genre_column] == 1]

    # Merge df_it with df_ga to get playtime and release data for games of the specified genre
    genre_user_playtime = df_it.merge(genre_games, left_on='item_id', right_on='id')

    # Find the user with the most playtime for the given genre
    top_user_df = genre_user_playtime.groupby('user_id')['playtime_forever'].sum().reset_index()
    if top_user_df.empty:
        return {"error": f"No user data found for genre '{genre}'."}
    top_user = top_user_df.loc[top_user_df['playtime_forever'].idxmax()]

    # Group playtime by release date as a string
    playtime_by_year = (
        genre_user_playtime.groupby('release_date')['playtime_forever']
        .sum()
        .reset_index()
    )
    
    # Sort the results by 'Hours' in descending order
    playtime_by_year_list = playtime_by_year.rename(columns={'release_date': 'Year', 'playtime_forever': 'Hours'})
    playtime_by_year_list = playtime_by_year_list.sort_values(by='Hours', ascending=False)
    
    # Convert sorted DataFrame to a list of dictionaries
    playtime_by_year_list = playtime_by_year_list.to_dict(orient='records')

    # Prepare and return the result
    result = {
        f"User with the most hours played for Genre {genre}": top_user['user_id'],
        "Hours Played": playtime_by_year_list
    }

    return result


@app.get("/best_developer_year/{year}")
async def best_developer_year(year: str):
    # Filter reviews for recommended and positive sentiment
    positive_reviews = df_re[(df_re['recommend'] == True) & (df_re['sentiment_analysis'] == 2)]
    
    # Filter games released in the given year
    games_in_year = df_ga[df_ga['release_date'] == year]
    
    # Merge the data on game ID
    merged_data = positive_reviews.merge(games_in_year, left_on='item_id', right_on='id')
    
    # Group by developer and count positive recommendations
    developer_recommendations = merged_data.groupby('developer').size().reset_index(name='positive_recommendations')
    
    # Sort and get the top 3 developers
    top_developers = developer_recommendations.sort_values('positive_recommendations', ascending=False).head(3)
    
    # Convert to list of dictionaries for output
    result = top_developers.to_dict(orient='records')
    
    return result


@app.get("/developer_reviews_analysis/{developer}")
async def developer_reviews_analysis(developer: str):
    # Filter games by the developer
    developer_games = df_ga[df_ga['developer'] == developer]
    
    # Merge the developer's games with their reviews
    developer_reviews = pd.merge(developer_games, df_re, left_on='id', right_on='item_id')
    
    # Count positive and negative reviews
    positive_reviews = len(developer_reviews[developer_reviews['sentiment_analysis'] == 2])
    negative_reviews = len(developer_reviews[developer_reviews['sentiment_analysis'] == 0])
    
    # Create and return the result dictionary
    result = {developer: {'Negative': negative_reviews, 'Positive': positive_reviews}}
    
    return result




# Selecting genre and spec columns for the feature matrix
features = [col for col in df_ga.columns if 'genre_' in col or 'spec_' in col]

# Creating the feature matrix with genres and specifications
X = df_ga[features].fillna(0)

# Calculating the cosine similarity matrix
cosine_sim = cosine_similarity(X)

@app.get("/recommendations/{game_id}")
async def get_recommendations(game_id: str, num_recommendations: int = 5):
    
    # Check if the game_id exists in the DataFrame
    idx_list = df_ga.index[df_ga['id'] == game_id].tolist()
    if not idx_list:
        # If the game_id is not found, return an HTTP error response
        raise HTTPException(status_code=404, detail=f"Game ID {game_id} not found in the dataset.")
    
    # If the game_id is found, proceed with fetching the recommendations
    idx = idx_list[0]
    sim_scores = list(enumerate(cosine_sim[idx]))

    # Excluir el juego de entrada de las recomendaciones
    sim_scores = [sim_score for sim_score in sim_scores if sim_score[0] != idx]

    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[:num_recommendations] # Obtener los top N recomendaciones
    game_indices = [i[0] for i in sim_scores]
    
    # Fetching the game details based on the indices
    recommended_games = df_ga.iloc[game_indices][['id', 'app_name']]
    
    # Convert the DataFrame to a dictionary for JSON response
    return recommended_games.to_dict(orient='records')
    