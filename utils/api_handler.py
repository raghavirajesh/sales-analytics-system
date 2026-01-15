import requests

BASE_URL = "https://dummyjson.com/products"

#--------------3.1--------------# 
def fetch_all_products():
    """
    Fetches all products from DummyJSON API.

    Returns: list of product dictionaries
    """

    try:
        # Using limit=100 to fetch all available products
        response = requests.get(f"{BASE_URL}?limit=100")
        data = response.json()

        print("Successfully fetched products from API")
        return data["products"]

    except:
        print("Failed to fetch products from API")
        return []

def create_product_mapping(api_products):
    """
    Creates a mapping of product IDs to product info.

    Returns: dictionary mapping product ID -> info
    """

    product_mapping = {}

    for product in api_products:
        product_mapping[product["id"]] = {
            "title": product.get("title"),
            "category": product.get("category"),
            "brand": product.get("brand"),
            "rating": product.get("rating")
        }

    return product_mapping

#--------------3.2--------------# 
def enrich_sales_data(transactions, product_mapping):
    """
    Enriches transaction data with API product information.

    Returns: list of enriched transaction dictionaries
    """

    enriched_transactions = []

    for tx in transactions:
        enriched_tx = tx.copy()  # Start with original transaction fields

        try:
            # Extract numeric ID from ProductID (example: P101 -> 101)
            product_id_str = tx["ProductID"]
            numeric_id = int(tx["ProductID"][1:]) - 100

            # Check if this ID exists in API product mapping
            if numeric_id in product_mapping:
                api_info = product_mapping[numeric_id]

                enriched_tx["API_Category"] = api_info["category"]
                enriched_tx["API_Brand"] = api_info["brand"]
                enriched_tx["API_Rating"] = api_info["rating"]
                enriched_tx["API_Match"] = True

            else:
                # Product not found in API
                enriched_tx["API_Category"] = None
                enriched_tx["API_Brand"] = None
                enriched_tx["API_Rating"] = None
                enriched_tx["API_Match"] = False

        except:
            # Any unexpected error → mark as not matched
            enriched_tx["API_Category"] = None
            enriched_tx["API_Brand"] = None
            enriched_tx["API_Rating"] = None
            enriched_tx["API_Match"] = False

        enriched_transactions.append(enriched_tx)

    return enriched_transactions

def save_enriched_data(enriched_transactions, filename="data/enriched_sales_data.txt"):
    """
    Saves enriched transactions back to a pipe-delimited file.
    """

    # Header including new API columns
    header = (
        "TransactionID|Date|ProductID|ProductName|Quantity|UnitPrice|CustomerID|Region|"
        "API_Category|API_Brand|API_Rating|API_Match\n"
    )

    try:
        with open(filename, "w", encoding="utf-8") as file:
            file.write(header)

            for tx in enriched_transactions:
                line = (
                    f"{tx['TransactionID']}|{tx['Date']}|{tx['ProductID']}|{tx['ProductName']}|"
                    f"{tx['Quantity']}|{tx['UnitPrice']}|{tx['CustomerID']}|{tx['Region']}|"
                    f"{tx['API_Category']}|{tx['API_Brand']}|{tx['API_Rating']}|{tx['API_Match']}\n"
                )

                file.write(line)

        print("Enriched data saved successfully!")

    except:
        print("Error saving enriched data file!")


