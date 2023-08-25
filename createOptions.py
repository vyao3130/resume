import tkinter as tk
import csv
import os
import argparse
# reminder for csv file should look like: job description, resume entry title, resume entry
# the resume entry title is what the resume entry belongs to


REF_DESCR_ENTRY = 'REF_POINTS.csv'
RESUME_ENTRIES = ["Ericsson, image scraper, queensTA, ticket seller"]
RESUME_TO_FILE = {"Ericsson": "ericssonEXP.txt", "image scraper":"imageScraperPROJ.txt", "queensTA":"QueensTAEXP.txt", "ticket seller":"ticketsellerPROJ.txt"}
job_folder = "jobs"

def choose_resume_entry():
    # choose the specific resume entry to make
    print("Options are: ")
    for entry in RESUME_ENTRIES:
        print(f"- {entry} \n")
    resume_entry = input('Enter resume entry to create.\n')
    return resume_entry

def find_file(resume_entry):
    # find the file coresponding to the chosen resume entry, and have it edited by the resume
    for entry, file in RESUME_TO_FILE:
        if entry == resume_entry:
            read_file = file
            break
    return read_file


def create_options(resume_chosen):
    # get all the job descriptions relevant to create the resume entry
    job_references = {}
    csv_file = csv.reader(open(REF_DESCR_ENTRY, "r"), delimiter=",")
    for row in csv_file:
        if row[1] == resume_chosen:
            job_references.update({row[0]:row[2]})
    return job_references

def on_click(resume_text, path_to_edit):
    print(f"The text {resume_text} \n was added to the resume entry located in the file {path_to_edit}.")
    with open(path_to_edit, 'a') as file:
        file.write(resume_text)

# Create a window
root = tk.Tk()
root.title("Options UI")

def create_buttons(job_references, path_to_edit):
    job_text = list(job_references.keys())
    resume_text = list(job_references.values())
    for job_text, resume_text in job_references:
        button = tk.Button(root, text=job_text, command=lambda o=resume_text: on_click(o, path_to_edit))
        button.pack()


# Run the main loop
def main():
    # find resume entry to edit and the corresponding file
    resume_chosen = choose_resume_entry()
    file = find_file(resume_chosen)
    
    # find  the folder path
    parser = argparse.ArgumentParser()  
    parser.add_argument("--folder", "-fol", type=str, help="The path to the folder which contains files to be edited by the resume. Must" + \
                    " have:\n -exp \n -proj \n -skill(optional) in each file. ",required=True)
    args = parser.parse_args()

    # files = args.files
    folder = args.folder

    path_to_edit = os.path.join(folder, file)

    job_references = create_options(resume_chosen)
    create_buttons(job_references, path_to_edit)

    root.mainloop()
