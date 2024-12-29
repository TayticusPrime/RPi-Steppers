import tkinter as tk
import serial
import struct
import time

# Set up serial connection (replace with your correct COM port)
arduino = serial.Serial('COM3', 9600, timeout=1)

# Set up the Tkinter GUI
root = tk.Tk()
root.title("Arduino Communication")

# Define the GUI elements
frequency_label = tk.Label(root, text="Frequency (Hz):")
frequency_label.grid(row=0, column=0, padx=10, pady=10, sticky='w')
frequency_entry = tk.Entry(root)
frequency_entry.grid(row=0, column=1, padx=10, pady=10, sticky='e')
frequency_entry.insert(0, "1046.50")  # Default value for frequency

duration_label = tk.Label(root, text="Duration (s):")
duration_label.grid(row=1, column=0, padx=10, pady=10, sticky='w')
duration_entry = tk.Entry(root)
duration_entry.grid(row=1, column=1, padx=10, pady=10, sticky='e')
duration_entry.insert(0, "5.0")  # Default value for duration

mode_label = tk.Label(root, text="Mode:")
mode_label.grid(row=2, column=0, padx=10, pady=10, sticky='w')

# Mode drop-down menu
mode_values = ["OFF", "ON", "PULSE", "STANDARD MODE", "FLIP-FLOP MODE", "ALL OFF"]
mode_var = tk.StringVar(root)
mode_var.set(mode_values[2])  # Default value set to "PULSE"
mode_menu = tk.OptionMenu(root, mode_var, *mode_values)
mode_menu.grid(row=2, column=1, padx=(10, 20), pady=10, sticky='e', ipadx=5)  # Right-aligned with margin

pin_id_label = tk.Label(root, text="Pin ID:")
pin_id_label.grid(row=3, column=0, padx=10, pady=10, sticky='w')

# Pin ID drop-down menu
pin_id_values = [1, 2, 3, 4]
pin_id_var = tk.StringVar(root)
pin_id_var.set(pin_id_values[0])  # Default value
pin_id_menu = tk.OptionMenu(root, pin_id_var, *pin_id_values)
pin_id_menu.grid(row=3, column=1, padx=(10, 20), pady=10, sticky='e', ipadx=5)  # Right-aligned with margin

# Display box for incoming serial data
display_box = tk.Text(root, height=10, width=40)
display_box.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

# Function to clear the display box
def clear_display():
    display_box.delete(1.0, tk.END)

# Function to send data to Arduino (only when "Send" button is clicked)
def send_data():
    try:
        # Get values from the drop-downs and entry fields
        pin_id = int(pin_id_var.get())  # Pin ID from drop-down menu
        mode_str = mode_var.get()  # Mode from drop-down menu
        
        # Convert mode to corresponding integer value
        if mode_str == "OFF":
            mode = 0
        elif mode_str == "ON":
            mode = 1
        elif mode_str == "PULSE":
            mode = 2
        elif mode_str == "ALL OFF":
            mode = 3
        elif mode_str == "STANDARD MODE":
            mode = 4
        elif mode_str == "FLIP-FLOP MODE":
            mode = 5
        else:
            print("Invalid mode selected.")
            return

        frequency = float(frequency_entry.get())  # Frequency as float
        duration = float(duration_entry.get())  # Duration as float

        # Pack the data into bytes (B is unsigned byte, f is float)
        packed_data = struct.pack('B B f f', pin_id, mode, frequency, duration)

        # Debugging: Print the packed data (raw bytes) to the console
        print("Packed Data (Raw Bytes):", packed_data)

        # Send data to Arduino (only once when button is clicked)
        arduino.write(packed_data)

        # Print confirmation
        print("Data sent to Arduino.")
        
    except ValueError:
        print("Invalid input. Please check the values entered.")

# Function to read data from Arduino (this will not send data)
def read_from_arduino():
    if arduino.in_waiting > 0:
        # Read raw bytes (do not assume UTF-8 text format)
        raw_data = arduino.read(arduino.in_waiting)

        # Convert raw bytes to string (handle encoding issues with 'ignore' mode)
        try:
            data = raw_data.decode('utf-8', errors='ignore').strip()  # Try to decode as UTF-8
            if data:
                display_box.insert(tk.END, data + '\n')  # Display the serial data
                display_box.yview(tk.END)  # Scroll to the end
        except UnicodeDecodeError:
            print(f"Error decoding data: {raw_data}")

    # Call the read function again after 100ms (non-blocking)
    root.after(100, read_from_arduino)

# Set up the "Send" and "Clear" buttons
send_button = tk.Button(root, text="Send", command=send_data, width=15)
send_button.grid(row=4, column=0, padx=10, pady=10)

clear_button = tk.Button(root, text="Clear", command=clear_display, width=15)
clear_button.grid(row=4, column=1, padx=10, pady=10)

# Start reading data from Arduino (this function runs periodically)
read_from_arduino()

# Run the GUI loop
root.mainloop()
