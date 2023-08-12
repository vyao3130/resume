import os
import argparse
import shutil
import os

JOB_FOLDER = r"C:\Users\Vivian\Documents\resume\jobs"
REF_FOLDER = r"C:\Users\Vivian\Documents\resume\REF_FOLDER"


def copy_folder(src_folder, dest_folder):
    if not os.path.exists(src_folder):
        print(f"Source folder {src_folder} does not exist.")
        return

    if os.path.exists(dest_folder):
        print(f"Destination folder {dest_folder} already exists.")
        return

    try:
        shutil.copytree(src_folder, dest_folder)
        print(f"Copied {src_folder} to {dest_folder}")
    except Exception as e:
        print(f"An error occurred: {e}")



def main():
    parser = argparse.ArgumentParser()  
    parser.add_argument("--folder_name", "-f", type=str, help="Folder name to put files in.", required=True)
    args = parser.parse_args()

    # Get the job folder to put the files
    new_directory = os.path.join(JOB_FOLDER, args.folder_name)

    copy_folder(REF_FOLDER, new_directory)


main()