import random
import pandas as pd
import os
import sys


def read_bingo_points(file_path):
    # Reading the content of the file
    with open(file_path, 'r') as file:
        file_content = file.readlines()

    # Extracting the points from the file content
    points = [line.strip() for line in file_content if line.strip()]

    cleaned_points = []

    for line in points:
        # Extract the actual text between the '|' symbols, if present
        if '|' in line:
            start = line.find('|') + 1
            end = line.rfind('|')
            point = line[start:end].strip()
            cleaned_points.append(point)

    combined_points = []
    for i in range(0, len(cleaned_points), 2):
        # Combine two lines into one point, handling the case where the last line might be alone
        point = cleaned_points[i]
        if i + 1 < len(cleaned_points):
            point += " " + cleaned_points[i + 1]
        combined_points.append(point)
    return combined_points


def generate_bingo_card(card_number, points):
    # Shuffle the points randomly
    random.shuffle(points)

    # Create a 5x5 grid (5 rows, 5 columns) for the bingo card
    grid = [points[i:i + 5] for i in range(0, len(points), 5)]

    # Create a DataFrame from the grid
    df = pd.DataFrame(grid)

    # Determine the output file name based on card number
    filename = f"bingo_card_{card_number}.csv"

    # Check if the file already exists and increment the card number if necessary
    while os.path.exists(filename):
        card_number += 1
        filename = f"bingo_card_{card_number}.csv"

    # Save the DataFrame to a CSV file
    df.to_csv(filename, index=False)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python bingo_generator.py <file_path> <number_of_cards>")
        sys.exit(1)

    try:
        file_path = sys.argv[1]
        num_cards = int(sys.argv[2])
        combined_points = read_bingo_points(file_path)
        for card_number in range(1, num_cards + 1):
            generate_bingo_card(card_number, combined_points)
            print(f"Bingo card {card_number} generated successfully.")
    except ValueError:
        print("Please provide a valid number of bingo cards.")
        sys.exit(1)
