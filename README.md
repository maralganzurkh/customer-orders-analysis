# Customer Orders Analysis

**Python fundamentals project | SimpliLearn Microsoft AI Engineer Program**

A customer segmentation and revenue analysis script built in Python, demonstrating core data structures including lists, tuples, dictionaries, and sets.

---

## What This Project Does

- Builds a demo dataset of 14 customer orders across 7 customers
- Classifies customers as High-value, Moderate, or Low-value based on total spend
- Computes revenue per product category
- Identifies cross-category buyers and electronics customers
- Finds customers who purchased from both Electronics and Clothing
- Exports CSVs, a bar chart (PNG), and a Markdown report to an `outputs/` folder

## Concepts Demonstrated

| Concept | Where Used |
|---|---|
| Lists | Customer names, order tuples |
| Tuples | Individual order records (customer, product, price, category) |
| Dictionaries | Customer → orders mapping, revenue per category |
| Sets | Unique categories, cross-category buyer identification |
| List comprehensions | Filtering electronics and multi-category customers |
| Functions | `build_demo_data()`, `analyze()`, `classify_spender()`, `save_outputs()` |

## Customer Classification Logic

| Classification | Criteria |
|---|---|
| High-value | Total spend > $100 |
| Moderate | Total spend $50–$100 |
| Low-value | Total spend < $50 |

## How to Run

```bash
# 1. Clone the repo
git clone https://github.com/maralganzurkh/customer-orders-analysis

# 2. Install dependencies
pip install pandas matplotlib

# 3. Run
python analyze_customer_orders.py
```

## Output

Running the script creates an `outputs/` folder containing:
- `orders.csv` — full order records
- `customer_summary.csv` — customer classifications and spend totals
- `revenue_by_category.csv` — revenue breakdown by product category
- `revenue_by_category.png` — bar chart of category revenue
- `customer_orders_report.md` — full Markdown analysis report

---

*Project completed as part of the Microsoft AI Engineer Program — SimpliLearn (2026)*  
*Author: Maral-Od Ganzurkh | [maralganzurkh.com](https://maralganzurkh.com)*
