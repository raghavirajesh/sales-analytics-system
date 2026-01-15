def read_sales_data(filename):
    """
    Reads sales data from file while handling encoding issues.
    Returns list of raw data lines (excluding header and empty lines).
    """

    encodings_to_try = ["utf-8", "latin-1", "cp1252"]
    raw_lines = None

    for enc in encodings_to_try:
        try:
            with open(filename, "r", encoding=enc) as file:
                raw_lines = file.readlines()
            break  # Stop if reading succeeds
        except UnicodeDecodeError:
            continue
        except FileNotFoundError:
            print("Error: File not found!")
            return []

    if raw_lines is None:
        print("Error: Could not read file with supported encodings.")
        return []

    # Remove header row
    raw_lines = raw_lines[1:]

    # Remove empty lines
    cleaned_lines = [line.strip() for line in raw_lines if line.strip()]

    return cleaned_lines

def parse_transactions(raw_lines):
    """
    Parses raw lines into a clean list of transaction dictionaries.

    Returns: list of dictionaries with keys:
    ['TransactionID', 'Date', 'ProductID', 'ProductName',
     'Quantity', 'UnitPrice', 'CustomerID', 'Region']
    """

    transactions = []

    for line in raw_lines:
        line = line.strip()

        # Skip empty lines
        if not line:
            continue

        # Split fields using pipe delimiter
        parts = line.split("|")

        # Handle cases where product name contains commas
        # This may cause extra splits, so we merge product name back
        if len(parts) > 8:
            parts = [
                parts[0], parts[1], parts[2],
                "".join(parts[3:-4]),
                parts[-4], parts[-3], parts[-2], parts[-1]
            ]

        # Skip rows with incorrect number of fields
        if len(parts) != 8:
            continue

        # Assign fields to variables
        transaction_id, date, product_id, product_name, quantity, unit_price, customer_id, region = parts

        # Remove commas from product name
        product_name = product_name.replace(",", "")

        # Remove commas from numeric fields
        quantity = quantity.replace(",", "")
        unit_price = unit_price.replace(",", "")

        # Convert data types
        try:
            quantity = int(quantity)
            unit_price = float(unit_price)
        except:
            continue  # Skip if conversion fails

        # Store cleaned record as dictionary
        transaction = {
            "TransactionID": transaction_id,
            "Date": date,
            "ProductID": product_id,
            "ProductName": product_name,
            "Quantity": quantity,
            "UnitPrice": unit_price,
            "CustomerID": customer_id,
            "Region": region
        }

        transactions.append(transaction)

    return transactions


def validate_and_filter(transactions, region=None, min_amount=None, max_amount=None):
    """
    Validates transactions and applies optional filters.
    Returns: (valid_transactions, invalid_count, filter_summary)
    """

    valid_transactions = []
    invalid_count = 0

    # --- Validation Phase ---
    for tx in transactions:
        if (
            tx["Quantity"] <= 0 or
            tx["UnitPrice"] <= 0 or
            not tx["TransactionID"].startswith("T") or
            not tx["ProductID"].startswith("P") or
            not tx["CustomerID"].startswith("C") or
            tx["Region"].strip() == ""
        ):
            invalid_count += 1
            continue

        # Compute transaction amount
        tx["Amount"] = tx["Quantity"] * tx["UnitPrice"]
        valid_transactions.append(tx)

    total_input = len(transactions)
    filtered_by_region = 0
    filtered_by_amount = 0

    # --- Apply Region Filter ---
    if region:
        before = len(valid_transactions)
        valid_transactions = [tx for tx in valid_transactions if tx["Region"] == region]
        filtered_by_region = before - len(valid_transactions)

    # --- Apply Amount Filters ---
    if min_amount is not None:
        before = len(valid_transactions)
        valid_transactions = [tx for tx in valid_transactions if tx["Amount"] >= min_amount]
        filtered_by_amount += before - len(valid_transactions)

    if max_amount is not None:
        before = len(valid_transactions)
        valid_transactions = [tx for tx in valid_transactions if tx["Amount"] <= max_amount]
        filtered_by_amount += before - len(valid_transactions)

    # --- Summary Dictionary ---
    filter_summary = {
        "total_input": total_input,
        "invalid": invalid_count,
        "filtered_by_region": filtered_by_region,
        "filtered_by_amount": filtered_by_amount,
        "final_count": len(valid_transactions)
    }

    return valid_transactions, invalid_count, filter_summary


