import csv
import os
import sys

def normalize(data):
    min_val = min(data)
    max_val = max(data)
    return [(x - min_val) / (max_val - min_val) for x in data]

def get_thetas(input):
    if not os.path.isfile(input):
        print(f"Error: File '{input}' does not exist.")
        sys.exit(1)

    try:
        with open(input, 'r') as file:
            lines = file.readlines()
            if len(lines) < 2:
                print(f"Error: File '{input}' must contain at least two lines (theta0 and theta1).")
                sys.exit(1)
            t0 = float(lines[0].strip())
            t1 = float(lines[1].strip())
    except Exception as e:
        print(f"Error reading file '{input}': {e}")
        sys.exit(1)

    return (t0, t1)

def get_data(input):
    x = []
    y = []

    if not os.path.isfile(input):
        print(f"Error: File '{input}' does not exist.")
        sys.exit(1)

    try:
        with open(input, 'r') as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                x.append(float(row[0]))
                y.append(float(row[1]))
    except Exception as e:
        print(f"Error reading file '{input}': {e}")
        sys.exit(1)

    return (x, y)