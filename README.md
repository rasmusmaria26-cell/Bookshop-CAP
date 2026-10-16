# Bookshop

A sample book-catalog application built with the SAP Cloud Application Programming Model (CAP). It exposes books, authors, and reviews through an OData v4 service and includes a stock-aware order action.

## Features

- Browse books and authors through the catalog service.
- View a book's author and other related data using OData query options.
- Submit an order that reduces stock only when enough copies are available.
- Automatically append an `11% off!` label to the titles of books with stock greater than 100.
- Create book reviews; ratings must be whole numbers from 1 to 5.
- Use the included Python script to post sample reviews and calculate average ratings.

## Requirements

- Node.js 20 or later
- npm
- Python 3 and the `requests` package (only if running `post_reviews.py`)

## Run locally

From the project directory, install dependencies and start the CAP server:

```sh
npm install
npm start
```

The service starts at `http://localhost:4004`. For development with automatic reload, install the CAP development kit and run `cds watch`:

```sh
npm install --global @sap/cds-dk
cds watch
```

CAP loads the sample CSV data from `db/data` when the service starts with the default local database configuration.

## Catalog API

The OData v4 service is available at:

```text
http://localhost:4004/odata/v4/catalog
```

Useful endpoints:

| Endpoint | Description |
|---|---|
| `/Books` | List books |
| `/Books(1)` | Retrieve a book by ID |
| `/Authors` | List authors |
| `/Reviews` | List reviews |
| `/$metadata` | View the OData service metadata |

For example, list books with stock greater than 100 and include their authors:

```text
http://localhost:4004/odata/v4/catalog/Books?$filter=stock%20gt%20100&$expand=author
```

### Submit an order

`submitOrder` accepts a book ID and a quantity. For example:

```sh
curl -X POST http://localhost:4004/odata/v4/catalog/submitOrder \
  -H "Content-Type: application/json" \
  -d "{\"book\":1,\"quantity\":2}"
```

The action subtracts the requested quantity from stock when sufficient stock is available. If there is not enough stock, the service responds with HTTP `409 Conflict`.

### Create a review

Create a review by posting its rating, comment, and related book ID:

```sh
curl -X POST http://localhost:4004/odata/v4/catalog/Reviews \
  -H "Content-Type: application/json" \
  -d "{\"rating\":5,\"comment\":\"Excellent book!\",\"book_ID\":1}"
```

Ratings outside the integer range 1–5 are rejected with HTTP `400 Bad Request`.

## Optional: post sample reviews

With the CAP server running, install the Python dependency and run the included script:

```sh
python -m pip install requests
python post_reviews.py
```

The script posts three reviews for books returned by the service and prints the average for each reviewed title. Running it again creates additional reviews.

## Project structure

| Path | Purpose |
|---|---|
| `db/schema.cds` | Books, authors, and reviews data model |
| `db/data/*.csv` | Sample books and authors |
| `srv/cat-service.cds` | Catalog service entities and `submitOrder` action |
| `srv/cat-service.js` | Order handling, stock discounts, and review validation |
| `post_reviews.py` | Optional script to post reviews and calculate averages |
| `package.json` | Node.js dependencies and start command |

## License

This project is marked `UNLICENSED` in `package.json`; no reuse or distribution license is specified.

## References

- [SAP Cloud Application Programming Model](https://cap.cloud.sap)
- [SAP CAP sample projects](https://github.com/SAP-samples/cloud-cap-samples)
