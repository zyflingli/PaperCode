filenames = []
for i in range (1,31) :
    filenames.append('House A/Day_' + str(i) + '.txt')


with open('House A/ARAS_Dataset.txt', 'w') as outfile:
    for fname in filenames:
        with open(fname) as infile:
            for line in infile:
                outfile.write(line)
                
filenames = []
for i in range (1,31) :
    filenames.append('House B/Day_' + str(i) + '.txt')


with open('House B/ARAS_Dataset.txt', 'w') as outfile:
    for fname in filenames:
        with open(fname) as infile:
            for line in infile:
                outfile.write(line)