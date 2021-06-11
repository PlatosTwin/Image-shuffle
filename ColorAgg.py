import random
import sys
from math import log10, sqrt

import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from numpy.random import default_rng

fname = 'Documents/Art/Watercolor/Scans/Cholla on Edge.jpg'


def aggregate(filename, ax_agg, color_threshold=250, bins=10, percent_thresh=1e-10, seed=False):
    """
    Aggregate and plot by prominence the colors in the input image. Will print random seed used to generate plot.
    """

    im_rgb = Image.open('/Users/nikitabogdanov/' + filename).convert('RGB')

    # Get colors, sort the list, and remove colors that are overly near to white.
    colors = im_rgb.getcolors(maxcolors=2000000)
    try:
        colors = sorted(colors, key=lambda x: -x[0])
    except IndexError:
        print("ERROR in function '" + str(sys._getframe().f_code.co_name) +
              "'. Increase maxcolors to process this image.")
        return

    near_white = [c for c in colors
                  if c[1][0] > color_threshold and c[1][1] > color_threshold and c[1][2] > color_threshold]
    removed = 0
    for c in near_white:
        colors.pop(colors.index(c))
        removed += 1

    print(str(removed) + " colors near white removed.")

    # Split colors into RGB and frequency
    rgb = [[c[1][i] / 255 for i in range(3)] for c in colors]
    freq = [c[0] for c in colors]

    # Bin the colors
    hist, binedges = np.histogramdd(np.array(rgb), bins=bins, weights=freq)

    # Create rectangles to represent colors
    if not seed:
        seed = random.randrange(sys.maxsize)
    print("'Aggregate' seed: " + str(seed))
    rg = default_rng(seed)
    plot_width = 50
    plot_height = plot_width
    for x, _ in enumerate(binedges[0][0:-1]):
        for y, _ in enumerate(binedges[1][0:-1]):
            for z, _ in enumerate(binedges[2][0:-1]):
                if hist[x, y, z] > hist.sum()*percent_thresh:

                    rect_x = rg.random() * plot_width - plot_width / 2
                    rect_y = rg.random() * plot_height - plot_height / 2
                    rect_w = 100 * log10(1 + sqrt(hist[x, y, z] / hist.sum()))
                    rect_h = rect_w

                    # Get the RGB values each bin represents, using the values the bins are centered on
                    c = (binedges[0][x] + 0.5 / bins, binedges[1][y] + 0.5 / bins, binedges[2][z] + 0.5 / bins)
                    ax_agg.add_patch(plt.Rectangle((rect_x, rect_y), rect_w, rect_h, color=c, alpha=.5))

    ax_agg.set_aspect('equal')
    ax_agg.set_xlim(auto=True)
    ax_agg.set_ylim(auto=True)
    ax_agg.plot()
    ax_agg.axis('off')


def small_factors(x, target):
    num = 1

    for i in range(1, x + 1):
        if x % i == 0 and i < target + 1 and i > target - 1:
           num = i
           break

    return num


def shuffle(array, div, seed=False):
    # Make the number of rows divisible by threshold
    while small_factors(array.shape[0], div) != div:
        array = np.delete(array, 0, axis=0)

    # Array to store stacked rows
    r_segmented = np.zeros((div, int(array.shape[0] / div * array.shape[1]), 3))

    # Stack rows
    for i in range(div):
        temp = array[int(i * array.shape[0] / div), :, :]
        for row in array[int(i * array.shape[0] / div + 1):int((i + 1) * array.shape[0] / div), :, :]:
            temp = np.vstack((temp, row))

        r_segmented[i] = temp

    # Shuffle rows
    if not seed:
        seed = random.randrange(sys.maxsize)
    rng = np.random.default_rng(seed)
    rng.shuffle(r_segmented)

    # Split shuffled rows
    array_new = np.zeros_like(array)
    for i in range(div):
        array_new[int(i * array.shape[0] / div):int((i + 1) * array.shape[0] / div), :, :] =\
            np.vsplit(r_segmented[i], int(array.shape[0] / div))

    return array_new


def image_shuffle(filename, ax_shuffled, r_div, c_div, total_shuffle=True, seed=False):
    """
    Tile an input image and randomly shuffle the tiles. Seed functionality not yet implemented.
    """

    if c_div == 0 or r_div == 0:
        raise ValueError("'Threshold' cannot be set to 0. Check h_thresh and v_thresh.")

    # Read image
    img = mpimg.imread('/Users/nikitabogdanov/' + filename)
    img = img[:, :, 0:3]

    # Make sure number of rows and columns is divisible by r_div and c_div
    while small_factors(img.shape[0], r_div) != r_div:
        img = np.delete(img, 0, axis=0)

    while small_factors(img.shape[1], c_div) != c_div:
        img = np.delete(img, 0, axis=1)

    # Intra-row shuffling: row slice, rotate, shuffle, rotate back, re-compose
    intra_row_shuffled = np.zeros_like(img)
    for i in range(r_div):
        r_slice = img[int(i * img.shape[0] / r_div):int((i + 1) * img.shape[0] / r_div), :, :]
        rotated_r_slice = np.rot90(r_slice)
        shuffled_rotated_r_slice = shuffle(rotated_r_slice, div=c_div)
        shuffled_r_slice = np.rot90(shuffled_rotated_r_slice, 3)

        intra_row_shuffled[int(i * img.shape[0] / r_div):int((i + 1) * img.shape[0] / r_div), :, :] = shuffled_r_slice

        final_shuffled = intra_row_shuffled
    # If total shuffle: row shuffle, rotate, new row slice, rotate, shuffle, rotate back, compose, rotate back
    if total_shuffle:
        #
        row_shuffled = shuffle(intra_row_shuffled, div=r_div)
        rotated_row_shuffled = np.rot90(row_shuffled)
        row_col_shuffled = np.zeros_like(rotated_row_shuffled)

        for i in range(c_div):
            rc_slice = rotated_row_shuffled[int(i * rotated_row_shuffled.shape[0] / c_div):
                                      int((i + 1) * rotated_row_shuffled.shape[0] / c_div), :, :]

            shuffled_rc_slice = np.rot90(shuffle(np.rot90(rc_slice), div=r_div))

            row_col_shuffled[int(i * rotated_row_shuffled.shape[0] / c_div):
                       int((i + 1) * rotated_row_shuffled.shape[0] / c_div), :, :] = shuffled_rc_slice

        final_shuffled = shuffle(np.rot90(row_col_shuffled), div=r_div)

    ax_shuffled.imshow(final_shuffled, aspect='equal')
    ax_shuffled.axis('off')


# Setup plotting
fig = plt.figure()
# ax_img = plt.subplot(211)  # 211
ax_agg = plt.subplot(111)  # 223
# ax_shuffled = plt.subplot(111)  # 224

# Create aggregate and/or shuffled images
aggregate(fname, ax_agg=ax_agg, bins=15)
# image_shuffle(fname, ax_shuffled=ax_shuffled, r_div=40, c_div=25, total_shuffle=True)  # Portrait: r < c

#  Show the original
# image = plt.imread('/Users/nikitabogdanov/' + fname)
# ax_img.imshow(image, aspect='equal')
# ax_img.axis('off')

# Show plot
plt.show()
