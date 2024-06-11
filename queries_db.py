import sqlite3

def query_database():
    conn = sqlite3.connect('tutorial2.db')  # Zmień ścieżkę do pliku bazy danych jeśli to konieczne
    cursor = conn.cursor()

    # Wykonanie zapytania
    cursor.execute("SELECT * FROM users_test")

    # Pobranie wyników
    results = cursor.fetchall()

    # Wyświetlenie wyników
    for row in results:
        print(row)

    # Zamknięcie połączenia
    cursor.close()
    conn.close()

if __name__ == "__main__":
    query_database()
