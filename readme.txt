The interactive exploration of US Bike Share data has been implemented in a simple GUI application using tkinter.

The application window has:
- Radio buttons along the left side of the window for selecting filters
- A "Load Data" button for updating the statistics along the right side of the window
- A "Print Data" button to print the raw data in the terminal
- A "Quit" button to terminate the application

Most of the code in bikeshare.py defines the layout of the GUI. I've done my best to clean this code and break it out into smaller functions. If I were to futher develop this application, I would break this out into another module in order to make it more manageable.

The Standard Library documentation for tkinter can be found at:
https://docs.python.org/3/library/tkinter.html

Black has been used for code formatting. More information can be found at:
https://pypi.org/project/black/

Pylint has been used for style checking. The following lints were set aside to maintain the simplicity of the project:
- C0301: Line too long
- R0913: Too many arguments
- R0901: Too many ancestors
- R0902: Too many instance attributes

More information can be found at:
https://pylint.org/
