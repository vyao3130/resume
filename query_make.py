"""
    Write queries based off the files in a given folder. The names in the given folder are already
    assumed and used- any other folders will be ignored.
"""
import os
import argparse
import shutil
import sys
import pyperclip
import json

PATH_TO_JSON_FILE_EXP = r"C:\Users\Vivian\Documents\resume\exp_file.json"

def unpack_file(file):
    """
    Unpack json file.

    """
    with open(file, 'r') as f:
        content = json.load(f)
    return content

def convert_entry(file):
    """
    Converting text into a more usable format
    """
    with open(file, 'r') as f:
        content = f.read()

    lines = content.split('\n')
    bullet_points = [line.strip('âˆ\xa0 ') for line in lines[0:] if line.strip()]
    return {"bullet_points": bullet_points}

def read_file(file):
    """
    read file lol
    """
    with open(file, 'r') as f:
        content = f.read()
    
    return content

def main():
    # parser.add_argument("--files", "-f", type=str, nargs='*', help="The files to be formatted into the resume. Must" + \
    #                     " have:\n -exp \n -proj \n -skill(optional) in each file. ",required=False)
    parser = argparse.ArgumentParser()        
    parser.add_argument("--folder", "-f", type=str, help="Write a chatgpt query based off the files in a given folder.",required=False)
    args = parser.parse_args()
    # files = args.files
    folder = args.folder
    
    query_string = "Pretend to be an advisor helping a recent graduate apply to a junior developer position. Their resume contains the following: \n"

    # No files specified by user, default to ALL files in the folder
    # if not files:
    files = [file for file in os.listdir(folder) if os.path.isfile(os.path.join(folder, file))]
    expDict = unpack_file(PATH_TO_JSON_FILE_EXP)
    job_posting = ""

    for file in files:
        if file in expDict:
            job_title = (expDict.get(file)).get("job_title")
            query_string = query_string + f"Job Title: {job_title} \n"

            experience = convert_entry(os.path.join(folder, file)).get("bullet_points")
            query_string = query_string + f"{experience} \n"
        if file == "jobposting.txt":
            job_posting = read_file(os.path.join(folder, file))
        



    
    query_string = query_string + """Created and deployed an online customer-to-customer ticket selling system. 

            ∠ Developed robust unit tests using Selenium for frontend and backend systems, ensuring comprehensive test coverage
            ∠ Leveraged Flask and SQLite, to enhance user experience and optimize sales operations
            ∠ Contributed to the frontend and backend codebase within a Scrum framework, driving collaborative development and continuous improvement

            Education:
            {Bachelor of Computing (Honours), Specialization in Software Development 
            """
    
    if job_posting:
        query_string = query_string + "The job posting the recent graduate is applying to is the following: " + f"{job_posting}"
    else:
        print("There needs to be a job_posting.txt file so we can make a proper query.")
        sys.exit(1)
    
    pyperclip.copy(query_string)
    print(f"The following has been copied: \n {query_string} \n end of string copied")
    print(f" Following is commong queries used after: \n Using the given advice, as the advisor, edit the applicant's resume for them in the same format without using an objective statement")

if __name__ == "__main__":
    main()

