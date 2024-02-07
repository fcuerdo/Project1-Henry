from fastapi import FastAPI, HTTPException
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import StandardScaler
import pyarrow
import pyarrow.parquet as pq
from collections import defaultdict



app = FastAPI()


# Datasets uploading
df_ga = pd.read_parquet("./datasets/steam_games_cleaned.parquet")
df_ga_endpoint1 = pd.read_parquet("./datasets/steam_games_endpoint1_cleaned.parquet")
df_re = pd.read_parquet("./datasets/steam_reviews_cleaned.parquet")
df_it = pd.read_parquet("./datasets/steam_items_cleaned.parquet")

@app.get('/developer/{desarrollador}')
async def calculate_developer_stats(developer_name):
    games_file_path = "./datasets/steam_games_endpoint1_cleaned.parquet"
    yearly_data_list = []
    
    parquet_file = pq.ParquetFile(games_file_path)
    
    for batch in parquet_file.iter_batches(batch_size=10000):
        df_chunk = batch.to_pandas()
        dev_games_chunk = df_chunk[df_chunk['developer'] == developer_name]
        
        yearly_stats = dev_games_chunk.groupby('release_date').agg(
            cantidad_items=('id', 'count'),
            contenido_free=('price', lambda x: (x == 0.00).sum())
        )
        
        yearly_stats['porcentaje_contenido_free'] = (
            yearly_stats['contenido_free'] / yearly_stats['cantidad_items']
        ) * 100
        
        yearly_data_list.append(yearly_stats)
    
    yearly_data_final = pd.concat(yearly_data_list)
    yearly_data_final = yearly_data_final.groupby('release_date').sum()
    yearly_data_final['porcentaje_contenido_free'] = (
        yearly_data_final['contenido_free'] / yearly_data_final['cantidad_items']
    ) * 100
    
    yearly_data_final.rename(columns={
        'cantidad_items': 'Cantidad de Items',
        'porcentaje_contenido_free': 'Contenido Free'
    }, inplace=True)
    
    yearly_data_final['Contenido Free'] = yearly_data_final['Contenido Free'].map("{:.2f}%".format)
    yearly_data_final.sort_values('release_date', ascending=False, inplace=True)
    
    return yearly_data_final.reset_index().to_dict(orient='records')



@app.get("/userdata/{user_id}")
async def user_data(user_id):
       
    # Initialize an empty DataFrame for the final result
    total_spent = 0
    recommend_count = 0
    total_reviews = 0
    number_of_items = 0

    # Open the Parquet files
    games_parquet = pq.ParquetFile("./datasets/steam_games_endpoint2_cleaned.parquet")
    reviews_parquet = pq.ParquetFile("./datasets/steam_rewiews_endpoint2_cleaned.parquet")
    items_parquet = pq.ParquetFile("./datasets/steam_items_endpoint2_cleaned.parquet")

    # Process the items file in batches
    for batch in items_parquet.iter_batches(batch_size=500000):
        items_chunk = batch.to_pandas()
        user_items_chunk = items_chunk[items_chunk['user_id'] == user_id]
        
        # Increment the number of items
        number_of_items += len(user_items_chunk)
        
        # Process the games file in batches
        for game_batch in games_parquet.iter_batches(batch_size=10000):
            games_chunk = game_batch.to_pandas()
            user_games_chunk = user_items_chunk.merge(games_chunk, left_on='item_id', right_on='id', how='left')
            total_spent += user_games_chunk['price'].sum()

        # Process the reviews file in batches
        for review_batch in reviews_parquet.iter_batches(batch_size=10000):
            reviews_chunk = review_batch.to_pandas()
            user_reviews_chunk = user_items_chunk.merge(reviews_chunk, on='item_id', how='left')
            recommend_count += user_reviews_chunk['recommend'].sum()
            total_reviews += len(user_reviews_chunk)

    # Calculate the recommendation percentage
    recommend_percentage = (recommend_count / total_reviews) * 100 if total_reviews else 0

    # Prepare and return the result
    result = {
        "Usuario X": user_id,
        "Dinero gastado": f"{total_spent:.2f} USD",
        "% de recomendación": f"{recommend_percentage:.2f}%",
        "cantidad de items": number_of_items
    }
    
    return result




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
    # Convert year to string to ensure proper filtering
    year = str(year)
    
    # Use pandas to read Parquet files
    df_ga = pd.read_parquet('./datasets/steam_games_endpoint4_cleaned.parquet')
    df_re = pd.read_parquet('./datasets/steam_rewiews_endpoint4_cleaned.parquet')

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

    # Initialize counters for positive and negative reviews
    positive_reviews_count = 0
    negative_reviews_count = 0

    # Load the games dataset and filter by developer
    games_parquet = pq.ParquetFile('./datasets/steam_games_endpoint5_cleaned.parquet')
    developer_games_ids = []
    for batch in games_parquet.iter_batches(batch_size=400000):
        games_chunk = batch.to_pandas()
        filtered_chunk = games_chunk[games_chunk['developer'] == developer]
        developer_games_ids.extend(filtered_chunk['id'].tolist())
    
    # Now process the reviews in batches, only considering the previously filtered game IDs
    reviews_parquet = pq.ParquetFile('./datasets/steam_rewiews_endpoint5_cleaned.parquet')
    for batch in reviews_parquet.iter_batches(batch_size=900000):
        reviews_chunk = batch.to_pandas()
        # Filter reviews for games developed by the specified developer
        developer_reviews_chunk = reviews_chunk[reviews_chunk['item_id'].isin(developer_games_ids)]
        
        # Update positive and negative review counts
        positive_reviews_count += (developer_reviews_chunk['sentiment_analysis'] == 2).sum()
        negative_reviews_count += (developer_reviews_chunk['sentiment_analysis'] == 0).sum()

    # Create and return the result dictionary
    result = {developer: {'Negative': negative_reviews_count, 'Positive': positive_reviews_count}}
    
    return result



    