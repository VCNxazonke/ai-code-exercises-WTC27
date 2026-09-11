"""
Activity 1: Idiomatic Code Transformation
Side-by-side comparison of non-idiomatic vs. idiomatic Python code.
"""

# ==============================================================================
# ORIGINAL VERSION (Non-Idiomatic)
# ==============================================================================
def process_user_scores_original(user_data):
    result = {}
    keys = user_data.keys()
    for key in keys:
        scores = user_data[key]
        total = 0
        count = 0
        for score in scores:
            if score >= 0:
                total = total + score
                count = count + 1
        if count > 0:
            avg = total / count
            result[key] = avg
        else:
            result[key] = 0.0
    return result


# ==============================================================================
# IMPROVED VERSION (Idiomatic Python)
# ==============================================================================
def process_user_scores_idiomatic(user_data: dict[str, list[float]]) -> dict[str, float]:
    """
    Processes user test scores by calculating the mean of non-negative scores.
    Demonstrates idiomatic Python features: dict comprehension, list comprehensions,
    dictionary `.items()` iteration, and built-in `sum()` and `len()`.
    """
    def calculate_valid_mean(scores: list[float]) -> float:
        valid_scores = [s for s in scores if s >= 0]
        return sum(valid_scores) / len(valid_scores) if valid_scores else 0.0

    return {user: calculate_valid_mean(scores) for user, scores in user_data.items()}


# ==============================================================================
# DEMONSTRATION & VERIFICATION
# ==============================================================================
if __name__ == "__main__":
    sample_data = {
        "alice": [85.0, 90.0, 95.0, -5.0],
        "bob": [-10.0, -15.0],
        "charlie": [100.0, 90.0]
    }
    
    print("Original output: ", process_user_scores_original(sample_data))
    print("Idiomatic output:", process_user_scores_idiomatic(sample_data))
    assert process_user_scores_original(sample_data) == process_user_scores_idiomatic(sample_data)
    print("Verification passed successfully.")
