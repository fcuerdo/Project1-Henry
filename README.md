![!\[wp9013291-status-logo-wallpapers\](https://github.com/fcuerdo/Project1-Henry/assets/33520476/9d66c3fb-2544-4002-a2c5-1bbeec270](https://github.com/fcuerdo/Project1-Henry/blob/master/Hardware_SteamLogo_Banner.png)

# Steam Insight Engine

### In an ever-evolving digital world, the "Steam Insight Engine" emerges as a key initiative to unravel and enhance user interaction on Steam, a leading platform in video game distribution. This project focuses on analyzing and providing accessible understanding of Steam data, offering review analysis, game recommendations, and developer statistics to enrich user experience.

## Why Steam?

We chose Steam due to its rich database and diverse community, allowing us to extract valuable insights to improve the experience of both players and developers. Players benefit by discovering games that align with their tastes, while developers gain crucial insights to create more engaging games.

## Problems Solved

This project addresses the challenge of game discovery in a vast library, helping users find games that match their preferences and providing developers with essential data to optimize their creations.

## Objective

The main objective of this project is to provide users with a convenient way to interact with data related to games on the Steam platform, offering functionalities like review analysis, game recommendations, and developer statistics.

## API Endpoints

### GET /developer/{developer_name}

**Description:** Retrieves statistics for a specific developer.<br>
**Parameter:** developer_name (name of the developer).<br>
**Response:** Returns a set of developer statistics, including the number of games, free content, and percentage of free content per year. If the developer is not found, returns a 404 error.

### GET /userdata/{user_id}

**Description:** Retrieves user data, including total spending, recommendation percentage, and number of items.<br>
**Parameter:** user_id (user identifier).<br>
**Response:** Detailed user information. If the user_id is not found, returns a 404 error.

### GET /user_for_genre/{genre}

**Description:** Finds the user with the most hours played for a specific genre.<br>
**Parameter:** genre (game genre).<br>
**Response:** Returns the user with the most hours played in that genre, total hours played, and hours played per year. If the genre is not found, returns an error message.

### GET /best_developer_year/{year}

**Description:** Identifies the top developers in a specific year.<br>
**Parameter:** year (year of interest).<br>
**Response:** List of top developers and their positive recommendations that year. If there are no data for that year, returns an error message.

### GET /developer_reviews_analysis/{developer}

**Description:** Performs a review analysis for a specific developer.<br>
**Parameter:** developer (name of the developer).<br>
**Response:** Count of positive and negative reviews for the developer. If the developer is not found, returns an error message.

### GET /recommendations/{game_id}

**Description:** Provides game recommendations based on genre similarity.<br>
**Parameter:** game_id (game identifier) and optionally num_recommendations (number of recommendations to return).<br>
**Response:** List of recommended games. If the game is not found, returns a 404 error.

These endpoints provide a rich and versatile interface for interacting with Steam data, facilitating access to valuable information for both developers and platform users.

## Modules and Libraries Used

### Python

- **Pandas:** For data manipulation and analysis.
- **NumPy:** For numerical calculations.
- **Matplotlib and Seaborn:** For data visualization.
- **NLTK:** For text processing and sentiment analysis.
- **FastAPI:** For API implementation.
- **PyArrow:** For handling Parquet files.

## Project Structure

The project is structured into the following main components:

- **data/:** Contains the datasets used in the project.
- **datasets/:** Directory where processed and cleaned datasets are stored in Parquet format.
- **api/:** Contains files related to the implementation of the API using FastAPI.
- **notebooks/:** Jupyter Notebooks used for exploratory analysis and model development.
- **README.md:** This file, which provides a general overview of the project, its objectives, and functionalities.

## Deployment

This project is deployed on [Render](https://render.com/). You can access the API on Render at the following URL: [fcuerdo/](https://steamrecommendation.onrender.com).

## Usage Guide

1. Clone this repository to your local machine.
2. Install the required dependencies using `pip install -r requirements.txt`.
3. Run the API using the command `uvicorn api.main:app --reload`.
4. Visit `http://localhost:8000/docs` in your browser to view the interactive API documentation and perform queries.

## Contribution

Contributions are welcome. If you wish to contribute to the project, please follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/feature-name`).
3. Make your changes and commit them (`git commit -am 'Add new feature'`).
4. Push the branch (`git push origin feature/feature-name`).
5. Create a new Pull Request.

## Author

- **Facundo Cuerdo**
- GitHub: [fcuerdo](https://github.com/fcuerdo)
- LinkedIn: [fcuerdo](https://www.linkedin.com/in/fcuerdo/)