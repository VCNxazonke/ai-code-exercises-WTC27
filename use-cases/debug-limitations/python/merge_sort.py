"""
Merge Sort Implementation with Verified Fix.

Scenario: A sorting function with a subtle bug.
Bug Diagnosis: In the left remainder loop, incrementing `j` instead of `i` causes an infinite loop.
Fix: Correct pointer increment to `i += 1`.
"""

def merge_sort(arr):
    """
    Sorts a list of comparable elements in ascending order using Merge Sort.
    
    Args:
        arr (list): List of elements to sort.
        
    Returns:
        list: A new sorted list containing all elements from arr.
    """
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])

    return merge(left, right)


def merge(left, right):
    """
    Merges two sorted lists into a single sorted list.
    """
    result = []
    i = 0
    j = 0

    # Main comparison loop
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    # Fixed left remainder loop: increment i (previously bugged with j += 1)
    while i < len(left):
        result.append(left[i])
        i += 1

    # Right remainder loop
    while j < len(right):
        result.append(right[j])
        j += 1

    return result


if __name__ == "__main__":
    sample = [38, 27, 43, 3, 9, 82, 10]
    sorted_sample = merge_sort(sample)
    print(f"Original: {sample}")
    print(f"Sorted:   {sorted_sample}")
