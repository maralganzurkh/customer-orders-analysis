#!/usr/bin/env python3
"""
Analyzing Customer Orders Using Python
--------------------------------------
Ready-to-run script that:
- Builds a demo dataset of customer orders
- Stores data using lists, tuples, dictionaries, and sets
- Classifies customers (High/Moderate/Low) by total spend
- Computes revenue per category
- Finds cross-category buyers and electronics buyers
- Outputs CSVs, a chart (PNG), and a Markdown report in ./outputs

Optional: You can adapt the "orders" list below or extend the script to load from a CSV.
"""

from collections import defaultdict
import os
from io import StringIO
import math

import pandas as pd
import matplotlib.pyplot as plt


def build_demo_data():
    # List of customer names
    customers = ["Alice", "Bob", "Charlie", "Diana", "Ethan", "Farah", "Grace"]

    # Orders as tuples: (customer_name, product, price, category)
    orders = [
        ("Alice",   "Smartphone X",     899.00, "Electronics"),
        ("Alice",   "Phone Case",        29.00, "Electronics"),
        ("Bob",     "Jeans",             69.00, "Clothing"),
        ("Bob",     "T-shirt",           25.00, "Clothing"),
        ("Charlie", "Air Fryer",        149.00, "Home Essentials"),
        ("Charlie", "Vacuum Cleaner",   199.00, "Home Essentials"),
        ("Diana",   "Laptop Pro 14",   1799.00, "Electronics"),
        ("Diana",   "Wireless Mouse",    39.00, "Electronics"),
        ("Ethan",   "Blender",           89.00, "Home Essentials"),
        ("Ethan",   "Hoodie",            59.00, "Clothing"),
        ("Farah",   "Earbuds",           99.00, "Electronics"),
        ("Farah",   "Yoga Mat",          35.00, "Home Essentials"),
        ("Grace",   "Dress",             89.00, "Clothing"),
        ("Grace",   "Smartwatch",       299.00, "Electronics"),
    ]

    return customers, orders


def classify_spender(total: float) -> str:
    if total > 100:
        return "High-value"
    elif 50 <= total <= 100:
        return "Moderate"
    else:
        return "Low-value"


def analyze(customers, orders):
    # Dictionary: customer -> list of ordered products dicts
    customer_orders = defaultdict(list)
    for cname, product, price, category in orders:
        customer_orders[cname].append({"product": product, "price": float(price), "category": category})

    # Dictionary: product -> category
    product_to_category = {prod: cat for _, prod, _, cat in orders}

    # Set of unique product categories
    categories = {cat for _, _, _, cat in orders}

    # Totals and classes
    totals = {}
    classes = {}
    for cname in customers:
        spend = sum(item["price"] for item in customer_orders.get(cname, []))
        totals[cname] = round(spend, 2)
        classes[cname] = classify_spender(spend)

    # Revenue per category
    revenue_per_category = defaultdict(float)
    for _, _, price, cat in orders:
        revenue_per_category[cat] += float(price)
    revenue_per_category = {k: round(v, 2) for k, v in revenue_per_category.items()}

    # Unique products
    unique_products = {prod for _, prod, _, _ in orders}

    # Electronics customers (list comprehension + set)
    electronics_customers = sorted({c for c, p, _, cat in orders if cat == "Electronics"})

    # Top 3 spenders
    top_spenders = sorted(totals.items(), key=lambda kv: kv[1], reverse=True)[:3]

    # Customer summary rows
    summary_rows = []
    for cname in customers:
        purchases = customer_orders.get(cname, [])
        cats = sorted({p["category"] for p in purchases})
        summary_rows.append({
            "Customer": cname,
            "Total Spend ($)": totals[cname],
            "Classification": classes[cname],
            "Categories Purchased": ", ".join(cats) if cats else "-",
            "Item Count": len(purchases),
        })
    summary_df = pd.DataFrame(summary_rows).sort_values(by=["Total Spend ($)"], ascending=False)

    # Multi-category & both electronics+clothing
    customer_to_categories = {c: {p["category"] for p in plist} for c, plist in customer_orders.items()}
    multi_category_customers = sorted([c for c, cats in customer_to_categories.items() if len(cats) > 1])
    electronics_buyers = {c for c, cats in customer_to_categories.items() if "Electronics" in cats}
    clothing_buyers = {c for c, cats in customer_to_categories.items() if "Clothing" in cats}
    both_electronics_and_clothing = sorted(list(electronics_buyers & clothing_buyers))

    # DataFrames to output
    orders_df = pd.DataFrame(orders, columns=["Customer", "Product", "Price", "Category"])
    rev_cat_df = pd.DataFrame(
        [{"Category": k, "Revenue ($)": v} for k, v in revenue_per_category.items()]
    ).sort_values(by="Revenue ($)", ascending=False)

    # Pack results
    results = {
        "orders_df": orders_df,
        "summary_df": summary_df,
        "rev_cat_df": rev_cat_df,
        "categories": categories,
        "unique_products": unique_products,
        "electronics_customers": electronics_customers,
        "multi_category_customers": multi_category_customers,
        "both_electronics_and_clothing": both_electronics_and_clothing,
        "top_spenders": top_spenders,
    }
    return results


