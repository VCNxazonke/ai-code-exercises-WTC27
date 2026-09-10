"""
Inventory Analysis Module - Performance Optimized Version.

Initial Complexity: O(N^2 * K) due to nested loops over all pairs and linear duplicate check `any()`.
Optimized Complexity: O(N log N + K log K) using price sorting, binary search windowing (`bisect`),
and index offset loops (j starting at i + 1) to eliminate duplicate checks entirely.
"""

import bisect
import random
import time

def find_product_combinations(products, target_price, price_margin=10):
    """
    Find all pairs of products where the combined price is within
    the target_price ± price_margin range.

    Optimized algorithm:
    1. Sort products by price (O(N log N)).
    2. Use `bisect_left` and `bisect_right` to find exact index bounds for valid pairs.
    3. Loop j from max(i + 1, left_idx) to eliminate duplicate pair comparisons (j > i)
       and prevent O(K) linear scanning in `results`.

    Args:
        products: List of dictionaries with 'id', 'name', and 'price' keys
        target_price: The ideal combined price
        price_margin: Acceptable deviation from target price

    Returns:
        List of dictionaries with product pairs and their combined price
    """
    results = []
    min_price = target_price - price_margin
    max_price = target_price + price_margin

    # Sort products by price (O(N log N))
    sorted_products = sorted(products, key=lambda p: p['price'])
    prices = [p['price'] for p in sorted_products]
    n = len(sorted_products)

    for i in range(n):
        p1_price = prices[i]
        
        # Calculate needed price range for product2
        min_p2 = min_price - p1_price
        max_p2 = max_price - p1_price

        if max_p2 < 0:
            break

        # Use binary search to find range of valid product2 indices starting after i
        left_idx = max(i + 1, bisect.bisect_left(prices, min_p2, i + 1, n))
        right_idx = bisect.bisect_right(prices, max_p2, left_idx, n)

        for j in range(left_idx, right_idx):
            product1 = sorted_products[i]
            product2 = sorted_products[j]
            combined_price = p1_price + prices[j]

            pair = {
                'product1': product1,
                'product2': product2,
                'combined_price': combined_price,
                'price_difference': abs(target_price - combined_price)
            }
            results.append(pair)

    # Sort results by price difference from target
    results.sort(key=lambda x: x['price_difference'])
    return results


if __name__ == "__main__":
    random.seed(42)

    print("Generating Product List (5,000 items)...")
    product_list = [
        {
            'id': i,
            'name': f'Product {i}',
            'price': random.randint(5, 500)
        }
        for i in range(5000)
    ]

    # Benchmark Optimized Version on 5,000 products
    print(f"Finding product combinations for {len(product_list)} products...")
    start_time = time.perf_counter()
    combinations = find_product_combinations(product_list, 500, 50)
    end_time = time.perf_counter()

    print(f"Found {len(combinations)} product combinations")
    print(f"Optimized Execution time: {end_time - start_time:.4f} seconds")
