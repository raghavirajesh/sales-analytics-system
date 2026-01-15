from utils.file_handler import read_sales_data, parse_transactions
from utils.file_handler import validate_and_filter
from utils.data_processor import ( calculate_total_revenue, 
    region_wise_sales, 
    top_selling_products, 
    customer_analysis, 
    daily_sales_trend,
    low_performing_products
)
from utils.api_handler import (fetch_all_products, 
    create_product_mapping, 
    enrich_sales_data, 
    save_enriched_data)

from report_generator import generate_sales_report

from datetime import datetime
import sys


def main():
    """
    Main execution function
    """

    try:
        # 1. Print welcome message
        print("=" * 40)
        print("SALES ANALYTICS SYSTEM")
        print("=" * 40)

        # 2. Read sales data file (handle encoding)
        print("\n[1/10] Reading sales data...")
        raw_data = read_sales_data("data/sales_data.txt")
        print(f"✓ Successfully read {len(raw_data)} transactions")

        # 3. Parse and clean transactions
        print("\n[2/10] Parsing and cleaning data...")
        transactions = parse_transactions(raw_data)
        print(f"✓ Parsed {len(transactions)} records")

        # 4. Display filter options to user
        print("\n[3/10] Filter Options Available:")
        regions = sorted(set(list({t["Region"] for t in transactions if t["Region"].strip()})))
        amounts = [ t["Quantity"] * t["UnitPrice"] for t in transactions if t["Quantity"] > 0 and t["UnitPrice"] > 0]

        #amounts = [t["Quantity"] * t["UnitPrice"] for t in transactions]

        print("Regions:", ", ".join(regions))
        print(f"Amount Range: ₹{min(amounts)} - ₹{max(amounts)}")

        choice = input("\nDo you want to filter data? (y/n): ").strip().lower()

        # 5. If yes, ask for filter criteria and apply
        if choice == "y":
            region_filter = input("Enter region (or press Enter to skip): ").strip()
            min_amount = input("Enter minimum amount (or press Enter to skip): ").strip()
            max_amount = input("Enter maximum amount (or press Enter to skip): ").strip()

            region_filter = region_filter if region_filter else None
            min_amount = float(min_amount) if min_amount else None
            max_amount = float(max_amount) if max_amount else None

            valid_transactions, invalid_count, filter_summary = validate_and_filter(
                transactions, region_filter, min_amount, max_amount
            )
        else:
            valid_transactions, invalid_count, filter_summary = validate_and_filter(transactions)

        # 6. Validate transactions
        # (Validation already handled inside validate_and_filter)

        
        # 7. Display validation summary
        print("\n[4/10] Validating transactions...")
        print(f"✓ Valid: {len(valid_transactions)} | Invalid: {invalid_count}")
    

        # 8. Perform all data analyses (call all functions from Part 2)
        print("\n[5/10] Analyzing sales data...")
        total_revenue = calculate_total_revenue(valid_transactions)
        region_perf = region_wise_sales(valid_transactions)
        top_products = top_selling_products(valid_transactions)
        top_cust = customer_analysis(valid_transactions)
        daily_trend = daily_sales_trend(valid_transactions)
        prod_perf = low_performing_products(valid_transactions)
        print("✓ Analysis complete")

        # 9. Fetch products from API
        print("\n[6/10] Fetching product data from API...")
        api_products = fetch_all_products()
        print(f"✓ Fetched {len(api_products)} products")

        # 10. Enrich sales data with API info
        print("\n[7/10] Enriching sales data...")
        product_mapping = create_product_mapping(api_products)
        enriched_transactions = enrich_sales_data(valid_transactions, product_mapping)

        enriched_success = sum(1 for t in enriched_transactions if t["API_Match"])
        total_valid = len(valid_transactions)
        success_rate = (enriched_success / total_valid) * 100 if total_valid else 0
        print(f"✓ Enriched {enriched_success}/{total_valid} transactions ({success_rate:.1f}%)")

        # 11. Save enriched data to file
        print("\n[8/10] Saving enriched data...")
        save_enriched_data(enriched_transactions)
        print("✓ Saved to: data/enriched_sales_data.txt")

        # 12. Generate comprehensive report
        print("\n[9/10] Generating comprehensive report...")
        generate_sales_report(valid_transactions, enriched_transactions)
        print("✓ Report saved to: output/sales_report.txt")

        # 13. Print success message with file locations
        print("\n[10/10] Process Complete!")
        print("=" * 40)
        print("Enriched Data File: data/enriched_sales_data.txt")
        print("Sales Report File: output/sales_report.txt")
        print("=" * 40)

    except Exception as e:
        print("\n Something went wrong!")
        print("Error:", str(e))
        print("Please check input files and function definitions.")
        sys.exit(1)


if __name__ == "__main__":
    main()
