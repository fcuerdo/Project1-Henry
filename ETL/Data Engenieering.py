# %% [markdown]
# # Modules Import
# 

# %% [markdown]
# ### In this section, we import all necessary libraries for our data processing and analysis tasks. This includes libraries for handling data structures (pandas, numpy), visualization (matplotlib, seaborn), working with JSON and compressed files (json, gzip), and text processing (nltk, re)

# %%

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



#Stop words download
#nltk.download('vader_lexicon')
#nltk.download('stopwords')
#nltk.download('punkt')



# %%
def optimize_dataframe_types(df):
    """
    Optimizes data types in a pandas DataFrame to reduce memory usage.
    """
    # Convert object types to categories where appropriate
    for col in df.select_dtypes(include=['object']).columns:
        if df[col].nunique() / len(df[col]) < 0.5:  # Arbitrary threshold
            df[col] = df[col].astype('category')
    
    # Convert integers to the smallest possible int subclass
    for col in df.select_dtypes(include=['int']).columns:
        df[col] = pd.to_numeric(df[col], downcast='integer')
    
    # Convert floats to the smallest possible float subclass
    for col in df.select_dtypes(include=['float']).columns:
        df[col] = pd.to_numeric(df[col], downcast='float')
    
    return df

# %% [markdown]
# # Datasets Import
# 

# %% [markdown]
# ## Games Dataset

# %% [markdown]
# ### Here, we load and preprocess the dataset containing information about various games. This involves reading from a compressed .gz file, decoding JSON objects, and cleaning the data by dropping rows that are completely null.

# %%
file_path_games = r"PI MLOps - STEAM\steam_games.json.gz"
df_ga = []
with gzip.open(file_path_games, 'r') as gz_file:
    for line in gz_file:
        json_obj = json.loads(line.decode('utf-8'))
        df_ga.append(json_obj)
df_ga = pd.DataFrame(df_ga)

df_ga = df_ga.dropna(how = 'all')

df_ga.head()


# %%
# Deleting unnecesary columns
df_ga = df_ga.drop(columns=['publisher', 'title', 'url', 'early_access','reviews_url', 'tags'])


# %%
# Usaremos 'apply' para aplicar una función lambda a cada elemento de la columna 'price'.
df_ga['price'] = df_ga['price'].apply(lambda x: 0 if isinstance(x, str) and x not in [np.nan, None, 'NaN'] else x)

# Ahora, convierte toda la columna a un tipo numérico, reemplazando cualquier valor no convertible con NaN.
df_ga['price'] = pd.to_numeric(df_ga['price'], errors='coerce')


# %%
# Your existing code for handling 'Unknown' values
df_ga['release_date'] = df_ga['release_date'].astype('object')  # Convert to object
df_ga['release_date'] = df_ga['release_date'].fillna(value='Unknown')
df_ga['release_date'] = df_ga['release_date'].replace({'Soon..': 'Unknown'})

# Convert to datetime where possible
df_ga['release_date'] = pd.to_datetime(df_ga['release_date'], errors='coerce')

# Extract the year from valid datetime objects and fill NaT with None
df_ga['release_date'] = df_ga['release_date'].dt.year

# Separate the data into two parts: valid years and 'Unknown'
valid_years = df_ga['release_date'].dropna().astype(int)
unknown_dates = df_ga['release_date'].isna()

# Assign the year as integer where valid, and 'Unknown' where invalid
df_ga['release_date'] = df_ga['release_date'].where(~unknown_dates, 'Unknown')
df_ga.loc[~unknown_dates, 'release_date'] = valid_years

# %%
df_ga.head()

# %%
# Converting all non-list values in empty lists
df_ga['genres'] = df_ga['genres'].apply(lambda x: x if isinstance(x, list) else [])

# Genres subset
genres_set = set(genre for sublist in df_ga['genres'] for genre in sublist)

# Creating a Column for each genre
for genre in genres_set:
    df_ga[f'genre_{genre}'] = df_ga['genres'].apply(lambda x: 1 if genre in x else 0)


# Droping original column
df_ga.drop('genres', axis=1, inplace=True)

df_ga.head()

# %%
# Converting all non-list values in empty lists
df_ga['specs'] = df_ga['specs'].apply(lambda x: x if isinstance(x, list) else [])

