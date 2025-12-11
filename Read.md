# Mini-analityka danych z JSONPlaceholder

Prosty dashboard analityczny zbudowany w Pythonie z użyciem Streamlit.  
Aplikacja pobiera dane z publicznego API: https://jsonplaceholder.typicode.com i oblicza kilka podstawowych statystyk dotyczących użytkowników, postów, komentarzy i zadań TODO.

## Funkcjonalności

Aplikacja wykorzystuje dane z endpointów:
- `/users`
- `/posts`
- `/comments`
- `/todos`

Na ich podstawie wyliczane są m.in.:
- liczba postów na użytkownika,
- średnia liczba komentarzy na post,
- procent wykonanych zadań (TODOs) per użytkownik,
- top 5 najbardziej komentowanych postów.

## Wizualizacje

W projekcie znajdują się wykresy:
- wykres słupkowy: liczba postów per użytkownik,
- wykres słupkowy: procent wykonanych TODOs,
- wykres słupkowy: top 5 najczęściej komentowanych postów.

## Demo aplikacji

 **Działająca wersja online:**  
https://TUTAJ-WKLEJ-LINK-ZE-STREAMLIT

## 🗂 Repozytorium

👉 **GitHub:**  
https://github.com/TWOJ-LOGIN/TWOJE-REPO

## 🧩 Uruchomienie lokalne

Aby uruchomić aplikację na własnym komputerze:

```bash
git clone https://github.com/TWOJ-LOGIN/TWOJE-REPO.git
cd TWOJE-REPO
pip install -r requirements.txt
streamlit run app.py
