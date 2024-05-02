import openslide
from matplotlib import pyplot as plt

import math  # Import the math module

def select_roi_and_scale(wsi_path):
    # Open the WSI file
    slide = openslide.OpenSlide(wsi_path)

    # Use the smallest available level
    lower_level = slide.level_count - 1
    lower_level_dimensions = slide.level_dimensions[lower_level]

    # Read and display the whole image at this level
    whole_slide_image = slide.read_region((0, 0), lower_level, lower_level_dimensions)
    whole_slide_image = whole_slide_image.convert("RGB")  # Convert to RGB

    # Setup the plot for interaction
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.imshow(whole_slide_image)
    ax.set_title(f"Entire Slide at Level {lower_level}")
    plt.axis('off')

    roi = {'start': None, 'end': None}

    def onclick(event):
        # Record x and y coordinates on click
        if roi['start'] is None:
            roi['start'] = (event.xdata, event.ydata)
            print(f"Start point set at {roi['start']}")
        else:
            roi['end'] = (event.xdata, event.ydata)
            print(f"End point set at {roi['end']}")

            # Draw the rectangle
            rect = plt.Rectangle(roi['start'], roi['end'][0] - roi['start'][0], roi['end'][1] - roi['start'][1], linewidth=1, edgecolor='r', facecolor='none')
            ax.add_patch(rect)
            plt.draw()

            # Calculate and scale the coordinates using the correct downsample factor
            downsample_factor = slide.level_downsamples[lower_level]
            top_left = (int(roi['start'][0] * downsample_factor), int(roi['start'][1] * downsample_factor))
            width = int((roi['end'][0] - roi['start'][0]) * downsample_factor)
            height = int((roi['end'][1] - roi['start'][1]) * downsample_factor)

            # Round width and height up to the nearest number divisible by 256
            tile_size = 256
            width = math.ceil(width / tile_size) * tile_size
            height = math.ceil(height / tile_size) * tile_size

            # Print and potentially save these values
            print(f"Scaled top-left and dimensions: ({top_left[0]}, {top_left[1]}) ({width}, {height})")
            
            # Disconnect the mouse click event and close the plot
            fig.canvas.mpl_disconnect(cid)
            plt.close(fig)

    # Connect the mouse click event to the handler
    cid = fig.canvas.mpl_connect('button_press_event', onclick)

    plt.show()

wsi = '/Users/marcusnsr/Desktop/Bachelor/data_old/wsi1.ndpi'
select_roi_and_scale(wsi)