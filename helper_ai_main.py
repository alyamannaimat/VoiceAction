import sys
import os
from qtpy import QtWidgets
from PySide6.QtGui import QIcon
from PySide6.QtGui import QPixmap
import helper
import audio

# Packages installed:
#
# Package                   Version
# ------------------------- -----------
# altgraph                  0.17.4
# contourpy                 1.3.0
# cycler                    0.12.1
# fonttools                 4.54.1
# kiwisolver                1.4.7
# matplotlib                3.9.2
# numpy                     2.1.1
# packaging                 24.1
# pefile                    2024.8.26
# pillow                    10.4.0
# pip                       24.2
# pyinstaller               6.10.0
# pyinstaller-hooks-contrib 2024.8
# pyparsing                 3.1.4
# pyqtgraph                 0.13.7
# PySide6                   6.7.3
# PySide6_Addons            6.7.3
# PySide6_Essentials        6.7.3
# python-dateutil           2.9.0.post0
# pywin32-ctypes            0.2.3
# QtAwesome                 1.3.1
# QtPy                      2.4.1
# setuptools                75.1.0
# shiboken6                 6.7.3
# six                       1.16.0
apiKey = input("Enter your Google Generative AI API Key: ")

class App(QtWidgets.QMainWindow):
    
    # Initialise App
    def __init__(self):
        super().__init__()

        # Main Widget and Layout
        self.main_wdg = QtWidgets.QWidget()
        self.layout = QtWidgets.QVBoxLayout(self.main_wdg)

        self.app_folder = 'Helper ai'  # Name of appdata folder

        # Settings list
        self.settings = ['']

        # App UI Elements here:

        self.output_layout = QtWidgets.QHBoxLayout()
        self.input_layout = QtWidgets.QHBoxLayout()
        self.log_layout = QtWidgets.QVBoxLayout()
        self.image_layout = QtWidgets.QVBoxLayout()

        self.log_title = QtWidgets.QLabel('Log:')
        self.image_title = QtWidgets.QLabel('Image:')
        self.log_list_wdg = QtWidgets.QListWidget()
        self.image_wdg = QtWidgets.QLabel()
        self.image_wdg.setMinimumSize(500, 500)
        self.log_list_wdg.setMinimumSize(200, 200)

        self.record_button = QtWidgets.QPushButton()
        self.mic_icon = QIcon('images2/images2/mic_symbol.png')
        self.record_button.setIcon(self.mic_icon)
        self.record_button.setFixedSize(35, 35)
        self.input_textbox = QtWidgets.QLineEdit()
        self.input_textbox.setPlaceholderText('Type...')
        self.enter_button = QtWidgets.QPushButton('Enter')

        self.init_ui()
        self.populate_ui()
        self.connect_signals()
        

    # Initialise UI
    def init_ui(self):
        self.setWindowTitle('Helper AI')
        image = self.resource_path('images2/images2/google-gemini-icon.ico')
        self.setWindowIcon(QIcon(image))

        # Read Settings File
        settings_data = self.read_from_appdata(f'{self.app_folder}/config/app_settings.txt')

        if settings_data is not None:
            self.settings = settings_data.splitlines()
            print('Settings: ' + str(self.settings))

        if not settings_data:
            # Makes new settings file
            print('Overwriting settings file...')

            settings_data = '\n'.join(self.settings)
            print(f'''Writing these settings:

                    {settings_data}''')
            self.write_to_appdata(f'{self.app_folder}/config/app_settings.txt', settings_data)

        # MAIN Widget
        self.setCentralWidget(self.main_wdg)

        # MAIN Layout
        self.main_wdg.setLayout(self.layout)

        self.layout.addLayout(self.output_layout)
        self.layout.addLayout(self.input_layout)

        self.output_layout.addLayout(self.log_layout)
        self.output_layout.addLayout(self.image_layout)

        self.log_layout.addWidget(self.log_title)
        self.log_layout.addWidget(self.log_list_wdg)

        self.image_layout.addWidget(self.image_title)
        self.image_layout.addWidget(self.image_wdg)

        self.input_layout.addWidget(self.record_button)
        self.input_layout.addWidget(self.input_textbox)
        self.input_layout.addWidget(self.enter_button)

    def record_button_clicked(self):
        print('RECORD BUTTON CLICKED')
        self.log_list_wdg.addItem('RECORD BUTTON CLICKED!!!')
        command = audio.main(apiKey)
        self.input_textbox.setText(command)
        
        

    def enter_button_clicked(self):
        print('ENTER BUTTON CLICKED')
        text_in_textbox = self.input_textbox.text()
        if text_in_textbox == '':
            print('textbox is empty')
            self.log_list_wdg.addItem('textbox is empty')
        else:
            print('executing action')
            self.log_list_wdg.addItem('executing action')
            helper.main(text_in_textbox, apiKey)


    def populate_ui(self):
        print('Populated UI.')

    def connect_signals(self):
        print('Connecting signals...')
        self.record_button.clicked.connect(self.record_button_clicked)
        self.enter_button.clicked.connect(self.enter_button_clicked)

    def write_to_appdata(self, relative_path, data):
        # Get the path to the Roaming AppData directory
        appdata_path = os.path.join(os.path.expanduser('~'), 'AppData', 'Roaming')

        # Create the full path for the specified subdirectory and file
        full_path = os.path.join(appdata_path, relative_path)

        # Check if the file exists
        if not os.path.exists(full_path):
            print(f"File not found: {full_path}")
            print('Missing files and directories will be restored')

        # Extract the directory part of the full path
        directory = os.path.dirname(full_path)

        # Create the directory if it doesn't exist
        os.makedirs(directory, exist_ok=True)

        # Write to the file
        with open(full_path, 'w') as f:
            f.write(data)

        print(f"Data written to: {full_path}")

    def read_from_appdata(self, relative_path):
        # Get the path to the Roaming AppData directory
        appdata_path = os.path.join(os.path.expanduser('~'), 'AppData', 'Roaming')

        # Create the full path for the specified subdirectory and file
        full_path = os.path.join(appdata_path, relative_path)

        # Check if the file exists
        if not os.path.exists(full_path):
            print(f"File not found: {full_path}")
            print('Missing files and directories will be restored')
            return None

        # Read the file
        with open(full_path, 'r') as f:
            data = f.read()

        print(f"Data read from: {full_path}")
        return data

    # For reading embedded files
    def resource_path(self, relative_path):
        """ Get the absolute path to the resource (for both exe and dev modes) """
        try:
            # If the application is running as a PyInstaller executable
            base_path = sys._MEIPASS
        except AttributeError:
            # If running in development mode
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)

if __name__ == '__main__':
    print(__name__)
    app = QtWidgets.QApplication(sys.argv)
    launcher = App()
    launcher.show()
    
    sys.exit(app.exec())

