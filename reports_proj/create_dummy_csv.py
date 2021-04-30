import csv


col_name = ['Transaction id', 'Product', 'Quantity', 'Customer', 'Date']

row_values = [
    ['E200', 'cape', '2', 'Clark', '2021-03-12'],
    ['E300', 'shield', '4', 'Clark', '2021-03-12'],
    ['E500', 'sword', '6', 'Clark', '2021-03-12'],
    ['E600', 'cowl', '7', 'Clark', '2021-03-12'],
    ['E700', 'shield', '2', 'Diana', '2021-03-15'],
    ['E100', 'cowl', '1', 'Bruce', '2021-03-13'],
]

filename = 'Test_CSV.csv'

with open(filename, 'w') as csvfile:
    csvwriter = csv.writer(csvfile)

    csvwriter.writerow(col_name)
    csvwriter.writerows(row_values)