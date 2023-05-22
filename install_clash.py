import os
import shutil
import subprocess


directory = "./clash"

# Get all files in the directory
files = os.listdir(directory)

# Sort files by name
sorted_files = sorted(files)

# Print the files with numbers
for i, file_name in enumerate(sorted_files, start=1):
    print(f"{i}. {file_name}")

# Prompt the user to select a file
while True:
    try:
        choice = int(input("Enter the number of the file you want to install: "))
        if 1 <= choice <= len(sorted_files):
            selected_file = sorted_files[choice - 1]
            print(f"You selected file: {selected_file}")
            break
        else:
            print("Invalid input. Please enter a valid number.")
    except ValueError:
        print("Invalid input. Please enter a valid number.")

# Copy the selected file to /usr/bin/ and rename it as "clash"
destination_dir = "/usr/bin/"
destination_file = "clash"
source_file = os.path.join(directory, selected_file)
destination_path = os.path.join(destination_dir, destination_file)

try:
    # Copy the file
    shutil.copy2(source_file, destination_path)
    print(f"File '{selected_file}' copied to '{destination_path}'.")

    # Set executable permissions using subprocess and sudo
    subprocess.run(["sudo", "chmod", "+x", destination_path])
    print(f"Executable permissions set for '{destination_path}'.")
except Exception as e:
    print(f"Error: {str(e)}")

print('done!')