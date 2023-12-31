import subprocess
# import pyperclip
import argparse
import sys
import shutil
import os
import json
from string import Template

parser = argparse.ArgumentParser()                                               

RESUME_NAME = "vyao_resume.tex"
PATH_TO_RESUME_BEGINNING = r"C:\Users\Vivian\Documents\resume\beginning_resume.txt"
PATH_TO_DEFAULT_SKILLS = r"C:\Users\Vivian\Documents\resume\REF_FOLDER\skills.txt"
PATH_TO_JSON_FILE_EXP = r"C:\Users\Vivian\Documents\resume\exp_file.json"

def convert_entry(file):
    """
    Converting text into a more usable format
    """
    new_bullet_points = []
    with open(file, 'r') as f:
        content = f.read()

    lines = content.split('\n')
    bullet_points = [line.strip('âˆ\xa0 ') for line in lines[0:] if line.strip()]
    for bullet in bullet_points:
        bullet = bullet.replace("%", "\%")
        new_bullet = bullet.replace("#", "\#")
        new_bullet_points.append(new_bullet)
    return {"bullet_points": new_bullet_points}


def format_exp(exp_file, folder):
    """
    Convert exp into usable for .tex format
    exp_file (string) : file name 
    folder (string) :  path to folder containing the exp file 
    """
    job_info = convert_entry(os.path.join(folder, exp_file))
    print(job_info)
    # create job bullet points
    bulletPoints = job_info.get("bullet_points")
    job_bulletPoints = ["\\resumeItem{" + bullet + "}" + "\n" for bullet in bulletPoints]

    # find job specific information from reference json file
    job_title = ""
    json_file = open(PATH_TO_JSON_FILE_EXP)
    json_data = json.load(json_file)

    # parse job specific information into tex format
    if exp_file in json_data.keys():
        job_ref_dict = json_data[exp_file]
        job_name =  job_ref_dict.get("job_title")
        job_time = job_ref_dict.get("time_span") 
        job_comp = job_ref_dict.get("company") 
        job_loc = job_ref_dict.get("location")

        job_title = "\t\t\\resumeSubheading \n" +  \
        f"\t\t\t$par {job_name}$bar$par {job_time}$bar \n" + \
        f"\t\t\t$par {job_comp}$bar$par {job_loc}$bar\n"

        # format job specific information and add the above bullet points
        job_string = Template(job_title).substitute(par="{", bar="}") +\
                      "\t\t\t " + "\\resumeItemListStart \n" + \
                      "\t\t\t\t" + "\t\t\t\t".join(job_bulletPoints)  +\
                      "\t\t\t" + "\\resumeItemListEnd \n"\
                        
        return job_string

    else:
        print(f"File {exp_file} doesnt fit in the EXP seaction.")
        return None

    

def format_proj(file, folder):
    """
    Convert project into usable for .tex format
    """
    job_info = convert_entry(os.path.join(folder, file))
    time = job_info.get("time")

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
    
    return (time, job_string)


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

def compile_pdf(tex_file, folder):
    try:
        # Running pdflatex on the specified tex file
        process = subprocess.run(f'pdflatex -output-directory {folder} {tex_file}', check=True)
        
        # If the return code is zero, the compilation was successful
        if process.returncode == 0:
            print(f"PDF has been successfully compiled from {tex_file} into {folder}")
        else:
            print(f"Error compiling PDF from {tex_file}")

    except FileNotFoundError:
        print("pdflatex not found. Please install TeX distribution.")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred during the compilation: {str(e)}")

def main():
    parser.add_argument("--folder", "-fol", type=str, help="The path to the folder which contains files to be formatted into the resume. Must" + \
                        " have:\n -exp \n -proj \n -skill(optional) in each file. ",required=False)
    args = parser.parse_args()

    folder = args.folder
    files = [file for file in os.listdir(folder) if os.path.isfile(os.path.join(folder, file))]

    # Sort through the files and take the ones with specific names for use
    formatted_experience = ""
    formatted_project = ""
    experience_tex = ""
    project_tex = ""
    formatted_skills = ""

    # iterate through the files
    for file in files:
        if "EXP" in file:
            time, formatted_experience = format_exp(file, folder)
            experience_tex = experience_tex + '\n' + formatted_experience
            print(f"The file {file} is being formatted for use in the experience section")
        elif "PROJ" in file:
            formatted_project = format_proj(file, folder)
            project_tex = project_tex + '\n' + formatted_project
            print(f"The file {file} is being formatted for use in the project section")
        elif "skill" in file:
            with open(os.path.join(folder, file), 'r') as source_file:
                formatted_skills = source_file.read()
            print(f"The file {file} is being formatted for use in the skill section")
        else:
            print(f"The file {file} is not recognized by this script.")

    # Error checking for no formatted input
    if not formatted_experience:
        print("There was no experience file found. Exiting...")
        sys.exit(1)
    if not formatted_project:
        print("There was no project file found. Exiting...")
        sys.exit(1)

    if not folder:
        new_file_path = os.getcwd() + RESUME_NAME
    else:
        new_file_path = os.path.join(folder, RESUME_NAME)

    shutil.copy(PATH_TO_RESUME_BEGINNING, new_file_path)

    # # adding skills at the end
    EDUCATION_FILE = r"C:/Users/Vivian/Documents/resume/education.txt"
    education = ""
    with open(EDUCATION_FILE, 'r') as f:
                education = f.read()
    # experience section
    texfile_string = "\n\\section{Work Experience } \n \t\\resumeSubHeadingListStart" + f"{experience_tex}" + \
    "\t\\resumeSubHeadingListEnd\n" + \
    "\n\\section{Projects }\n \t\t\\resumeSubHeadingListStart" + f"{project_tex}" +\
    "\t\t\\resumeSubHeadingListEnd\n\n" + f"{education}" + f"{formatted_skills}" +\
    "\n\n \\end{" + "document}"
    # formatted section
    # create_texfile.append(formatted_skills + "\n\n \\end{ document}") +  \
    
    # create_texfile = create_texfile.replace('#', '\\#')
    # write content to the file
    outputTex(texfile_string, str(new_file_path))
    print(f"Resume .tex file can be found at {new_file_path}")
    compile_pdf(new_file_path, folder)
    
if __name__ == "__main__":
    main()