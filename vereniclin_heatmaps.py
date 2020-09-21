import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from PIL import Image


img_fn_1 = 'Andrea_2020-06-05T11-25-32AAV5-KCl8mM_heatmap.png'
img_fn_2 = 'Andrea_2020-06-05T11-25-32AAV5-KCl8mM_Verenicline_heatmap.png'
img_fn_3 = 'Andrea_2020-06-05T11-25-32AAV5-KCl8mM_Verenicline_washout_heatmap.png'

img_1 = Image.open(img_fn_1)
img_2 = Image.open(img_fn_2)
img_3 = Image.open(img_fn_3)

fig = plt.figure(figsize=(12,3)) # set the figure size to be square

gs = gridspec.GridSpec(1, 3, wspace=None, hspace=None)
# set the space between subplots and the position of the subplots in the figure
# gs.update(wspace=0.01, hspace=0.01, left=0, right=1, bottom=0, top=1)

for g, data in zip(gs, [img_1, img_2, img_3]):
    ax = plt.subplot(g)
    ax.axes.get_yaxis().set_visible(False)
    ax.axes.get_xaxis().set_visible(False)
    ax.axis('off')
    plt.imshow(data)
top = gs.top
bottom = gs.bottom
gs.tight_layout(fig, h_pad=0.5)
plt.savefig('Andrea_AAV5_complete_heatmap.png')
plt.show()