# Spec subset
specs_set = set(spec for sublist in df_ga['specs'] for spec in sublist)

# Creating a Column for each specs
for spec in specs_set:
    df_ga[f'spec_{spec}'] = df_ga['specs'].apply(lambda x: 1 if spec in x else 0)


# Droping original column
df_ga.drop('specs', axis=1, inplace=True)

df_ga.head()

# %%
df_ga = optimize_dataframe_types(df_ga)  # Apply optimization after loading

# %%
df_ga_endpoint1 = df_ga
df_ga_endpoint1 = df_ga_endpoint1.dropna(subset=['developer'])
df_ga_endpoint1['release_date'] = df_ga_endpoint1['release_date'].astype(str)
df_ga_endpoint1 = df_ga_endpoint1[df_ga_endpoint1['release_date'] != 'Unknown']
columns_to_keep = ['app_name', 'release_date', 'price', 'id', 'developer']
df_ga_endpoint1 = df_ga_endpoint1[columns_to_keep]
df_ga_endpoint1

# %%
df_ga_endpoint1.to_parquet('./datasets/steam_games_endpoint1_cleaned.parquet', index=False, compression='gzip')

# %%
df_ga_endpoint2 = df_ga_endpoint1
columns_to_keep2 = ['price', 'id']
df_ga_endpoint2 = df_ga_endpoint2[columns_to_keep2]
df_ga_endpoint2

# %%
df_ga_endpoint2.to_parquet('./datasets/steam_games_endpoint2_cleaned.parquet', index=False, compression='gzip')

# %%
df_ga_endpoint3 = df_ga
df_ga_endpoint3 = df_ga_endpoint3.dropna(subset=['developer'])
Columns_to_keep5 = ['id'] + [col for col in df_ga_endpoint3.columns if col.startswith('genre_')]
df_ga_endpoint3 = df_ga_endpoint3[Columns_to_keep5]
columns_to_drop = [col for col in df_ga_endpoint3.columns if col.startswith('genre_') and (df_ga_endpoint3[col] == 1).sum() < 20]
df_ga_endpoint3.drop(columns=columns_to_drop, inplace=True)
df_ga_endpoint3


# %%
df_ga_endpoint3.to_parquet('./datasets/steam_games_endpoint3_cleaned.parquet', index=False, compression='gzip')

# %%
df_ga_endpoint4 = df_ga_endpoint1
columns_to_keep6 = ['developer', 'id', 'release_date']
df_ga_endpoint4 = df_ga_endpoint4[columns_to_keep6]
df_ga_endpoint4

# %%
df_ga_endpoint4.to_parquet('./datasets/steam_games_endpoint4_cleaned.parquet', index=False, compression='gzip')

# %%
df_ga_endpoint5 = df_ga_endpoint1
columns_to_keep8 = ['developer', 'id']
df_ga_endpoint5 = df_ga_endpoint5[columns_to_keep8]
df_ga_endpoint5

# %%
df_ga_endpoint5.to_parquet('./datasets/steam_games_endpoint5_cleaned.parquet', index=False, compression='gzip')

# %%
# Copy the DataFrame to avoid modifying the original
df_ga_recommend = df_ga.copy()

# Drop rows where 'developer' is NaN to clean the data
df_ga_recommend.dropna(subset=['developer'], inplace=True)

# Dynamically find the genre and specification columns
genre_spec_columns = [col for col in df_ga_recommend.columns if col.startswith('genre_') or col.startswith('spec_')]

# Filter columns to only keep those with more than 30 '1' values
columns_to_keep10 = ['id', 'app_name', 'developer']  # Base columns to keep
for col in genre_spec_columns:
    if df_ga_recommend[col].sum() > 500:
        columns_to_keep10.append(col)

# Update the DataFrame to only keep the selected columns
df_ga_recommend = df_ga_recommend[columns_to_keep10]



# %%
df_ga_recommend['id'].dropna()


# %%
df_ga_recommend.to_parquet('./datasets/steam_games_recommend_cleaned.parquet', index=False, compression='gzip')



# %%
df_ga_recommend

# %%
df_ga.info()

# %%
game_info = df_ga[df_ga['id'] == '591960']
game_info

