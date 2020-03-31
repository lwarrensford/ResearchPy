def CompareFiles(str_file1,str_file2):
    '''
    This function compares two long string texts and returns their 
    differences as two sequences of unique lines, one list for each.
    '''
    #reading from text file and splitting str_file into lines - delimited by "\n"
    file1_lines = str_file1.split("\n")
    file2_lines = str_file2.split("\n")

    #unique lines to each one, store it in their respective lists
    unique_file1 = []
    unique_file2 = []

    #unique lines in str1
    for line1 in file1_lines:
        if line1 !='':
           if line1 not in file2_lines:
              unique_file1.append(line1)

    #unique lines in str2
    for line2 in file2_lines:
        if line2 != '':
           if line2 not in file1_lines:
              unique_file2.append(line2)

    return unique_file1, unique_file2
    
aa = 'ala'
    
f1 = open(aa + '_charge.txt',"r")
data1 = f1.read()
f1.close()

f3 = open(aa + '.out',"r")
data3 = f3.read()
f3.close()

unique1, unique2 = CompareFiles(data1, data3)

file = open(aa + '_error.out','w')
file.write("-------------------------\n")
file.write("\nONLY in FILE ONE\n")
file.write("\n-------------------------\n")
file.write(str('\n'.join(unique1)))
file.write("\n-------------------------\n")
file.write("\nONLY in FILE TWO\n")
file.write("\n-------------------------\n")
file.write(str('\n'.join(unique2)))
file.close()

line_bits = []
    
for i in range(0, len(unique1)):
    line = unique1[i].split()
    print(line)
    line[i].replace(' ','')
    #for i in range (0, len(line)):
    #    line = line.split(" ")
    #   line_bits.append(line[i])

print(unique1)
