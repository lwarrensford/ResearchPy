"""
Pulls structure images from Zinc Database based on text file that ranks
molecules by highest penalties.

-Luke Warrensford 5/18
"""

import urllib.request

with open('badvalues_organized.txt') as f_obj:
    lines = f_obj.readlines()

for i in range(1, 10):
    # Vary endpoint in range to get top # of high penalty molecules.
    urllib.request.urlretrieve("http://zinc.docking.org/img/sub/" + 
        lines[i][4:12] + '.gif', 'structures/ZINC' + lines[i][4:12] + 
        '.jpeg')
    print("Downloading structure " + str(lines[i][4:12]) + "...")
