from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.app import MDApp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.image import Image as KivyImage
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.filemanager import MDFileManager
from kivy.uix.popup import Popup
from kivy.uix.progressbar import ProgressBar
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle
import matplotlib.pyplot as plt
import pandas as pd
import os
from kivy.uix.spinner import Spinner
import time  # Import the time module

# ...
import core

class CustomFigureCanvas(FigureCanvasKivyAgg):
    def __init__(self, figure, **kwargs):
        super(CustomFigureCanvas, self).__init__(figure, **kwargs)
        Clock.schedule_once(self.resize_callback, 0)

    def resize_callback(self, dt):
        dpi = self.figure.get_dpi()
        self.figure.set_size_inches(self.width / dpi, self.height / dpi)
        self.draw()

class ImageUploaderApp(MDApp):
    def __init__(self, **kwargs):
        super(ImageUploaderApp, self).__init__(**kwargs)
        self.file_manager = None  # Initialize file_manager attribute
        self.current_processed_image_path = None
        # Screen manager to handle multiple screens
        self.sm = ScreenManager()

    def build(self):
        self.layout = BoxLayout(orientation='vertical', spacing=10)

        # Set background image
        background_image = KivyImage(source='bac.png', allow_stretch=True, keep_ratio=False)
        self.layout.add_widget(background_image)


        
        # Stylish label for the title
        title_label = Label(
            text="Image Uploader",
            font_size='24sp',
            color=(1, 1, 1, 1),  # White color
            bold=True,
            size_hint_y=None,
            height=50
        )
        self.layout.add_widget(title_label)

        # Button for uploading images
        self.upload_button = MDRaisedButton(
            text="Upload Images",
            on_release=self.show_file_chooser,
            size_hint=(None, None),
            size=(200, 50),
            pos_hint={'center_x': 0.5}
        )
        self.layout.add_widget(self.upload_button)

        # Process button initially invisible
        self.process_button = None  # Initialize process_button as None

        # Instance variables to store the list of image files and selected path
        self.image_files = []
        self.selected_path = ""

        return self.layout

    def show_file_chooser(self, instance):
        self.file_manager = MDFileManager(
            exit_manager=self.exit_manager,
            select_path=self.select_path,
        )
        self.file_manager.show('/')  # Start with the root directory

    def exit_manager(self, *args):
        self.file_manager.close()

    def select_path(self, path):
        self.file_manager.close()
        if path:
            self.upload_images(path)

    def upload_images(self, selected_path):
        self.selected_path = selected_path
        if os.path.isdir(self.selected_path):  # Check if the selected path is a directory
            self.upload_images_from_folder()
        else:
            print("Invalid selection. Please select a folder.")

    def upload_images_from_folder(self):
        # Get a list of image files and sort them using a custom sorting key
        self.image_files = sorted(
            [f for f in os.listdir(self.selected_path) if f.endswith(('.png', '.jpg'))],
            key=lambda x: int(x.split('_')[1].split('.')[0])
        )

        if not self.image_files:
            print("Error: No image files found in the selected folder.")
        else:
            print(f"Selected Folder with Image Files: {self.selected_path}")
            print("Image Files:")
            for image_file in self.image_files:
                print(f"- {image_file}")

            # Enable and show the process button dynamically
            self.process_button = MDRaisedButton(
                text="Process Images",
                on_release=self.process_images,
                size_hint=(None, None),
                size=(200, 50),
                pos_hint={'center_x': 0.5}
            )
            self.layout.add_widget(self.process_button)

    def process_images(self, instance):
        if not self.image_files:
            print("Error: No image files selected. Please upload images first.")
        else:
            # Show processing popup
            processing_popup = self.show_processing_popup()

            # Simulate processing (replace this with your actual processing logic)
            Clock.schedule_once(lambda dt: self.processing_logic(processing_popup), 0)

    def show_processing_popup(self):
        # Create a Popup with a ProgressBar
        processing_popup = Popup(
            title='Processing',
            size_hint=(None, None),
            size=(300, 100),
            auto_dismiss=False  # Prevents the popup from closing automatically
        )
        processing_popup.open()
        return processing_popup

    def processing_logic(self, processing_popup):
        # Actual processing logic goes here
        df = core.genimage(True, len(self.image_files), self.image_files, self.selected_path)
        df.to_excel('max_peak_data.xlsx')

        # Close the processing popup
        processing_popup.dismiss()

        # Show the Insights button after processing
        insights_button = MDRaisedButton(
            text="Insights",
            on_release=self.show_insights_screen,
            size_hint=(None, None),
            size=(200, 50),
            pos_hint={'center_x': 0.5}
        )
        self.layout.add_widget(insights_button)


    def show_insights_screen(self, instance):
     self.delete_current_processed_image()
 
     # Create a new screen for insights
     insights_screen = Screen(name='insights')
     insights_layout = BoxLayout(
         orientation='vertical', spacing=10, size_hint=(None, None), size=(400, 300),
         pos_hint={'center_x': 0.5, 'center_y': 0.5}
     )
 
     # Add buttons for Strip Location Plot and Strain Plot
     strip_location_button = MDRaisedButton(
         text="Strip Location Plot",
         on_release=self.show_strip_location_plot,
         size_hint=(None, None),
         size=(200, 50),
         pos_hint={'center_x': 0.5}
     )
     strain_plot_button = MDRaisedButton(
         text="Strain Plot",
         on_release=self.show_strain_plot_options,
         size_hint=(None, None),
         size=(200, 50),
         pos_hint={'center_x': 0.5}
     )
 
     # Add a "Back" button to return to the main screen
    
     insights_layout.add_widget(strip_location_button)
     insights_layout.add_widget(strain_plot_button)
     
 
     insights_screen.add_widget(insights_layout)
 
     # Clear the existing layout and add the new one
     self.layout.clear_widgets()
     self.layout.add_widget(insights_screen)
 





    def show_strip_location_plot(self, instance):
     try:
        # Read the saved data
        df = pd.read_excel('max_peak_data.xlsx')

        # Create a new figure
        fig, ax = plt.subplots()
        max_1 = df['Max Peak 1']
        max_2 = df['Max Peak 2']
        max_3 = df['Max Peak 3']
        max_4 = df['Max Peak 4']
        max_5 = df['Max Peak 5']

        ax.plot(max_1, label='strip 1', color='blue')
        ax.plot(max_2, label='strip 2', color='green')
        ax.plot(max_3, label='strip 3', color='orange')
        ax.plot(max_4, label='strip 4', color='black')
        ax.plot(max_5, label='strip 5', color='red')
        ax.legend()
        ax.set_title('Position of each Stripes')
        ax.set_ylabel('Pixels from Ref Point')
        ax.set_xlabel('Time')

        # Save the processed plot as an image
        processed_image_path = "strip_location_plot.png"
        self.current_processed_image_path = processed_image_path 
        canvas = FigureCanvasKivyAgg(figure=fig)
        canvas.print_png(processed_image_path)

        # Create a new layout with the processed image
        processed_layout = BoxLayout(orientation='vertical', spacing=10)
        processed_image = KivyImage(source=processed_image_path)
        processed_layout.add_widget(processed_image)

        # Add a "Back" button to return to the main screen
        back_button = MDRaisedButton(
            text="Back",
            on_release=self.show_insights_screen,
            size_hint=(None, None),
            size=(200, 50),
            pos_hint={'center_x': 0.5}
        )
        processed_layout.add_widget(back_button)

        # Clear the existing layout and add the new one
        self.layout.clear_widgets()
        self.layout.add_widget(processed_layout)

     except FileNotFoundError:
        print("Error: Data file not found. Please process images first.")

   


    def show_strain_plot_options(self, instance):
      # Create a new screen for strain plot options
      strain_options_screen = Screen(name='strain_options')
      strain_options_layout = BoxLayout(orientation='vertical', spacing=10, size_hint=(None, None), size=(400, 300), pos_hint={'center_x': 0.5, 'center_y': 0.5})
  
      # Add starting strip widgets
      starting_layout = BoxLayout(orientation='horizontal', spacing=10, size_hint_y=None, height=50)
      starting_label = Label(text="Starting strip number:", size_hint=(None, None), height=30, font_size=16)
      starting_spinner = Spinner(text="Starting Strip", values=["1", "2", "3", "4", "5"], size_hint=(None, None), size=(200, 44))
      starting_layout.add_widget(starting_label)
      starting_layout.add_widget(starting_spinner)
  
      # Add ending strip widgets
      ending_layout = BoxLayout(orientation='horizontal', spacing=10, size_hint_y=None, height=50)
      ending_label = Label(text="Ending strip number:", size_hint=(None, None), height=30, font_size=16)
      ending_spinner = Spinner(text="Ending Strip ", size_hint=(None, None), size=(200, 44))
      ending_layout.add_widget(ending_label)
      ending_layout.add_widget(ending_spinner)
  
      # Function to update ending_spinner values based on the selected starting_spinner value
      def update_spinner_values(selected_value, spinner_to_update, other_spinner):
          spinner_to_update.values = [value for value in ["1", "2", "3", "4", "5"] if value != selected_value]
  
      starting_spinner.bind(text=lambda instance, value: update_spinner_values(value, ending_spinner, starting_spinner))
      ending_spinner.bind(text=lambda instance, value: update_spinner_values(value, starting_spinner, ending_spinner))
  
      # Button to proceed to the strain plot
      proceed_button = MDRaisedButton(
          text="Proceed",
          on_release=lambda x: self.show_strain_plot(instance, starting_spinner.text, ending_spinner.text),
          size_hint=(None, None),
          size=(200, 50),
          pos_hint={'center_x': 0.5}  # Center the button horizontally
      )
  
      # Add widgets to the layout
      strain_options_layout.add_widget(starting_layout)
      strain_options_layout.add_widget(ending_layout)
      strain_options_layout.add_widget(proceed_button)
  
      # Add the layout to the screen
      strain_options_screen.add_widget(strain_options_layout)
  
      # Clear the existing layout and add the new one
      self.layout.clear_widgets()
      self.layout.add_widget(strain_options_screen)




    def show_strain_plot(self, instance, start, end):
     try:
        # Convert selected strip numbers to integers
        start = int(start)
        end = int(end)

        df = pd.read_excel('max_peak_data.xlsx')

        data_d = {}
        for i in range(1, 6):
            data_d[str(i)] = df['Max Peak ' + str(i)]

        count = len(data_d['1'])

        fig, ax = plt.subplots()
        if start is not None and end is not None:
            strain = []
            diffres = data_d[str(end)][0] - data_d[str(start)][0]

            for i in range(1, count):
                diff = data_d[str(end)][i] - data_d[str(start)][i]
                strain.append((diff - diffres) / diff)

        ax.plot(strain, label='strain', color='blue')
        ax.legend()
        ax.set_title('Strain between ' + str(start) + ' and ' + str(end))
        ax.set_ylabel('Strain')
        ax.set_xlabel('Frames')

        # Save the strain plot with a timestamp to avoid caching issues
        timestamp = int(time.time())
        processed_image_path = f"strain_plot_{timestamp}.png"
        self.current_processed_image_path = processed_image_path 
        canvas = FigureCanvasKivyAgg(figure=fig)
        canvas.print_png(processed_image_path)

        # Create a new layout with the processed image
        processed_layout = BoxLayout(orientation='vertical', spacing=10)
        processed_image = KivyImage(source=processed_image_path)
        processed_layout.add_widget(processed_image)

        # Add a "Back" button to return to the main screen
        back_button = MDRaisedButton(
            text="Back",
            on_release=self.show_insights_screen,
            size_hint=(None, None),
            size=(200, 50),
            pos_hint={'center_x': 0.5}
        )
        processed_layout.add_widget(back_button)

        # Clear the existing layout and add the new one
        self.layout.clear_widgets()
        self.layout.add_widget(processed_layout)

     except ValueError:
        print("Error: Invalid strip number selected.")
     except FileNotFoundError:
        print("Error: Data file not found. Please process images first.")
    
    def delete_current_processed_image(self):
        try:
            if self.current_processed_image_path and os.path.exists(self.current_processed_image_path):
                os.remove(self.current_processed_image_path)
        except Exception as e:
            print(f"Error deleting image: {e}")
if __name__ == '__main__':
    ImageUploaderApp().run()