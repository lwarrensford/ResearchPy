import pandas as pd
import numpy as np
import glob
import matplotlib.pyplot as plt
from scipy.stats import linregress
import statsmodels.formula.api as smf
import statsmodels.api as sm
from statsmodels.sandbox.regression.predstd import wls_prediction_std


"""
Data analysis script for pose energy analysis

-- Luke Warrensford
"""

poses = []

# Finds the pose numbers we need for later
for filename in glob.glob('energy_pose*.dat'):
    if len(filename) == 16:
        poses.append(str(filename[-5:-4]))
    elif len(filename) == 17:
        poses.append(str(filename[-6:-4]))
    elif len(filename) == 18:
        poses.append(str(filename[-7:-4]))
    else:
        continue

poses = [int(x) for x in poses]
poses.sort()

col = ['pose', 'rmsd', 'rank', 'P_intra', 'L_intra', 'G_solv', 'SASA', 'P_solv', 'P_SASA', 'L_solv', 'L_SASA', 'vdw', 'e_elec']
terms = ['P_intra', 'L_intra', 'G_solv', 'SASA', 'P_solv', 'P_SASA', 'L_solv', 'L_SASA', 'vdw', 'e_elec']

# Makes a blank DataFrame
pm = pd.DataFrame(columns=col)

pose_data = {}

# Looks for all the info in the rms and energy files and stores them in a DataFrame
for pose in poses:
    with open('sorted_final_rmsd.dat') as readOutput:
        oLines = readOutput.readlines()
        for i in range(0, len(oLines)):
            oLines[i] = str(oLines[i])
            oLine = oLines[i].split()
            if oLine[4] == str(pose):
                pose_data = {
                    "pose": int(pose),
                    "rmsd": float(oLine[-1]),
                    "rank": i+1
                }
            else:
                continue
    with open("energy_pose" + str(pose) + ".dat", 'r') as ene:
        lines = ene.readlines()
        for i in range(0, len(lines)):
            lines[i] = str(lines[i])
            line = lines[i].split()
            if line[0] == "Energy":
                pass
            else:
                pose_data.update( {
                    terms[i-1]: float(line[-1])
                } )
                continue
    pm = pm.append(pose_data, ignore_index=True)

# Makes a pretty DataFrame with all the info we need
# Btw, s is the pose ranking and I did it like that to add it to the beginning of the columns
pm_sum = pm.iloc[:, -10:]
s = pm.iloc[:, 2]
pm_sum.insert(0, 'rank', s)
print(pm_sum) 

pm_sum.to_csv('poses.csv', index=False)

# Does the multi-variable ordinary least squares regression analysis
lm = smf.ols(formula='rank ~ P_intra + L_intra + G_solv + SASA + P_solv + P_SASA + L_solv + L_SASA + vdw + e_elec', data=pm_sum).fit()
print(lm.params)
print(lm.summary())

# Doing this lets you select individual weights assigned by the OLS fitting procedure
# ex: select the weight assigned to the P_intra term in the linear equation
lmP = lm.params
#print(lmP.P_intra)

# Getting the raw total score and selecting individual elements for the plots
pm_sum['total_score']=pm_sum.iloc[:,1:].sum(axis=1)

# This plots the fitted values of a parameter with the rank of that pose, just swap out the index in plot_fit() with the
# column you want to analyze (change the value of x = [] too)

x = pm_sum['L_SASA']
y = pm_sum['rank']

#fig, ax = plt.subplots()
fig = sm.graphics.plot_fit(lm, 8)
plt.plot(x, y, 'o', label='original data')
plt.show()

