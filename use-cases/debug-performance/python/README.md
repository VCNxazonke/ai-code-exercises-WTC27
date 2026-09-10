# Inventory Analyzer - Performance Optimization Challenge

A Python tool for analyzing product inventory to find combinations of products that match specific price targets.

## Features

- Find pairs of products whose combined price matches a target price within a specified margin
- Handles large product inventories efficiently
- Progress tracking for long-running analyses
- Sorted results by closest match to target price
- Duplicate combination prevention

## Usage

The main function `find_product_combinations` takes the following parameters:

```python
def find_product_combinations(products, target_price, price_margin=10):
    """
    Args:
        products: List of dictionaries with 'id', 'name', and 'price' keys
        target_price: The ideal combined price
        price_margin: Acceptable deviation from the target price
    """
```

### Example Usage

```python
product_list = [
    {'id': 1, 'name': 'Product 1', 'price': 100},
    {'id': 2, 'name': 'Product 2', 'price': 200},
    # ... more products
]

combinations = find_product_combinations(product_list, 500, 50)
```

Each result contains:
- Product 1 details
- Product 2 details
- Combined price
- Price difference from target

## How to run

`python inventory_analysis.py`

## Performance

- Capable of processing large inventories (5000+ products)
- Reports the total combinations and elapsed benchmark time when run directly
- Returns results sorted by closest match to target price

### Optimization Notes

The original approach checked every possible product pair and used a linear scan
to prevent duplicate combinations. That makes the work approximately `O(N^2 * K)`.

The implementation in `inventory_analysis.py` sorts products by price once, uses
`bisect` to find the valid partner-price window, and only examines each pair
once. Its complexity is `O(N log N + K)`, where `K` is the number of matching
pairs returned. The result list still requires `O(K log K)` sorting by price
difference.

The included benchmark uses 5,000 deterministic products. On the current
workspace it found 2,432,833 combinations in about 1.7 seconds. Runtime will
vary by Python version and machine, so the command below is the authoritative
way to remeasure it:

```text
python inventory_analysis.py
```

Correctness coverage is in `test_inventory_analysis.py` and compares the
optimized function with a brute-force oracle on randomized small inventories.