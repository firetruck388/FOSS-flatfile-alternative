import tkinter as tk
import csv
from tkinter import filedialog, messagebox, ttk
from sqlalchemy import create_engine, MetaData, Column, Integer, String, Float, Boolean, DateTime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
import uuid
from datetime import datetime
import hashlib


Base = declarative_base()

# SQLAlchemy data type mapping
sqlalchemy_data_types = {
    'integer': Integer,
    'string': String,
    'float': Float,
    'boolean': Boolean,
    'datetime': DateTime
}

# Global metadata instance
metadata = MetaData()

# Function to create the SQLAlchemy table definition
def create_table_definition(selected_data_types):
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")
    class_name = f"Record_{timestamp}"
    columns = {'__tablename__': f'data_{timestamp}',
               'id': Column(String, primary_key=True)}
    columns['checksum'] = Column(String)

    for header, data_type in selected_data_types.items():
        columns[header] = Column(sqlalchemy_data_types[data_type.lower()])

    # Dynamically create a new class for each table
    RecordClass = type(class_name, (Base,), columns)

    # Create the table in the metadata
    Base.metadata.create_all(metadata.bind)

    return RecordClass


# Function to perform a basic check of the table and data
def perform_integrity_check(session, RecordClass, csv_path, selected_data_types):
    try:
        # Retrieve all database records
        db_records = session.query(RecordClass).all()
        db_records_checksums = [record.checksum for record in db_records]
        print(f"Database has {len(db_records)} records with checksums: {db_records_checksums}")

        # Initialize a counter for CSV rows
        csv_row_count = 0

        # Read the CSV file and compare checksums
        with open(csv_path, 'r', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for csv_row in reader:
                csv_row_count += 1
                # Compute checksum for the row just read from CSV
                csv_checksum = calculate_checksum(csv_row, selected_data_types)
                print(f"CSV row: {csv_row}")
                print(f"CSV checksum: {csv_checksum}")

                # Check if the computed checksum is in the list of database checksums
                if csv_checksum in db_records_checksums:
                    print(f"Checksum {csv_checksum} found in database.")
                else:
                    print(f"Checksum {csv_checksum} NOT found in database.")
                    raise ValueError(f"Checksum mismatch detected for CSV row: {csv_row}")

        # Verify the row counts
        if csv_row_count != len(db_records):
            raise ValueError(f"Row count mismatch: CSV has {csv_row_count} rows, but the database has {len(db_records)} records.")
        else:
            print("Row counts match.")

        print("All records verified successfully.")

    except Exception as e:
        messagebox.showerror('Integrity Check Failed', f"An error occurred during integrity check: {e}")


def calculate_checksum(row, selected_data_types):
    # Ensure the keys are sorted so the order is consistent
    sorted_keys = sorted(selected_data_types)
    row_str = ','.join(str(row.get(attr, '')) for attr in sorted_keys)
    return hashlib.sha256(row_str.encode()).hexdigest()



# Function to parse the CSV and create the database
def parse_csv_and_create_database(selected_data_types):
    # Generate a datetime stamp for the database filename with milliseconds
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")[:17]  # Slice to get YYYYMMDDHHMMSSmmm
    database_filename = f"mydatabase_{timestamp}.db"

    # Create the SQLAlchemy engine and metadata object
    engine = create_engine(f'sqlite:///{database_filename}')
    metadata.bind = engine

    # Call the function to dynamically create a class mapped to the table
    RecordClass = create_table_definition(selected_data_types)

    # Create a session to interact with the database
    Session = sessionmaker(bind=engine)
    session = Session()

    # Read the CSV file and insert data
    with open(file_path.get(), 'r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # Print each row's values before insertion
            print(f"Inserting row with values: {row}")
            checksum = calculate_checksum(row, selected_data_types)
            record = RecordClass()  # Use the dynamically created RecordClass here
            record.id = str(uuid.uuid4())  # Assign a UUID for the primary key
            for header, value in row.items():
                # If the column is a datetime type, convert the string to a datetime object
                if selected_data_types[header] == 'datetime':
                    try:
                        # Assuming the datetime format in the CSV is '%H:%M:%S %m/%d/%Y'
                        # You'll need to adjust this format to match the one used in your CSV
                        row[header] = datetime.strptime(value, '%H:%M:%S %m/%d/%Y')
                    except ValueError as e:
                        raise ValueError(f"Error parsing datetime for column {header}: {e}")
                setattr(record, header, row[header])  # Set each column value
            record.checksum = checksum

            # Inside parse_csv_and_create_database function, right before session.add(record):
            print(f"Inserting: {[(header, getattr(record, header)) for header in selected_data_types]}")

            session.add(record)  # Add the record to the session


    # After insertion, perform a basic integrity check
    perform_integrity_check(session, RecordClass, file_path.get(), selected_data_types)

    # Commit the session and close the connection
    session.commit()
    session.close()

    # Inform the user that the database has been created
    messagebox.showinfo('Success', f'The SQLite database "{database_filename}" has been created successfully.')


# Function to open a file dialog and select a CSV file
def select_file():
    filetypes = (('CSV files', '*.csv'), ('All files', '*.*'))
    filename = filedialog.askopenfilename(title='Open a file', initialdir='/', filetypes=filetypes)
    if filename:
        file_path.set(filename)

# Function to confirm the file selection and proceed
def confirm_selection():
    if file_path.get():
        # File path is set, proceed with parsing (functionality to be added later)
        # For now, just show a confirmation message
        messagebox.showinfo('Confirmation', 'You have selected the file: ' + file_path.get())
        prepare_data_type_selection()
    else:
        messagebox.showwarning('Warning', 'Please select a CSV file first.')

# Function to read CSV headers and create data type selection interface
def prepare_data_type_selection():
    if file_path.get():
        try:
            # Read the CSV file and extract headers
            with open(file_path.get(), newline='') as csvfile:
                reader = csv.reader(csvfile)
                headers = next(reader)

            # Clear previous data types frame contents
            for widget in frame_data_types.winfo_children():
                widget.destroy()

            # Create label and dropdown for each header
            for i, header in enumerate(headers):
                label_header = tk.Label(frame_data_types, text=header, anchor='w')
                label_header.grid(row=i, column=0, sticky='ew', padx=5)

                data_type_var = tk.StringVar(value='string')  # default value
                data_type_selection = ttk.Combobox(frame_data_types, textvariable=data_type_var,
                                                   values=('datetime', 'string', 'integer', 'float', 'boolean'))
                data_type_selection.grid(row=i, column=1, padx=5, pady=5)
                data_types[header] = data_type_var

            # Add confirm button
            button_confirm_data_types = tk.Button(frame_data_types, text='Confirm Data Types', command=confirm_data_types)
            button_confirm_data_types.grid(row=len(headers), column=0, columnspan=2, pady=10)

        except Exception as e:
            messagebox.showerror('Error', f'An error occurred: {e}')

# Function to confirm the data type selections
def confirm_data_types():
    selected_data_types = {header: var.get() for header, var in data_types.items()}
    messagebox.showinfo('Data Types Selected', str(selected_data_types))
    # Call the function to parse the CSV and create the database using SQLAlchemy
    parse_csv_and_create_database(selected_data_types)


# Create the main application window
app = tk.Tk()
app.title('CSV to SQLite Converter')

# StringVar to store the path of the selected file
file_path = tk.StringVar(app)
data_types = {}  # Dictionary to store the data types selected for each column

# Frame for the file selection
frame_file_selection = tk.Frame(app, pady=10)
frame_file_selection.pack(fill='x', padx=15)

# Label, entry and button for file selection
label_file = tk.Label(frame_file_selection, text='Select CSV File:', anchor='w')
label_file.pack(side='left', padx=5)

entry_file = tk.Entry(frame_file_selection, textvariable=file_path, width=50)
entry_file.pack(side='left', expand=True, fill='x', padx=5)

button_browse = tk.Button(frame_file_selection, text='Browse', command=select_file)
button_browse.pack(side='right', padx=5)

# Frame for the confirm button
frame_confirm = tk.Frame(app, pady=10)
frame_confirm.pack(fill='x', padx=15)

button_confirm = tk.Button(frame_confirm, text='Confirm Selection', command=confirm_selection)
button_confirm.pack(side='right', padx=5)

# Frame for the data type selection (This should be defined here)
frame_data_types = tk.Frame(app)
frame_data_types.pack(fill='x', expand=True, padx=15)

# Run the application
app.mainloop()
