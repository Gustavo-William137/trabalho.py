import requests
from bs4 import BeautifulSoup
import pandas as pd

def get_movies():
    url = "https://www.themoviedb.org/movie"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36"
    }

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Erro ao acessar o site: {response.status_code}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    movie_cards = soup.select("div.card")
    print(f"{len(movie_cards)} filmes encontrados.")

    movies_data = []

    for idx, card in enumerate(movie_cards, start=1):
        title_elem = card.select_one("h2 a")
        year_elem = card.select_one("span.release_date")

        title = title_elem.text.strip() if title_elem else "N/A"
        year = year_elem.text.strip() if year_elem else "N/A"

        movies_data.append({
            "Posição": idx,
            "Título": title,
            "Ano": year
        })

    return movies_data

if __name__ == "__main__":
    print("Coletando dados do TMDb...")
    movies = get_movies()

    if movies:
        df = pd.DataFrame(movies)
        df.to_csv("tmdb_movies.csv", index=False, encoding="utf-8-sig")
        print("Arquivo 'tmdb_movies.csv' gerado com sucesso!")
    else:
        print("Nenhum filme foi coletado.")
