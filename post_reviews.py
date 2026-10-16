import requests
from collections import defaultdict

BASE_URL = "http://localhost:4004/odata/v4/catalog"

# Step 1: Fetch books from CAP
response = requests.get(f"{BASE_URL}/Books")
response.raise_for_status()

books = response.json()["value"]

if not books:
    print("No books found. Check your CAP sample data.")
    raise SystemExit(1)

# Use the first two available books
selected_books = books[:2]

# Step 2: Prepare three reviews
reviews = [
    (selected_books[0], 5, "Excellent book!"),
    (selected_books[0], 4, "Very useful."),
    (
        selected_books[-1],
        3,
        "Good introduction."
    ),
]

ratings_by_book = defaultdict(list)

# Step 3: POST the reviews
for book, rating, comment in reviews:
    payload = {
        "rating": rating,
        "comment": comment,
        "book_ID": book["ID"]
    }

    response = requests.post(
        f"{BASE_URL}/Reviews",
        json=payload
    )
    response.raise_for_status()

    ratings_by_book[book["title"]].append(rating)
    print(f"Review created for: {book['title']}")

# Step 4: Calculate average rating
print("\nAverage ratings:")

for title, ratings in ratings_by_book.items():
    average = sum(ratings) / len(ratings)
    print(f"{title}: {average:.2f}/5")
    