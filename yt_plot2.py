import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

frequencies = [36170, 109817, 96430, 19046, 40112]   # bring some raw data

freq_series = pd.Series.from_array(frequencies)   # in my original code I create a series and run on that, so for consistency I create a series from the list.

x_labels = ['Puthiya Thalaimurai TV', 'pudu sitee', 'TAMILAN jokes', 'Madras Central', 'Nakkheeranwebtv']


N = 5
ind = np.arange(N)

# now to plot the figure...
plt.figure(figsize=(12, 8))
ax = freq_series.plot(kind='bar')
ax.set_title("Jallikattu Graph", color= 'Blue')
ax.set_xlabel("Channel_Title", color="red", size= '18')
ax.set_ylabel("View Counts", color="red", size= '18')
ax.set_xticklabels(x_labels,  size= '12', rotation= 'horizontal')
#ax.set_xlabel

#ax.set_xticks(x_labels)

rects = ax.patches

# Now make some labels
labels = [ i for i in frequencies]

for rect, label in zip(rects, labels):
    height = rect.get_height()
    ax.text(rect.get_x() + rect.get_width()/2, height + 5, label, ha='center', va='bottom')

plt.show()
plt.savefig("image.jpg")

