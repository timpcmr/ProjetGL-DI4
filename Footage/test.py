import csv

with open("15.csv", 'r') as file:
	metadata = dict()
	csvreader = csv.reader(file, delimiter = ';')
	rows_list = list(csvreader)
        
	for i in range(len(rows_list[0])):
		metadata[rows_list[0][i]] = rows_list[1][i]
	print(metadata)