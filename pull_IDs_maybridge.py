"""
Looks for high penalty ZINC molecules and outputs them into a new file.

-Luke Warrensford 1/18
"""

with open('maybhit_all.str') as f_obj:
    lines = f_obj.readlines()
    
with open('high_penalties.txt', 'a') as log_file:
    log_file.write("ZINC-ID" + "\t\tCategory" + "\tAtoms" + "\t\tPenalty (>50)")
    log_file.write("\n------------------------------------------------------------")

def pull_values():
    """Identifies high penalties and writes them to log file."""
    try:
        if float(line[-1]) > 0.0:
            if len(line) == 12:
                # Identifying line length allows category ID.
                print("High penalty detected for " + line[5] + 
                    "\tCategory: BOND")
                with open('high_penalties.txt', 'a') as log_file:
                    log_file.write("\n")
                    log_file.write("\t\tBOND" + ("\t\t") + 
                        line[8][0] + " " + line[9][0] + "\t\t" + line[-1])
            elif len(line) == 14:
                print("High penalty detected for " + line[6] + 
                    "\tCategory: ANGLE")
                with open('high_penalties.txt', 'a') as log_file:
                    log_file.write("\n")
                    log_file.write("\t\tANGLE" + ("\t\t") + 
                        line[9][0] + " " + line[10][0] + " " + line[11][0]
                        + "\t\t" + line[-1])
            elif len(line) == 16:
                print("High penalty detected for " + line[8] + 
                    "\tCategory: ANGLE")
                with open('high_penalties.txt', 'a') as log_file:
                    log_file.write("\n")
                    log_file.write("\t\tANGLE" + ("\t\t") + 
                        line[11][0] + " " + line[12][0] + " " + line[13][0]
                        + "\t\t" + line[-1])
            elif len(line) == 17 and str(line[5]) != '0':
                print("High penalty detected for " + line[8] + 
                    "\tCategory: DIHEDRAL")
                with open('high_penalties.txt', 'a') as log_file:
                    log_file.write("\n")
                    log_file.write("\t\tDIHEDRAL" + ("\t") + 
                        line[11][0] + " " + line[12][0] + " " + line[13][0] +
                        " " + line[14][0] + "\t\t" + line[-1])
            elif len(line) == 17 and str(line[5]) == '0':
                print("High penalty detected for " + line[8] + 
                    "\tCategory: IMPROPER")
                with open('high_penalties.txt', 'a') as log_file:
                    log_file.write("\n")
                    log_file.write("\t\tIMPROPER" + ("\t") + 
                        line[11][0] + " " + line[12][0] + " " + 
                        line[13][0] + " " + line[14][0] + "\t\t" + line[-1])
            elif len(line) == 6:
                print("High penalty detected for " + zinc_id + 
                    "\tCategory: CHARGE")
                with open('high_penalties.txt', 'a') as log_file:
                    log_file.write("\n")
                    log_file.write("\t\tCHARGE" + ("\t\t") + line[1]
                    + "\t\t" + line[-1])
        else:
            print("OK")
    except ValueError:
        pass

for i in range(0, len(lines)):
    lines[i] = (str(lines[i]))
    line = lines[i].split()
    if len(line) != 0 and line[0] == "RESI":
        zinc_id = line[1]
        with open('high_penalties.txt', 'a') as log_file:
            log_file.write("\n" + zinc_id)
    elif len(line) != 0 and line[0] != 'RETURN':
        pull_values()
    elif len(line) != 0 and line[0] == 'RETURN':
        with open('high_penalties.txt', 'a') as log_file:
            log_file.write("\n------------------------------------------------------------")
