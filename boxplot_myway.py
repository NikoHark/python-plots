"""
Thanks Josh Hemann for the example
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon


# Generate some data from five different probability distributions,
# each with different characteristics. We want to play with how an IID
# bootstrap resample of the data preserves the distributional
# properties of the original sample, and a boxplot is one visual tool
# to make this assessment
numDists = 5
randomDists = ['Normal(1,1)', ' Lognormal(1,1)', 'Exp(1)', 'Gumbel(6,4)',
               'Triangular(2,9,11)']
N = 10000
norm = np.random.normal(5, 1, N)
logn = np.random.lognormal(1, 1, N)
expo = np.random.exponential(5, N)
gumb = np.random.gumbel(5, 4, N)
tria = np.random.triangular(2, 9, 11, N)

# print "Norm:"
# print norm

# Generate some random indices that we'll use to resample the original data
# arrays. For code brevity, just use the same random indices for each array
bootstrapIndices = np.random.random_integers(0, N - 1, N)
normBoot = norm[bootstrapIndices]
expoBoot = expo[bootstrapIndices]
gumbBoot = gumb[bootstrapIndices]
lognBoot = logn[bootstrapIndices]
triaBoot = tria[bootstrapIndices]

# print "bootstrapIndices:"
# print bootstrapIndices



#
# Histogram
#

fig = plt.figure(1)
plt.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=0.06, hspace=0.22)

# Define min and max range of x axis for histogram
minX = 0
maxX = 20

ax1 = fig.add_subplot(1, 1, 1)
bins = np.arange(minX, maxX, 0.3)

hist, bin_edges = np.histogram(norm, bins=bins, density=True)
hist = hist * np.diff(bin_edges)
hist_cumul = np.cumsum(hist)
plt.plot(bin_edges[0:len(bin_edges) - 1], hist, "-*", label="norm", color='green')

hist, bin_edges = np.histogram(expo, bins=bins, density=True)
hist = hist * np.diff(bin_edges)
hist_cumul = np.cumsum(hist)
plt.plot(bin_edges[0:len(bin_edges) - 1], hist, "-*", label="expo", color='blue')

hist, bin_edges = np.histogram(logn, bins=bins, density=True)
hist = hist * np.diff(bin_edges)
hist_cumul = np.cumsum(hist)
plt.plot(bin_edges[0:len(bin_edges) - 1], hist, "-*", label="logn", color='orange')

hist, bin_edges = np.histogram(gumb, bins=bins, density=True)
hist = hist * np.diff(bin_edges)
hist_cumul = np.cumsum(hist)
plt.plot(bin_edges[0:len(bin_edges) - 1], hist, "-*", label="gumb", color='red')

hist, bin_edges = np.histogram(tria, bins=bins, density=True)
hist = hist * np.diff(bin_edges)
hist_cumul = np.cumsum(hist)
plt.plot(bin_edges[0:len(bin_edges) - 1], hist, "-*", label="tria", color='magenta')



# Add labels so that it looks really professional..
plt.xlabel('Random variable x')
plt.ylabel('Percentage')
plt.title('')
ax1.grid(True)
ax1.set_xticks(np.arange(minX, maxX, 1))
ax1.set_yticks(np.arange(0, 1.02, 0.02))
plt.xlim([minX, maxX])
plt.ylim([0, 0.15])
handles, labels = ax1.get_legend_handles_labels()
lgd = ax1.legend(handles, labels, loc='upper right')


# Create the formatter using the function to_percent. This multiplies all the
# default labels by 100, making them all percentages
# formatter = FuncFormatter(to_percent)
# ax1.yaxis.set_major_formatter(formatter)




#
# BOXPLOT
#
data = [norm, normBoot, logn, lognBoot, expo, expoBoot, gumb, gumbBoot,
        tria, triaBoot]

fig, ax1 = plt.subplots(figsize=(10, 6))
fig.canvas.set_window_title('MyWay journey lengths')
plt.subplots_adjust(left=0.075, right=0.95, top=0.9, bottom=0.25)

bp = plt.boxplot(data, notch=0, sym='+', vert=1, whis=1.5)
plt.setp(bp['boxes'], color='black')
plt.setp(bp['whiskers'], color='black')
plt.setp(bp['fliers'], color='red', marker='')  # Invisible marker ''

# Add a horizontal grid to the plot, but make it very light in color
# so we can use it for reading data values but not be distracting
ax1.yaxis.grid(True, linestyle='-', which='major', color='lightgrey',
               alpha=0.5)

# Hide these grid behind plot objects
ax1.set_axisbelow(True)
ax1.set_title('Comparison of journey lengths in Berlin, Catalonia and Trikala')
# ax1.set_xlabel('Distribution')
ax1.set_ylabel('Journey length in kilometers')

# Now fill the boxes with desired colors
boxColors = ['orange', 'royalblue']
numBoxes = numDists * 2
medians = range(numBoxes)
for i in range(numBoxes):
    box = bp['boxes'][i]
    boxX = []
    boxY = []
    for j in range(5):
        boxX.append(box.get_xdata()[j])
        boxY.append(box.get_ydata()[j])
    boxCoords = zip(boxX, boxY)

    # Alternate between Dark Khaki and Royal Blue
    k = i % 2
    boxPolygon = Polygon(boxCoords, facecolor=boxColors[k])
    ax1.add_patch(boxPolygon)

    # Now draw the median lines back over what we just filled in
    med = bp['medians'][i]
    medianX = []
    medianY = []
    for j in range(2):
        medianX.append(med.get_xdata()[j])
        medianY.append(med.get_ydata()[j])
        plt.plot(medianX, medianY, 'k')
        medians[i] = medianY[0]

        # Finally, overplot the sample averages, with horizontal alignment
        # in the center of each box
        # plt.plot([np.average(med.get_xdata())], [np.average(data[i])],
        #         color='w', marker='*', markeredgecolor='k')

# Set the axes ranges and axes labels
ax1.set_xlim(0.5, numBoxes + 0.5)
top = 40
bottom = -5
ax1.set_ylim(bottom, top)
xtickNames = plt.setp(ax1, xticklabels=np.repeat(randomDists, 2))
plt.setp(xtickNames, rotation=45, fontsize=8)


# Due to the Y-axis scale being different across samples, it can be
# hard to compare differences in medians across the samples. Add upper
# X-axis tick labels with the sample medians to aid in comparison
# (just use two decimal places of precision)
pos = np.arange(numBoxes) + 1
upperLabels = [str(np.round(s, 2)) for s in medians]
weights = ['bold', 'semibold']
for tick, label in zip(range(numBoxes), ax1.get_xticklabels()):
    k = tick % 2
    ax1.text(pos[tick], top - (top * 0.05), upperLabels[tick],
             horizontalalignment='center', size='x-small', weight=weights[k],
             color=boxColors[k])

# Finally, add a basic legend
'''plt.figtext(0.80, 0.08,  str(N) + ' Random Numbers' ,
           backgroundcolor=boxColors[0], color='black', weight='roman',
           size='x-small')
plt.figtext(0.80, 0.045, 'IID Bootstrap Resample',
backgroundcolor=boxColors[1],
           color='white', weight='roman', size='x-small')
plt.figtext(0.80, 0.015, '*', color='white', backgroundcolor='silver',
           weight='roman', size='medium')
plt.figtext(0.815, 0.013, ' Average Value', color='black', weight='roman',
           size='x-small')'''

plt.show()