# %% [markdown]
# ## Reviews Dataset

# %% [markdown]
# ### Similarly, for the reviews dataset, we process each line from a JSON file, handling potential errors and converting lines into a list of dictionaries, which we then transform into a DataFrame. This step is crucial for structuring the reviews data for further analysis.

# %%
data_list = []


# File Path
file_path = r"PI MLOps - STEAM\user_reviews.json\australian_user_reviews.json"


# Processing each line
with open(file_path, 'r', encoding='utf-8') as file:
    for line in file:
        try:
            # Usar ast.literal_eval para convertir la línea en un diccionario
            json_data = ast.literal_eval(line)
            data_list.append(json_data)
        except ValueError as e:
            print(f"Error in line: {line}")
            continue

# Crafting DataFrame from dic list
df_re = pd.DataFrame(data_list)

# Removing user_url attribute
df_re = df_re.drop(['user_url'], axis= 1)

# Removing Null Registers
df_re = df_re.dropna(how = 'all')

# Reset index
df_re = df_re.reset_index(drop=True)

# %%
df_re

# %%
# Exploding reviews column
df_re= df_re.explode('reviews')

# Filtering registers with one relevant key
df_re = df_re[df_re['reviews'].apply(lambda x: isinstance(x, dict) and 'review' in x)]

# Attributes assign
df_re['funny'] = df_re['reviews'].apply(lambda x: x.get('funny'))
df_re['posted'] = df_re['reviews'].apply(lambda x: x.get('posted'))
df_re['last_edited'] = df_re['reviews'].apply(lambda x: x.get('last_edited'))
df_re['item_id'] = df_re['reviews'].apply(lambda x: x.get('item_id'))
df_re['helpful'] = df_re['reviews'].apply(lambda x: x.get('helpful'))
df_re['recommend'] = df_re['reviews'].apply(lambda x: x.get('recommend'))
df_re['review_text'] = df_re['reviews'].apply(lambda x: x.get('review'))

# Removing 'Reviews' column
df_re.drop(columns=['reviews'], inplace=True)

# Removing Duplicates
df_re.drop_duplicates(inplace=True)



# %%
df_re = df_re.drop(columns = ['funny', 'last_edited','helpful'])

# %%
df_re

# %% [markdown]
# ### NLP Classification

# %% [markdown]
# #### In order to analyze the sentiment of user reviews, we first preprocess the text to remove URLs, special characters, and numbers, and to tokenize the text. This preprocessing step is vital for reducing noise in the text data and improving the performance of our sentiment analysis.

# %%
# Start Stemmer
stemmer = PorterStemmer()

def preprocess_text(text):
    '''
    Function to preprocess text by lowering case, removing URLs, special characters, and numbers,
    tokenizing, removing stopwords, and applying stemming.
    '''
    text = text.lower()  # Convert to lowercase
    text = re.sub(r'http\S+', '', text)  # URLs delete
    text = re.sub(r'[^a-z\s]', '', text)  # Numbers and Special Characters delete
    tokens = word_tokenize(text)  # Tokenization
    tokens = [stemmer.stem(word) for word in tokens if word not in set(stopwords.words('english'))]  # Stopwords delete and Steeming
    return ' '.join(tokens)

# Deploying preprocessing function
df_re['cleaned_review'] = df_re['review_text'].apply(preprocess_text) 

    

# %% [markdown]
# #### We utilize the VADER tool from the nltk library to perform sentiment analysis on the preprocessed review texts. This tool is particularly suited for texts from social media and similar contexts due to its sensitivity to both the polarity and intensity of emotions.

# %%
# Creating Analyzer Instance
sid = SentimentIntensityAnalyzer()

def sentiment_analysis_vader(text):
    if pd.isna(text):
        return 1  # Neutral if there is no text
    
    # Sentiment Score
    scores = sid.polarity_scores(text)

    # Score Assign
    compound = scores['compound']
    if compound >= 0.05:
        return 2  # Positive
    elif compound <= -0.05:
        return 0  # Negative
    else:
        return 1  # Neutral

# Deploying function to Dataset
df_re['sentiment_analysis'] = df_re['cleaned_review'].apply(sentiment_analysis_vader)



# %%
df_re

