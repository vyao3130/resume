import os
import argparse



def main():
    parser = argparse.ArgumentParser()  
    parser.add_argument("--folder_name", "-f", type=str, help="Folder name to put files in.", required=True)
    args = parser.parse_args()
    # File names and their content
    files = {
        "ericssonEXP.txt": "Content of file1",
        "QueensTAEXP.txt": "Content of file2",
        "ticketseller.txt": "Content of file3",
        "imagteScraper.txt": "Content of file3",
    }

    # Get the current working directory (where the script is run)
    current_directory = os.getcwd() + args.folder_name
    os.mkdir(current_directory)

    # Create files and write content to them
    for file_name, content in files.items():
        with open(os.path.join(current_directory, file_name), 'w') as file:
            file.write(content)

    print(f"{len(files)} files have been created in the current directory.")


main()