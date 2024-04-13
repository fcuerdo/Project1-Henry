from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
import pandas as pd

# Initialize FastAPI application
app = FastAPI()

@app.get("/")
async def read_root():
    return {"message": "Welcome to the FastAPI application!"}

# Load precalculated datasets for API endpoints
# This ensures that data is ready immediately when the API server starts and is used across different API calls
df_developer_stats = pd.read_parquet('./datasets/developer_stats.parquet')
df_review_analysis = pd.read_parquet('./datasets/review_analysis.parquet')
df_genre_playtime_stats = pd.read_parquet('./datasets/genre_playtime_stats.parquet')
df_user_data = pd.read_parquet('./datasets/user_data.parquet')
df_best_developers_by_year = pd.read_parquet('./datasets/best_developers_by_year.parquet')
# df_recommendation_dataset = pd.read_parquet('./datasets/recommendation_dataset.parquet') # --- On production stage ---

@app.get('/developer/{developer_name}', summary="Obtain developer statistics", 
         description="This endpoint returns the total statistics of games and the percentage of free games for a specific developer.")
async def calculate_developer_stats(developer_name: str):
    """
    Fetch and return the statistics for a specific game developer.
    - **developer_name**: The name of the game developer.
    
    If the developer exists in the dataset, it returns their stats, otherwise it raises an HTTP 404 error.
    """
    if developer_name in df_developer_stats.index:
        stats = df_developer_stats.loc[developer_name].to_dict()
        return stats
    else:
        raise HTTPException(status_code=404, detail=f"Developer named {developer_name} not found")

@app.get("/developer_reviews_analysis/{developer}", summary="Developer review analysis", 
         description="Performs sentiment analysis on the game reviews of a developer and returns the count of positive and negative reviews.")
async def developer_reviews_analysis(developer: str):
    """
    Perform a sentiment analysis of reviews for a specific developer.
    - **developer**: The name of the developer to analyze.
    
    If the developer is found, it maps numeric results to sentiment labels and returns them, otherwise, it raises a 404 error.
    """
    if developer in df_review_analysis.index:
        analysis = df_review_analysis.loc[developer].to_dict()

        # Map numeric results to sentiment labels for better readability
        sentiment_labels = {0: 'Negative', 1: 'Neutral', 2: 'Positive'}
        review_counts_labeled = {sentiment_labels.get(k, k): v for k, v in analysis.items()}
        
        return review_counts_labeled
    else:
        raise HTTPException(status_code=404, detail=f"Developer {developer} not found") 

@app.get("/genre_playtime/{genre}", summary="Get playtime by genre", 
         description="Provides the average playtime of all users for a specific genre in contrast to the average of all genres.")
async def user_for_genre(genre: str):
    """
    Return the average playtime for a specific genre versus the total average playtime.
    - **genre**: The game genre.   
    
    If the genre is found, it returns playtime stats, otherwise, it raises a 404 error.
    """
    if genre in df_genre_playtime_stats.index:
        playtime_stats = df_genre_playtime_stats.loc[genre].to_dict()
        return playtime_stats
    else:
        raise HTTPException(status_code=404, detail=f"Genre {genre} not found")

@app.get("/userdata/{user_id}", summary="Obtain user data", 
         description="Retrieves information about the user's total spending, the number of recommendations, and the percentage of recommendations.")
async def user_data(user_id: str):
    """
    Return relevant user data based on their ID.
    - **user_id**: The unique identifier for the user.
    
    Fetches and returns the user's statistics if found, otherwise returns an error.
    """
    if user_id in df_user_data.index:
        user_stats = df_user_data.loc[user_id].to_dict()
        return user_stats
    else:
        raise HTTPException(status_code=404, detail=f"User ID {user_id} not found")

@app.get("/best_developer_year/{release_date}", summary="Best developers by year",
         description="Finds the most successful developer for a given year based on positive reviews.")
async def best_developer_year(release_date: int):
    """
    Filter by year and obtain the best developer based on the data.
    - **release_date**: The year for which to find the best developer.
    
    If data is available for the year, returns the developer, otherwise raises an HTTP 404 error.
    """
    best_dev_for_year = df_best_developers_by_year[df_best_developers_by_year['release_date'] == release_date]
    
    if not best_dev_for_year.empty:
        best_developer = best_dev_for_year.iloc[0]['developer']
        return {"year": release_date, "best_developer": best_developer}
    else:
        raise HTTPException(status_code=404, detail=f"No data for year {release_date}")
