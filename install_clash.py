import os
import shutil
import subprocess


def select_file(directory: str) -> str:
    # Get all files in the directory
    files = os.listdir(directory)

    # Sort files by name
    sorted_files = sorted(files)

    # Print the files with numbers
    for i, file_name in enumerate(sorted_files, start=1):
        print(f"{i}. {file_name}")

    selected_file = ''

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

    return selected_file


def install_clash(directory: str, selected_file: str) -> bool:
    if select_file == '':
        print("No file selected. Exiting...")
        return False

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
        return True
    except Exception as e:
        print(f"Error: {str(e)}")
        return False


if __name__ == "__main__":
    directory = './clash'

    selected_file = select_file(directory)
    if install_clash(directory, selected_file):
        print('done!')
    else:
        print('fail!')
