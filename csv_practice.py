# ISM2411 Lab 12 — Read a Sales CSV, Write a Cleaned Report
# Author: Jimmy Reyes
#
# Reflection 1: How does this ETL pipeline compare to Excel?
# In Excel I would filter, add a formula column and copy the results to a new sheet by hand, and repeat every step whenever the data changed.Python does it all in one run, works the same on 10 rows or a million, and keeps a record of exactly what was done. Excel is still better for quickly looking at data or letting non-coders edit it.

# Reflection 2: A business process that benefits from an append-mode log
# A store could log its end-of-day sales total every evening, adding one line per day to the same file. Append mode is right because it keeps every earlier day, while "w" mode would erase the history each run.

import csv
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
SALES_FILE = BASE_DIR / "data" / "sales.csv"
CLEANED_FILE = BASE_DIR / "data" / "cleaned.csv"
LOG_FILE = BASE_DIR / "data" / "run_log.txt"

print("--- Exercise 1 ---")

with open(SALES_FILE, "r") as f:
    print(f"Opened {SALES_FILE}.")

print("--- Exercise 2 ---")

with open(SALES_FILE, "r") as f:
    reader = csv.reader(f)
    for row in reader:
        print(row)

print("--- Exercise 3 ---")

with open(SALES_FILE, "r") as f:
    reader = csv.reader(f)
    header = next(reader)
    print(f"Header: {header}")
    for row in reader:
        print(row)

print("--- Exercise 4 ---")
total_revenue = 0
with open(SALES_FILE, "r") as f:
    reader = csv.reader(f)
    next(reader)
    for row in reader:
        product, price_str, qty_str = row
        price = float(price_str)
        quantity = int(qty_str)
        total = price * quantity
        total_revenue += total
        print(f"{product}: {quantity} units x ${price:.2f} = ${total:.2f}")

print(f"Total revenue: ${total_revenue:.2f}")

print("--- Exercise 5 ---")

high_value = []
rows_read = 0

with open(SALES_FILE, "r") as f:
    reader = csv.reader(f)
    next(reader)  # Skip header
    for row in reader:
        rows_read += 1
        product, price_str, qty_str = row
        price = float(price_str)
        quantity = int(qty_str)
        total = price * quantity
        if total > 100:
            high_value.append([product, f"{price:.2f}", quantity, f"{total:.2f}"])

with open(CLEANED_FILE, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Product", "Price", "Qty", "Total"])
    for row in high_value:
        writer.writerow(row)

print(f"Wrote {len(high_value)} of {rows_read} rows to {CLEANED_FILE}.")

print("--- Exercise 6 ---")

dict_total = 0
with open(SALES_FILE, "r") as f:
    reader = csv.DictReader(f)
    for row in reader:
        price = float(row["price"])
        quantity = int(row["quantity"])
        total = price * quantity
        dict_total += total
        print(f"{row['product']}: {quantity} units x ${price:.2f} = ${total:.2f}")

print(f"Total revenue: ${dict_total:.2f}")
# csv.reader is fine for simple files where the column order never changes.
# DictReader is clearer (row["price"] vs row[1]) and still works if columns are reordered.

print("--- Exercise 7 ---")
summary = {}

with open(SALES_FILE, "r") as f:
    reader = csv.DictReader(f)
    for row in reader:
        product = row["product"]
        total = float(row["price"]) * int(row["quantity"])
        summary[product] = summary.get(product, 0) + total
for product in sorted(summary):
    print(f"{product}: ${summary[product]:.2f}")

print("--- Exercise 8 ---")
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
with open(LOG_FILE, "a") as f:
    f.write(f"{timestamp} total revenue: ${total_revenue:.2f}\n")

entries = 0
with open(LOG_FILE, "r") as f:
    for line in f:
        entries += 1
        print(line.strip())

print(f"Log entries so far: {entries}")