def save_outputs(results, out_dir="outputs"):
    os.makedirs(out_dir, exist_ok=True)

    # Save CSVs
    results["orders_df"].to_csv(os.path.join(out_dir, "orders.csv"), index=False)
    results["summary_df"].to_csv(os.path.join(out_dir, "customer_summary.csv"), index=False)
    results["rev_cat_df"].to_csv(os.path.join(out_dir, "revenue_by_category.csv"), index=False)

    # Chart
    plt.figure()
    plt.bar(results["rev_cat_df"]["Category"], results["rev_cat_df"]["Revenue ($)"])
    plt.title("Revenue by Category")
    plt.xlabel("Category")
    plt.ylabel("Revenue ($)")
    plt.xticks(rotation=20)
    chart_path = os.path.join(out_dir, "revenue_by_category.png")
    plt.tight_layout()
    plt.savefig(chart_path)
    plt.close()

    # Markdown report
    report = StringIO()
    report.write("# Customer Orders Analysis – Report\n\n")

    customers_count = results["orders_df"]["Customer"].nunique()
    orders_count = len(results["orders_df"])
    unique_products_count = len(results["unique_products"])
    categories_list = ", ".join(sorted(results["categories"]))

    report.write("## Overview\n")
    report.write("Demo dataset analysed using Python lists, tuples, dictionaries, sets, loops and conditionals. ")
    report.write("Outputs include spend-based customer classifications, category revenue, and cross-category behaviours.\n\n")

    report.write("## Key Metrics\n")
    report.write(f"- Unique customers: **{customers_count}**\n")
    report.write(f"- Total orders: **{orders_count}**\n")
    report.write(f"- Unique products: **{unique_products_count}**\n")
    report.write(f"- Categories: **{categories_list}**\n\n")

    report.write("## Customer Classification (by total spend)\n")
    report.write("- **High-value**: total > $100\n- **Moderate**: $50–$100\n- **Low-value**: < $50\n\n")

    report.write("### Top 3 Spenders\n")
    for i, (name, amt) in enumerate(results["top_spenders"], start=1):
        report.write(f"{i}. **{name}** — ${amt:.2f}\n")
    report.write("\n")

    report.write("### Customers who purchased Electronics\n")
    report.write(", ".join(results["electronics_customers"]) + "\n\n")

    report.write("### Customers purchasing from multiple categories\n")
    report.write(", ".join(results["multi_category_customers"]) if results["multi_category_customers"] else "None")
    report.write("\n\n")

    report.write("### Customers who bought both Electronics and Clothing\n")
    report.write(", ".join(results["both_electronics_and_clothing"]) if results["both_electronics_and_clothing"] else "None")
    report.write("\n\n")

    report.write("## Revenue by Category ($)\n")
    for _, row in results["rev_cat_df"].iterrows():
        report.write(f"- {row['Category']}: ${row['Revenue ($)']:.2f}\n")
    report.write("\n")

    report.write("> Chart saved alongside this report: `revenue_by_category.png`\n")

    report_path = os.path.join(out_dir, "customer_orders_report.md")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report.getvalue())

    return {
        "report_path": report_path,
        "chart_path": chart_path,
        "orders_csv": os.path.join(out_dir, "orders.csv"),
        "summary_csv": os.path.join(out_dir, "customer_summary.csv"),
        "revenue_csv": os.path.join(out_dir, "revenue_by_category.csv"),
    }


def main():
    customers, orders = build_demo_data()
    results = analyze(customers, orders)
    paths = save_outputs(results, out_dir="outputs")

    print("Analysis complete. Files saved to ./outputs")
    for k, v in paths.items():
        print(f"- {k}: {v}")


if __name__ == "__main__":
    main()
