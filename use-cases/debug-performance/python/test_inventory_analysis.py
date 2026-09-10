import random
import unittest

from inventory_analysis import find_product_combinations


def brute_force_combinations(products, target_price, price_margin):
    matches = []
    for left_index in range(len(products)):
        for right_index in range(left_index + 1, len(products)):
            combined_price = products[left_index]['price'] + products[right_index]['price']
            if abs(combined_price - target_price) <= price_margin:
                matches.append((
                    frozenset((products[left_index]['id'], products[right_index]['id'])),
                    combined_price,
                ))
    return sorted(matches, key=lambda match: (abs(target_price - match[1]), sorted(match[0])))


class FindProductCombinationsTests(unittest.TestCase):
    def test_matches_brute_force_oracle(self):
        random_generator = random.Random(7)

        for size in range(2, 15):
            for _ in range(20):
                products = [
                    {'id': index, 'name': f'Product {index}', 'price': random_generator.randint(1, 30)}
                    for index in range(size)
                ]
                target_price = random_generator.randint(2, 60)
                price_margin = random_generator.randint(0, 5)

                actual = [
                    (
                        frozenset((pair['product1']['id'], pair['product2']['id'])),
                        pair['combined_price'],
                    )
                    for pair in find_product_combinations(products, target_price, price_margin)
                ]

                self.assertEqual(
                    sorted(actual, key=lambda match: (abs(target_price - match[1]), sorted(match[0]))),
                    brute_force_combinations(products, target_price, price_margin),
                )

    def test_does_not_pair_a_product_with_itself(self):
        products = [{'id': 1, 'name': 'Only product', 'price': 10}]

        self.assertEqual(find_product_combinations(products, 20), [])


if __name__ == '__main__':
    unittest.main()