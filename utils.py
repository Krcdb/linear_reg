import csv

def normalize(data):
    min_val = min(data)
    max_val = max(data)
    return [(x - min_val) / (max_val - min_val) for x in data]

def get_data(input):
    x = []
    y = []

    with open(input, 'r') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            x.append(float(row[0]))
            y.append(float(row[1]))

    return (x, y)