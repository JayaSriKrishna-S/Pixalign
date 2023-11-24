import os
import time
import cv2
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# PLUG - IN - YOUR - MANUAL - SCRIPT
from scripts import plusminus

def genimage(csv,total_images,image_list,dir):

 df = pd.DataFrame(columns=['Max Peak 1', 'Max Peak 2',
                  'Max Peak 3', 'Max Peak 4', 'Max Peak 5'])

 
 if csv==True:
    starti=0
    endi=total_images+1
 else:
    starti=total_images
    endi=total_images+1  

 for e in image_list[starti:endi]:
    # Read the image
    # Note the flag for grayscale
    print(dir,e)
    image = cv2.imread(os.path.join(dir, str(e)), cv2.IMREAD_GRAYSCALE)

    # Get the height and width of the image
    height, width = image.shape

    # Determine the center y-coordinate
    center_y = height // 2

    # Extract a 1-pixel wide horizontal strip from the center of the image
    strip = image[center_y:center_y + 1, :]

    # Iterate through the strip to find the x-coordinate where the pixel value becomes 0
    for x in range(width):
        pixel_value = strip[0, x]
        if pixel_value == 0:
            mid_strip = (x - 1) // 2
            break

    mid_strip = 77

    # Extract vertical strip using mid_strip x-coordinate
    vertical_strip = image[:, mid_strip:mid_strip + 1]

    # Get pixel values from the bottom to the top of the vertical strip
    pixel_values = [vertical_strip[y, 0] for y in range(height)]
    pixel_values.reverse()
    

    spike_max_peaks = plusminus.script(pixel_values)

    if not csv:
    
       # Create a new figure and plot the image
       plt.figure(figsize=(10, 6))
   
       # Plot your data
       plt.plot(range(height), pixel_values, label='Original Data', color='blue')
       plt.scatter(spike_max_peaks, [pixel_values[i] for i in spike_max_peaks], color='red', marker='o', label='Max Peaks')
   
       # Additional plot settings
       plt.legend()
       plt.xlabel('Y Coordinates')
       plt.ylabel('Pixel Values')
       plt.title('Maximum Peaks within Detected Spikes (Min Amplitude: 10 pixels, Max Width: 30 pixels)')
       plt.gca().invert_xaxis()
   
       # Set Y-axis limits to limit the Y-axis
       plt.ylim(0, 300)  # Replace 'your_max_limit_here' with the value you want
   
       # Load the image separately
       background_image = cv2.imread('image/images_' + str(e) + '.jpg')
   
       # Rotate the image 90 degrees to the left
       rotated_image = cv2.rotate(background_image, cv2.ROTATE_90_CLOCKWISE)
       rotated_image = cv2.flip(rotated_image, 0)
   
       # Crop the rotated image to fit the plot size
       crop_width = min(rotated_image.shape[1], height)
       cropped_image = rotated_image[:, :crop_width]
   
       # Display the rotated and cropped image as the background
       plt.imshow(cropped_image, cmap='gray', extent=[0, height, 0, cropped_image.shape[0]])
   
       # Save the plot with the image as a background
       plt.savefig(f'processed/pr_{e}.png', bbox_inches='tight')
   
       # Clear the current figure to prepare for the next iteration
       plt.clf()
    else:
    # Append data to the DataFrame
      df = pd.concat([df, pd.DataFrame([spike_max_peaks], columns=df.columns)], ignore_index=True)

 return df



# df=genimage(True,460)
# df.to_excel('max_peak_data.xlsx', index=False)
# time.sleep(1)

# ploty.plot()


# import tkinter as tk
# from PIL import Image, ImageTk
# from tkinter import messagebox


# # Function to validate user input
# def validate_input_callback(P):
#     if P.isdigit():
#         value = int(P)
#         return 1 <= value <= 460
#     return False

# # Function to update the displayed image
# def update_image():
#     try:
#         e = int(entry.get())
#         if 1 <= e <= 460:
#             genimage(False,e)
#             image_path = f'processed/pr_{e}.png'
#             img = Image.open(image_path)
#             img = ImageTk.PhotoImage(img)
#             label.config(image=img)
#             label.image = img
#         else:
#             messagebox.showerror("Error", "Enter a number between 1 and 460")
#     except ValueError:
#         messagebox.showerror("Error", "Invalid input")

# # Function to handle window close event
# def on_closing():
#     app.destroy()
    
#     print('press Q to exit: ')
#     while True:
#       strain.plot()
#       user_input = input('Press Q to exit: ')
#       if user_input.lower() == 'q':
#         break
#     exit()

# # Create the main application window
# app = tk.Tk()
# app.title("Image Viewer")

# # Set a fixed window size and center it on the screen
# window_width = 400
# window_height = 350
# screen_width = app.winfo_screenwidth()
# screen_height = app.winfo_screenheight()
# x = (screen_width - window_width) // 2
# y = (screen_height - window_height) // 2
# app.geometry(f'{window_width}x{window_height}+{x}+{y}')

# # Create a label for the title
# title_label = tk.Label(app, text="Image Viewer", font=("Helvetica", 18))
# title_label.pack(pady=10)

# # Create an entry widget for user input
# entry = tk.Entry(app, font=("Helvetica", 12), validate="key", validatecommand=(validate_input_callback, "%P"))
# entry.pack(pady=10)

# # Create a button to update the displayed image
# update_button = tk.Button(app, text="Update Image", command=update_image, font=("Helvetica", 14))
# update_button.pack()

# # Create a label to display the image
# label = tk.Label(app)
# label.pack()

# # Add a footer label
# footer_label = tk.Label(app, text="Enter a number between 1 and 460 and click 'Update Image'", font=("Helvetica", 10))
# footer_label.pack(pady=20)

# # Create a close button
# close_button = tk.Button(app, text="Close", command=on_closing, font=("Helvetica", 14))
# close_button.pack()

# # Handle the window close event
# app.protocol("WM_DELETE_WINDOW", on_closing)

# # Start the Tkinter main loop
# app.mainloop()

