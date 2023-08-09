import subprocess
import pyperclip
import argparse
import sys
parser = argparse.ArgumentParser()                                               



def read_file_as_string(file_path):
    with open(file_path, 'r') as file:
        file_contents = file.read()
    return file_contents

# Example usage
file_path = args.file
file_string = read_file_as_string(file_path)
print(file_string)


def convert_entry(file):
    """
    Converting text into a more usable format
    """
    lines = file.split('\n')
    title = lines[0]
    bullet_points = [line.strip('âˆ\xa0 ') for line in lines[1:] if line.strip()]
    return {"job_title":title, "bullet_points": bullet_points}

def format_exp(exp_file):
    """
    Convert exp into usable for .tex format
    """
    job_info = convert_entry(exp_file)
    bulletPoints = job_info.get("bullet_points")
    job_bulletPoints = ["\\resumeItem \{" + bullet + "\}" + "\n" for bullet in bulletPoints]

    if "ericsson" in exp_file:
        job_title = "\t\t\\resumeSubheading \n" +  \
        "\t\t\t{5G VERIFICATION SOFTWARE DEVELOPER}{Sept 2021 - Sept 2022} \n" + \
        "\t\t\t{Ericssson }{Ottawa} \n"
    
    if "TAship" in exp_file:
        job_title = "\t\t\\resumeSubheading \n" +  \
        "\t\t\t{PROGRAMMING PARADIGMS TEACHING ASSISTANT}{Sept 2022 - Jan 2023} \n" + \
        "\t\t\t{Queen\'s University}{Kingston} \n"

    job_string = "\t\t" + job_title + \
                      "\t\t\t " + job_info.get("job_title") + "\n" + \
                      "\t\t\t " + "\\resumeItemListStart \n" + \
                      "\t\t\t\t" + "\t\t\t\t".join(job_bulletPoints)  +\
                      "\t\t\t" + "\\resumeItemListEnd \n"
    
    return job_string

def format_proj(proj_file):
    """
    Convert project into usable for .tex format
    """


def format_skills(input_file):
    """
    Convert skills into usable for .tex format
    """
    if not file:
        # path to constant file.
        input_file_name = "default_skills.tex"
    else:
        input_file_name = input_file
    # Define the names of the input and output files
    input_file = 'input_file.txt'
    output_file_name = 'resume.tex'

    with open(input_file_name, 'r') as input_file:
        content = input_file.read()
        with open(output_file_name, 'w') as output_file:
            output_file.write(content)

    print(f'Content from {input_file_name} has been copied to {output_file_name}.')

    
def outputTex(content):
    with open('resume.tex', 'w') as output_file:
            output_file.write(content)

def main():
    parser.add_argument("--files", "-f", type=str, nargs='*', help="The files to be formatted into the resume. Must" + \
                        " have:\n -exp \n -proj \n -skill(optional) in each file. ",required=True)
    args = parser.parse_args()
    files = args.files

    for file in files:
        if "exp" in file:
            formatted_experience = format_exp(file)
            experience_tex = experience_tex + '\n' + formatted_experience
            print(f"The file {file} is being formatted for use in the experience section")
        elif "proj" in file:
            formatted_project = format_proj(file)
            project_tex = project_tex + '\n' + formatted_project
            print(f"The file {file} is being formatted for use in the project section")
        elif "skill" in file:
            formatted_skills = format_skills(file)
            
        else:
            print(f"The file {file} is not recognized by this script.")
            sys.exit(0)
    
    if not formatted_experience:
        print("There was no experience file found. Exiting...")
        sys.exit(1)
    if not formatted_project:
        print("There was no project file found. Exiting...")

    # create tex file
    outputTex(beginning)
    create_texfile = "\\section{Education } \n \t\\resumeSubHeadingListStart \n".append(experience_tex)
    create_texfile.append("\t\\resumeSubHeadingListEnd")
    create_texfile.append("\\section{Projects }\n \t\t\\resumeSubHeadingListStart \n".append(project_tex))
    create_texfile.append("\t\t\\resumeSubHeadingListEnd")
    create_texfile.append(formatted_skills)

    outputTex(create_texfile)

    
if __name__ == "__main__":
    main()