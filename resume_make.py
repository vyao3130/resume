import subprocess
import pyperclip
import argparse
import sys
import shutil
import os


parser = argparse.ArgumentParser()                                               

RESUME_NAME = "resume.tex"
PATH_TO_RESUME_BEGINNING = r"C:\Users\Vivian\Documents\resume\beginning_resume.txt"
PATH_TO_DEFAULT_SKILLS = r"C:\Users\Vivian\Documents\resume\skills.txt"

def convert_entry(file):
    """
    Converting text into a more usable format
    """
    with open(file, 'r') as f:
        content = f.read()

    lines = content.split('\n')
    bullet_points = [line.strip('âˆ\xa0 ') for line in lines[0:] if line.strip()]
    return {"bullet_points": bullet_points}


def format_exp(exp_file, folder):
    """
    Convert exp into usable for .tex format
    """
    job_info = convert_entry(os.path.join(folder, exp_file))
    print(job_info)
    bulletPoints = job_info.get("bullet_points")
    job_bulletPoints = ["\\resumeItem{" + bullet + "}" + "\n" for bullet in bulletPoints]
    job_title = ""

    if "ericsson" in exp_file:
        job_title = "\t\t\\resumeSubheading \n" +  \
        "\t\t\t{5G VERIFICATION SOFTWARE DEVELOPER}{Sept 2021 - Sept 2022} \n" + \
        "\t\t\t{Ericssson }{Ottawa}\n"
    elif "TA" in exp_file:
        job_title = "\t\t\\resumeSubheading \n" +  \
        "\t\t\t{PROGRAMMING PARADIGMS TEACHING ASSISTANT}{Sept 2022 - Jan 2023} \n" + \
        "\t\t\t{Queen\'s University}{Kingston}\n"  
    else:
        print(f"File {exp_file} doesnt fit in the EXP section.")

    job_string = job_title +\
                      "\t\t\t " + "\\resumeItemListStart \n" + \
                      "\t\t\t\t" + "\t\t\t\t".join(job_bulletPoints)  +\
                      "\t\t\t" + "\\resumeItemListEnd \n"
    
    cleaned_string = job_string.replace('#', '\\#')
    return cleaned_string

def format_proj(file, folder):
    """
    Convert project into usable for .tex format
    """
    job_info = convert_entry(os.path.join(folder, file))

    bulletPoints = job_info.get("bullet_points")
    job_bulletPoints = ["\\resumeItem {" + bullet + "}" + "\n" for bullet in bulletPoints]

    if "imageScraper" in file:
        job_title = "\t\t\\resumeProjectHeading \n" +  \
        "\t\t\t{\\textbf{Photosaver (IN PROGRESS)} $|$ \emph{Python, Flask, React, PostgreSQL, Docker}}{June 2020 -- Present} \n" + \
        "\t\t\t{ https://github.com/electronAccelerator/PhotoSaver}\n"
    
    if "ticket" in file:
        job_title = "\t\t\\resumeProjectHeading \n" +  \
        "\t\t\t{\\textbf{TICKET SELLER (COMPLETED)} $|$ \emph{Python, Flask, React, PostgreSQL, Docker}}{June 2020 -- Present} \n" + \
        "\t\t\t{ https://hub.docker.com/repository/docker/cisc327group42/brain-bench}\n"

    job_string = job_title +\
                      "\t\t\t " + "\\resumeItemListStart \n" + \
                      "\t\t\t\t" + "\t\t\t\t".join(job_bulletPoints)  +\
                      "\t\t\t" + "\\resumeItemListEnd \n"
    
    cleaned_string = job_string.replace('#', '\\#')
    return cleaned_string


# def format_skills(file):
#     """
#     Convert skills into usable for .tex format
#     """
#     if not file:
#         # path to constant file.
#         input_file_name = "default_skills.tex"
#     else:
#         input_file_name = input_file
#     # Define the names of the input and output files
#     file = 'input_file.txt'
#     output_file_name = 'resume.tex'

#     with open(input_file_name, 'r') as input_file:
#         content = input_file.read()
#         with open(output_file_name, 'w') as output_file:
#             output_file.write(content)

#     print(f'Content from {input_file_name} has been copied to {output_file_name}.')

    
def outputTex(content, destination):
    with open(destination, 'a') as output_file:
            output_file.write(content)

def main():
    # parser.add_argument("--files", "-f", type=str, nargs='*', help="The files to be formatted into the resume. Must" + \
    #                     " have:\n -exp \n -proj \n -skill(optional) in each file. ",required=False)
    parser.add_argument("--folder", "-fol", type=str, help="The path to the folder which contains files to be formatted into the resume. Must" + \
                        " have:\n -exp \n -proj \n -skill(optional) in each file. ",required=False)
    args = parser.parse_args()

    # files = args.files
    folder = args.folder
    

    # No files specified by user, default to ALL files in the folder
    # if not files:
    files = [file for file in os.listdir(folder) if os.path.isfile(os.path.join(folder, file))]

    # Sort through the files and take the ones with specific names for use
    formatted_experience = ""
    format_skills = ""
    formatted_project = ""
    experience_tex = ""
    project_tex = ""
    formatted_skills = ""

    print(files)
    for file in files:
        if "EXP" in file:
            formatted_experience = format_exp(file, folder)
            experience_tex = experience_tex + '\n' + formatted_experience
            print(f"The file {file} is being formatted for use in the experience section")
        elif "PROJ" in file:
            formatted_project = format_proj(file, folder)
            project_tex = project_tex + '\n' + formatted_project
            print(f"The file {file} is being formatted for use in the project section")
        # elif "skill" in file:
        #     formatted_skills = format_skills(file)
        #     print(f"The file {file} is being formatted for use in the skill section")
        else:
            print(f"The file {file} is not recognized by this script.")

    # Error checking for no formatted input
    if not formatted_experience:
        print("There was no experience file found. Exiting...")
        sys.exit(1)
    if not formatted_project:
        print("There was no project file found. Exiting...")
        sys.exit(1)

    print(formatted_experience)
    # create tex file with beginning

    if not folder:
        new_file_path = os.getcwd() + RESUME_NAME
    else:
        new_file_path = os.path.join(folder, RESUME_NAME)

    shutil.copy(PATH_TO_RESUME_BEGINNING, new_file_path)

    # experience section
    create_texfile = "\n\\section{Education } \n \t\\resumeSubHeadingListStart" + f"{experience_tex}" + \
    "\t\\resumeSubHeadingListEnd\n" + \
    "\n\\section{Projects }\n \t\t\\resumeSubHeadingListStart" + f"{project_tex}" +\
    "\t\t\\resumeSubHeadingListEnd" + \
    "\n\n \\end{" + "document}"
    # formatted section
    # create_texfile.append(formatted_skills + "\n\n \\end{ document}") +  \

    # write content to the file
    outputTex(create_texfile, new_file_path)
    print(f"Resume file can be found at {new_file_path}")

    
if __name__ == "__main__":
    main()