# %%
df_re_endpoint2 = df_re
df_re_endpoint2 = df_re_endpoint2.dropna(subset=['recommend'])
columns_to_keep4 = ['user_id', 'item_id', 'recommend']
df_re_endpoint2 = df_re_endpoint2[columns_to_keep4]
df_re_endpoint2

# %%
df_re_endpoint2 = optimize_dataframe_types(df_re_endpoint2)  # Apply optimization after loading

# %%
df_re_endpoint2.to_parquet('./datasets/steam_rewiews_endpoint2_cleaned.parquet', index=False, compression='gzip')

# %%
df_re_endpoint4 = df_re
df_re_endpoint4 = df_re_endpoint4.dropna(subset=['recommend'])
columns_to_keep7 = ['item_id', 'recommend', 'sentiment_analysis']
df_re_endpoint4 = df_re_endpoint4[columns_to_keep7]
df_re_endpoint4

# %%
df_re_endpoint4.to_parquet('./datasets/steam_rewiews_endpoint4_cleaned.parquet', index=False, compression='gzip')

# %%
df_re_endpoint5 = df_re_endpoint4
columns_to_keep9 = ['item_id', 'sentiment_analysis']
df_re_endpoint5 = df_re_endpoint5[columns_to_keep9]
df_re_endpoint5

# %%
df_re_endpoint5.to_parquet('./datasets/steam_rewiews_endpoint5_cleaned.parquet', index=False, compression='gzip')

# %%
review_info = df_re[df_re['sentiment_analysis'] == 0]




# %%
df_re['sentiment_analysis'].value_counts()


# %% [markdown]
# ### Items Dateset

# %% [markdown]
# #### In this section, we focus on the dataset that contains information about users' items. This includes the games or software owned by users on the Steam platform. We start by loading the data from a JSON file and proceed to clean it by removing entries that don't provide meaningful information.

# %%
data_list = []


# File Path
file_path = r"PI MLOps - STEAM\users_items.json\australian_users_items.json"


#Open file processing all lines
with open(file_path, 'r', encoding='utf-8') as file:
    for line in file:
        try:
            # Converting to Dict
            json_data = ast.literal_eval(line)
            data_list.append(json_data)
        except ValueError as e:
            print(f"Error in line: {line}")
            continue

#Converting Dict list to Dataframe
df_it = pd.DataFrame(data_list)

df_it = df_it.drop(['user_url'], axis= 1)

# %%
df_it

# %%
#Delete users with no items
df_it = df_it[df_it['items_count'] != 0]

# %%
# Convert item to dict
def convert_to_dict(item):
    try:
        return ast.literal_eval(item)
    except:
        return None

# Applying function to each item register
df_it['items'] = df_it['items'].apply(lambda x: convert_to_dict(x) if isinstance(x, str) else x)

# Apply explode to items as a dict
df_it = df_it.explode('items')

# Assign attributes to new columns
df_it['item_id'] = df_it['items'].apply(lambda x: x.get('item_id') if isinstance(x, dict) else None)
df_it['item_name'] = df_it['items'].apply(lambda x: x.get('item_name') if isinstance(x, dict) else None)
df_it['playtime_forever'] = df_it['items'].apply(lambda x: x.get('playtime_forever') if isinstance(x, dict) else None)
df_it['playtime_2weeks'] = df_it['items'].apply(lambda x: x.get('playtime_2weeks') if isinstance(x, dict) else None)

# Drop 'items' columns
df_it.drop(columns=['items'], inplace=True)




# %%
df_it.drop_duplicates(inplace = True)
df_it_endpoint2 = df_it
df_it_endpoint2 = df_it_endpoint2.dropna(subset=['user_id'])
df_it_endpoint2 = df_it_endpoint2[df_it_endpoint2['playtime_forever'] != 0]
columns_to_keep3 = ['user_id', 'item_id', 'playtime_forever']
df_it_endpoint2 = df_it_endpoint2[columns_to_keep3]

# %%
df_it_endpoint2 = optimize_dataframe_types(df_it_endpoint2)  # Apply optimization after loading

# %%
df_it_endpoint2

# %%
df_it_endpoint2.to_parquet('./datasets/steam_items_endpoint2_cleaned.parquet', index=False, compression='gzip')


