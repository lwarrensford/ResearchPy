"""
Sum the total penalties of each ZINC molecule

-Luke Warrensford 1/18
"""


with open('high_penalties.txt', 'r') as r_obj:
    lines = r_obj.readlines()

penalties = []

for i in range(0, len(lines)):
    lines[i] = (str(lines[i]))
    line = lines[i].split()
    if line[0] == '------------------------------------------------------------':
        same = False
        tot = sum(penalties)
        tot = '%.1f' % tot
        with open('total_penalty.txt', 'a') as out_file:
            out_file.write('\n' + zinc_id + '\t' + str(tot))
        penalties = []
        continue
    elif len(line) == 1:
        zinc_id = line[0]
        same = True
    elif same:
        penalties.append(float(line[-1]))
