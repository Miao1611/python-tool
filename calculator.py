def calculate_statistics(numbers):
    count = len(numbers)
    total = sum(numbers)
    average = total / count
    minimum = min(numbers)
    maximum = max(numbers)

    result = {
        "count": count,
        "sum": total,
        "average": average,
        "min": minimum,
        "max": maximum
    }

    return result


if __name__ == "__main__":
    test_numbers = [12, 18, 25, 31, 44]

    result = calculate_statistics(test_numbers)

    print(result)