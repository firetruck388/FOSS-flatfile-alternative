# FOSS-flatfile-alternative
FOSS alternative to proprietary product called Flatfile, allowing users to parse a CSV file and generate a SQLite db file containing a table with the same records as the CSV file. 

# CSV to SQLite Converter

This Python application allows users to convert CSV files into SQLite databases. It features a graphical user interface (GUI) for ease of use and includes data integrity checks through checksum validation.

## Features

- **User-Friendly Interface**: Easy to use GUI for selecting and converting files.
- **Checksum Validation**: Ensures data integrity by validating the checksum of each record.
- **Data Type Selection**: Allows users to define the data type for each CSV column.

## How to Use the GUI App After Compiling `completed_script_with_checksumhashing.py`

1. **Select a CSV File**: Use the 'Browse' button to choose a CSV file from your filesystem.
2. ![image](https://github.com/enrimarini/FOSS-flatfile-alternative/assets/98195595/5190548a-8ea5-4849-bfb0-2e0491b88aad)
3. **Confirm File Selection**: After selecting the file, confirm your selection.
4. ![image](https://github.com/enrimarini/FOSS-flatfile-alternative/assets/98195595/0f234a11-99bf-4590-99e9-162727289ef7)
5. ![image](https://github.com/enrimarini/FOSS-flatfile-alternative/assets/98195595/fe2ac2bd-aeda-413a-a789-0fa542dbe70c)
6. **Assign Data Types**: For each column header in the CSV, assign the appropriate data type (e.g., integer, string, datetime).
7. ![image](https://github.com/enrimarini/FOSS-flatfile-alternative/assets/98195595/e76ba15f-fd85-40af-b769-f1a621cd2310)
8. **Confirm Data Types**: Confirm the data types for all columns to proceed with the conversion.
9. ![image](https://github.com/enrimarini/FOSS-flatfile-alternative/assets/98195595/91783645-3b9f-4984-9f9e-1008e9571f4b)
10. ![image](https://github.com/enrimarini/FOSS-flatfile-alternative/assets/98195595/6049317b-cf5c-4b81-b3c0-65d263d81799)
11. **Conversion**: The application will convert the CSV file into an SQLite database file, ensuring data integrity throughout the process.
12. ![image](https://github.com/enrimarini/FOSS-flatfile-alternative/assets/98195595/dbcd9248-ca6b-4a81-af09-2d4030bbf801)
13. **Integrity Check**: After conversion, an integrity check is performed, validating the checksum for each record against the original CSV data. This message printout currently only shows inside the Python console but can be made to print to the tkinter GUI.
14. ![image](https://github.com/enrimarini/FOSS-flatfile-alternative/assets/98195595/a08ee873-cc03-4905-8fcb-33d37c48e6fc)


## Installation

- This app runs as a local fat client. You will need to use a Python IDE or compiler of your choice. Make sure you are running Python 3.x and you have the **tkinter** and SQLAlchemy packages installed in your Python environment.   
- The file `completed_script_with_checksumhashing.py`is what you need to compile to generate the fat client instance. This is the main monolithic script that generates the app once compiled. You can also compile it by calling the script name using WSL or your native linux environment, provided you have Python 3.x installed.
- The script `csvparsing_and_sqlitefile_creator.py` does NOT have SHA-256 checksum hashing validation. It needs to be compiled just the same as `completed_script_with_checksumhashing.py`. I made this script to make it easier for folks to implement the core app into their environment of choice. It runs faster due to the lack of the checksum hashing feature. 
- The script and `datatypedefinition_gui_v1.py` contains some core logic but no data validation. I made this to help others implement the drop-down menu feature that assigns the selected datatype to the SQLite db table. 
- The script `tkintergui_template_basic.py` contains the basic GUI skeleton layout of the app. Core logic does not exist here. I made this to make it easy for others to import the GUI layout and implementing it in some other environment of their choice.
