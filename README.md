# Sales Analytics System

A Python-based Sales Analytics System that processes sales transaction data, performs validation and analysis, fetches product details from an external API, enriches transactions, and generates a final sales report.

---

## 📂 Project Structure

sales-analytics-system/
  ├── README.md
  ├── main.py
  ├── utils/
  │   ├── file_handler.py
  │   ├── data_processor.py
  │   └── api_handler.py
  ├── data/
  │   └── sales_data.txt (provided)
  ├── output/
  └── requirements.txt

---

## Setup Instructions

### 1. Clone the Repository
git clone <https://github.com/raghavirajesh>
cd sales-analytics-system


### 2. Install Required Libraries

This installs the required dependency:
- requests

---

## How to Run the Program

Run the following command from the project root folder:


---

## Expected Console Flow

When you run `main.py`, the program will:

1. Display a welcome message  
2. Read the sales data file from `data/sales_data.txt`  
3. Parse and clean transactions  
4. Show available regions and transaction amount range  
5. Ask if you want to apply filters  
6. Validate transactions  
7. Perform sales analysis  
8. Fetch product details from API  
9. Enrich sales data  
10. Save enriched data to `data/enriched_sales_data.txt`  
11. Generate report at `output/sales_report.txt`  
12. Display success message

---

## Generated Output Files

After successful execution:

- `data/enriched_sales_data.txt`  
- `output/sales_report.txt`

---

## Error Handling

- Handles file reading errors  
- Handles parsing errors  
- Handles API request failures  
- Prevents program crashes with user-friendly messages

---

## Requirements

- Python 3.14  
- requests library

---



