import re
import random
import statistics
from collections import Counter
import psycopg2


with open("python_class_question.html", "r", encoding="utf-8") as file:
    html = file.read()

pattern = re.compile(
    r"\b(?:GREEN|YELLOW|BROWN|BLUE|PINK|ORANGE|CREAM|RED|WHITE|ARSH|BLEW|BLACK)\b",
    re.IGNORECASE
)

colors = [color.upper() for color in pattern.findall(html)]
colors = ["BLUE" if color == "BLEW" else color for color in colors]

color_frequency = Counter(colors)

frequencies = list(color_frequency.values())

mean_frequency = statistics.mean(frequencies)

mean_color = min(
    color_frequency,
    key=lambda color: abs(color_frequency[color] - mean_frequency)
)

most_common_color = color_frequency.most_common(1)[0]

median_frequency = statistics.median(frequencies)

median_colors = [
    color
    for color, frequency in color_frequency.items()
    if frequency == median_frequency
]

variance = statistics.pvariance(frequencies)

red_probability = color_frequency["RED"] / len(colors)

print("Colour frequencies:", color_frequency)
print("Mean colour:", mean_color)
print("Most worn colour:", most_common_color)
print("Median colour:", median_colors)
print("Variance:", variance)
print("Probability of red:", red_probability)


def save_to_postgresql(color_frequency):
    connection = psycopg2.connect(
        host="localhost",
        database="bincom_db",
        user="postgres",
        password="YOUR_PASSWORD",
        port="5432"
    )

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS color_frequency (
            id SERIAL PRIMARY KEY,
            color VARCHAR(50) UNIQUE NOT NULL,
            frequency INTEGER NOT NULL
        )
    """)

    for color, frequency in color_frequency.items():
        cursor.execute("""
            INSERT INTO color_frequency (color, frequency)
            VALUES (%s, %s)
            ON CONFLICT (color)
            DO UPDATE SET frequency = EXCLUDED.frequency
        """, (color, frequency))

    connection.commit()
    cursor.close()
    connection.close()


save_to_postgresql(color_frequency)


def recursive_search(numbers, target, low, high):
    if low > high:
        return -1

    middle = (low + high) // 2

    if numbers[middle] == target:
        return middle
    elif target < numbers[middle]:
        return recursive_search(numbers, target, low, middle - 1)
    else:
        return recursive_search(numbers, target, middle + 1, high)


numbers = [10, 20, 30, 40, 50, 60, 70, 80, 90]

target = int(input("Enter number to search: "))

result = recursive_search(
    numbers,
    target,
    0,
    len(numbers) - 1
)

print(result)


binary_number = ""

for _ in range(4):
    binary_number += random.choice("01")

decimal_number = int(binary_number, 2)

print(binary_number)
print(decimal_number)


def fibonacci_sum(n):
    first = 0
    second = 1
    total = 0

    for _ in range(n):
        total += first
        first, second = second, first + second

    return total


print(fibonacci_sum(50))