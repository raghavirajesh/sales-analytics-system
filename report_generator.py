from datetime import datetime
from collections import defaultdict

def generate_sales_report(transactions, enriched_transactions, output_file='output/sales_report.txt'):
    """
    Generates a comprehensive formatted text report
    """

    # ---------- BASIC METRICS ----------
    total_transactions = len(transactions)
    total_revenue = sum(tx["Quantity"] * tx["UnitPrice"] for tx in transactions)
    avg_order_value = total_revenue / total_transactions if total_transactions else 0

    dates = [tx["Date"] for tx in transactions]
    date_range = f"{min(dates)} to {max(dates)}" if dates else "N/A"

    # ---------- REGION-WISE ----------
    region_sales = defaultdict(lambda: {"revenue": 0, "count": 0})

    for tx in transactions:
        region = tx["Region"]
        revenue = tx["Quantity"] * tx["UnitPrice"]
        region_sales[region]["revenue"] += revenue
        region_sales[region]["count"] += 1

    # Sort by revenue descending
    region_sorted = sorted(region_sales.items(), key=lambda x: x[1]["revenue"], reverse=True)

    # ---------- TOP 5 PRODUCTS ----------
    product_stats = defaultdict(lambda: {"qty": 0, "revenue": 0})

    for tx in transactions:
        name = tx["ProductName"]
        qty = tx["Quantity"]
        revenue = qty * tx["UnitPrice"]
        product_stats[name]["qty"] += qty
        product_stats[name]["revenue"] += revenue

    top_products = sorted(product_stats.items(), key=lambda x: x[1]["qty"], reverse=True)[:5]

    # ---------- TOP 5 CUSTOMERS ----------
    customer_stats = defaultdict(lambda: {"spent": 0, "orders": 0})

    for tx in transactions:
        cid = tx["CustomerID"]
        revenue = tx["Quantity"] * tx["UnitPrice"]
        customer_stats[cid]["spent"] += revenue
        customer_stats[cid]["orders"] += 1

    top_customers = sorted(customer_stats.items(), key=lambda x: x[1]["spent"], reverse=True)[:5]

    # ---------- DAILY TREND ----------
    daily_stats = defaultdict(lambda: {"revenue": 0, "transactions": 0, "customers": set()})

    for tx in transactions:
        date = tx["Date"]
        revenue = tx["Quantity"] * tx["UnitPrice"]
        daily_stats[date]["revenue"] += revenue
        daily_stats[date]["transactions"] += 1
        daily_stats[date]["customers"].add(tx["CustomerID"])

    daily_sorted = sorted(daily_stats.items())

    # ---------- PRODUCT PERFORMANCE ----------
    best_selling_day = max(daily_stats.items(), key=lambda x: x[1]["revenue"])[0] if daily_stats else "N/A"

    low_products = [name for name, stats in product_stats.items() if stats["qty"] < 2]

    avg_txn_region = {
        region: data["revenue"] / data["count"]
        for region, data in region_sales.items()
    }

    # ---------- API ENRICHMENT ----------
    total_products = len(enriched_transactions)
    enriched_count = sum(1 for tx in enriched_transactions if tx["API_Match"])
    success_rate = (enriched_count / total_products * 100) if total_products else 0

    failed_products = list({tx["ProductName"] for tx in enriched_transactions if not tx["API_Match"]})

    # ---------- WRITE REPORT ----------
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(output_file, "w", encoding="utf-8") as f:

        f.write("="*50 + "\n")
        f.write("       SALES ANALYTICS REPORT\n")
        f.write(f"     Generated: {now}\n")
        f.write(f"     Records Processed: {total_transactions}\n")
        f.write("="*50 + "\n\n")

        # OVERALL SUMMARY
        f.write("OVERALL SUMMARY\n")
        f.write("-"*50 + "\n")
        f.write(f"Total Revenue:        ₹{total_revenue:,.2f}\n")
        f.write(f"Total Transactions:   {total_transactions}\n")
        f.write(f"Average Order Value:  ₹{avg_order_value:,.2f}\n")
        f.write(f"Date Range:           {date_range}\n\n")

        # REGION PERFORMANCE
        f.write("REGION-WISE PERFORMANCE\n")
        f.write("-"*50 + "\n")
        f.write("Region      Sales        % of Total   Transactions\n")

        for region, data in region_sorted:
            percent = (data["revenue"] / total_revenue * 100) if total_revenue else 0
            f.write(f"{region:<12} ₹{data['revenue']:>10,.0f}   {percent:>6.2f}%        {data['count']}\n")

        f.write("\n")

        # TOP PRODUCTS
        f.write("TOP 5 PRODUCTS\n")
        f.write("-"*50 + "\n")
        f.write("Rank  Product         Quantity   Revenue\n")

        for i, (name, stats) in enumerate(top_products, start=1):
            f.write(f"{i:<5} {name:<15} {stats['qty']:<10} ₹{stats['revenue']:,.0f}\n")

        f.write("\n")

        # TOP CUSTOMERS
        f.write("TOP 5 CUSTOMERS\n")
        f.write("-"*50 + "\n")
        f.write("Rank  CustomerID   Total Spent   Orders\n")

        for i, (cid, stats) in enumerate(top_customers, start=1):
            f.write(f"{i:<5} {cid:<12} ₹{stats['spent']:,.0f}     {stats['orders']}\n")

        f.write("\n")

        # DAILY TREND
        f.write("DAILY SALES TREND\n")
        f.write("-"*50 + "\n")
        f.write("Date         Revenue     Transactions   Unique Customers\n")

        for date, data in daily_sorted:
            f.write(f"{date}   ₹{data['revenue']:>8,.0f}        {data['transactions']:<5}           {len(data['customers'])}\n")

        f.write("\n")

        # PRODUCT PERFORMANCE
        f.write("PRODUCT PERFORMANCE ANALYSIS\n")
        f.write("-"*50 + "\n")
        f.write(f"Best Selling Day: {best_selling_day}\n")
        f.write(f"Low Performing Products: {', '.join(low_products) if low_products else 'None'}\n")
        f.write("Average Transaction Value per Region:\n")

        for region, value in avg_txn_region.items():
            f.write(f"  {region}: ₹{value:,.2f}\n")

        f.write("\n")

        # API ENRICHMENT
        f.write("API ENRICHMENT SUMMARY\n")
        f.write("-"*50 + "\n")
        f.write(f"Total Products Processed: {total_products}\n")
        f.write(f"Successfully Enriched:    {enriched_count}\n")
        f.write(f"Success Rate:             {success_rate:.2f}%\n")
        f.write("Products Not Enriched:    ")
        f.write(", ".join(failed_products) if failed_products else "None")
        f.write("\n\n")

    print("Sales report generated successfully!")

