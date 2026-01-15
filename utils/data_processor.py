#--------------2.1--------------# 
def calculate_total_revenue(transactions):
    """
    Calculates total revenue from all transactions

    Returns: float (total revenue)

    Expected Output: Single number representing sum of (Quantity * UnitPrice)
    Example: 1545000.50
    """

    total_revenue = 0.0

    # Loop through each transaction and add Quantity * UnitPrice
    for tx in transactions:
        total_revenue += tx["Quantity"] * tx["UnitPrice"]

    return total_revenue


def region_wise_sales(transactions):
    """
    Analyzes sales by region

    Returns: dictionary with region statistics

    Expected Output Format:
    {
        'North': {
            'total_sales': 450000.0,
            'transaction_count': 15,
            'percentage': 29.13
        },
        ...
    }
    """

    region_data = {}
    total_revenue = calculate_total_revenue(transactions)

    # Step 1: Aggregate sales and count per region
    for tx in transactions:
        region = tx["Region"]
        amount = tx["Quantity"] * tx["UnitPrice"]

        if region not in region_data:
            region_data[region] = {
                "total_sales": 0.0,
                "transaction_count": 0
            }

        region_data[region]["total_sales"] += amount
        region_data[region]["transaction_count"] += 1

    # Step 2: Calculate percentage of total sales
    for region in region_data:
        sales = region_data[region]["total_sales"]
        percentage = (sales / total_revenue) * 100 if total_revenue > 0 else 0
        region_data[region]["percentage"] = round(percentage, 2)

    # Step 3: Sort dictionary by total_sales descending
    sorted_regions = dict(
        sorted(region_data.items(), key=lambda item: item[1]["total_sales"], reverse=True)
    )

    return sorted_regions


def top_selling_products(transactions, n=5):
    """
    Finds top n products by total quantity sold

    Returns: list of tuples

    Expected Output Format:
    [
        ('Laptop', 45, 2250000.0),
        ('Mouse', 38, 19000.0),
        ...
    ]
    """

    product_data = {}

    # Step 1: Aggregate quantity and revenue per product
    for tx in transactions:
        product = tx["ProductName"]       # Aggregate by ProductName
        quantity = tx["Quantity"]         # Grab quantity
        revenue = tx["Quantity"] * tx["UnitPrice"]  # Compute revenue

        if product not in product_data:
            product_data[product] = {
                "total_quantity": 0,
                "total_revenue": 0.0
            }

        product_data[product]["total_quantity"] += quantity
        product_data[product]["total_revenue"] += revenue

    # Step 2: Convert to list of tuples
    product_list = []
    for product in product_data:
        data = product_data[product]
        product_list.append(
            (product, data["total_quantity"], data["total_revenue"])
        )

    # Step 3: Sort by total_quantity descending
    product_list.sort(key=lambda x: x[1], reverse=True)  #Sort by Quantity Decending

    # Step 4: Return top n
    return product_list[:n]


def customer_analysis(transactions):
    """
    Analyzes customer purchase patterns

    Returns: dictionary of customer statistics

    Expected Output Format:
    {
        'C001': {
            'total_spent': 95000.0,
            'purchase_count': 3,
            'avg_order_value': 31666.67,
            'products_bought': ['Laptop', 'Mouse', 'Keyboard']
        },
        ...
    }
    """

    customer_data = {}

    # Step 1: Aggregate per customer
    for tx in transactions:
        customer = tx["CustomerID"]
        product = tx["ProductName"]
        amount = tx["Quantity"] * tx["UnitPrice"]

        if customer not in customer_data:
            customer_data[customer] = {
                "total_spent": 0.0,
                "purchase_count": 0,
                "products_bought": set()  # using set to avoid duplicates
            }

        customer_data[customer]["total_spent"] += amount
        customer_data[customer]["purchase_count"] += 1
        customer_data[customer]["products_bought"].add(product)

    # Step 2: Calculate average order value & convert product sets to list
    for customer in customer_data:
        total_spent = customer_data[customer]["total_spent"]
        count = customer_data[customer]["purchase_count"]

        avg_order = total_spent / count if count > 0 else 0

        customer_data[customer]["avg_order_value"] = round(avg_order, 2)
        customer_data[customer]["products_bought"] = list(
            customer_data[customer]["products_bought"]
        )

    # Step 3: Sort customers by total_spent descending
    sorted_customers = dict(
        sorted(customer_data.items(), key=lambda item: item[1]["total_spent"], reverse=True)
    )

    return sorted_customers

#--------------2.2--------------#
def daily_sales_trend(transactions):
    """
    Analyzes sales trends by date.

    Returns:
    Dictionary sorted by date with:
    revenue, transaction_count, unique_customers
    """

    daily_data = {}

    for tx in transactions:
        date = tx["Date"]
        amount = tx["Quantity"] * tx["UnitPrice"]
        customer = tx["CustomerID"]

        # Create date entry if not present
        if date not in daily_data:
            daily_data[date] = {
                "revenue": 0.0,
                "transaction_count": 0,
                "unique_customers": set()
            }

        # Update daily metrics
        daily_data[date]["revenue"] += amount
        daily_data[date]["transaction_count"] += 1
        daily_data[date]["unique_customers"].add(customer)

    # Convert customer sets to counts
    for date in daily_data:
        daily_data[date]["unique_customers"] = len(daily_data[date]["unique_customers"])

    # Sort dictionary by date
    sorted_daily_data = dict(sorted(daily_data.items()))

    return sorted_daily_data

def find_peak_sales_day(transactions):
    """
    Identifies the date with highest revenue.
    Returns tuple: (date, revenue, transaction_count)
    """

    daily_sales = {}

    for tx in transactions:
        date = tx["Date"]
        amount = tx["Quantity"] * tx["UnitPrice"]

        if date not in daily_sales:
            daily_sales[date] = {
                "revenue": 0.0,
                "transaction_count": 0
            }

        daily_sales[date]["revenue"] += amount
        daily_sales[date]["transaction_count"] += 1

    # Find date with maximum revenue
    peak_date = max(daily_sales.items(), key=lambda x: x[1]["revenue"])

    return (
        peak_date[0],
        peak_date[1]["revenue"],
        peak_date[1]["transaction_count"]
    )


#--------------2.3--------------#
def low_performing_products(transactions, threshold=10):
    """
    Identifies products with total quantity less than threshold.
    Returns list of tuples:
    (ProductName, TotalQuantity, TotalRevenue)
    """

    product_data = {}

    for tx in transactions:
        product = tx["ProductName"]
        quantity = tx["Quantity"]
        revenue = tx["Quantity"] * tx["UnitPrice"]

        if product not in product_data:
            product_data[product] = {
                "total_quantity": 0,
                "total_revenue": 0.0
            }

        product_data[product]["total_quantity"] += quantity
        product_data[product]["total_revenue"] += revenue

    # Collect only low performing products
    low_products = []

    for product, data in product_data.items():
        if data["total_quantity"] < threshold:
            low_products.append(
                (product, data["total_quantity"], data["total_revenue"])
            )

    # Sort by total quantity ascending
    low_products.sort(key=lambda x: x[1])

    return low_products
