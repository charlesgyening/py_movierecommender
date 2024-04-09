import os
from typing import Final
from telegram import Update
from telegram.ext import ContextTypes
from imdb import IMDb
import requests
from bs4 import BeautifulSoup
from openai_integration import generate_condensed_summary


ia = IMDb()

def recommend_movie(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.message.text
    username = update.message.from_user.username if update.message.from_user.username else "Anonymous"

    # Perform a movie search based on the user's input
    movies = ia.search_movie(query)

    if movies:
        # Extract information from the first search result
        movie = movies[0]
        title = movie['title']
        imdb_id = movie.getID()

        # Get additional information about the movie using the IMDb ID
        movie_details = ia.get_movie(imdb_id)

        # Example: Extract relevant information such as rating, genres, and user reviews
        rating = movie_details.get('rating', 'N/A')
        genres = ', '.join(movie_details.get('genres', []))
        user_reviews = get_user_reviews(imdb_id)
        synopsis = movie_details.get('synopsis', 'No synopsis available')

        # Prepare the data for OpenAI analysis
        input_text = f"User: {username}\nMovie: {title}\nIMDb ID: {imdb_id}\nRating: {rating}/10\nGenres: {genres}\nUser Reviews: {user_reviews}\nSynopsis: {synopsis}"

        # Save the information in a .txt file in the same directory
        save_info_to_txt(title, input_text)

        # Use OpenAI to analyze the content of the .txt file
        condensed_summary = generate_condensed_summary(title)

        return condensed_summary
    else:
        return f"Sorry, couldn't find information for the provided input '{query}'."
def get_user_reviews(imdb_id: str) -> str:
    try:
        # IMDb URL for user reviews
        imdb_url = f'https://www.imdb.com/title/{imdb_id}/reviews'

        # Send an HTTP GET request to the IMDb URL
        response = requests.get(imdb_url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the HTML content of the page using BeautifulSoup
            soup = BeautifulSoup(response.text, 'html.parser')

            # Extract user reviews from the HTML
            user_reviews = soup.find_all('div', class_='text show-more__control')

            # Display only the first three reviews for brevity
            user_reviews = [review.get_text() for review in user_reviews[:3]]
            
            return '\n'.join(user_reviews)

        else:
            return "No user reviews available."

    except Exception as e:
        print(f"Error getting user reviews: {e}")
        return "No user reviews available."

def save_info_to_txt(title: str, content: str) -> None:
    # Get the current directory
    current_directory = os.path.dirname(os.path.abspath(__file__))

    # Create the full path for the .txt file in the same directory
    filename = os.path.join(current_directory, f"{title.replace(' ', '_')}.txt")

    # Write content to the .txt file
    with open(filename, 'w') as file:
        file.write(content)