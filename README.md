# resume
LaTeX template for my personal resume

Based off of [sb2nov/resume](https://github.com/sb2nov/resume/) and [jakegut/resume](https://github.com/jakegut/resume). Very close to the jakegut resume except it contains an additional link under project entries so you can put a
link to your project.

Has become more streamlined in order to become easier to use.

## make_folders.py
Creates a folder with textfiles that will be used as resume entries in make_resume.

## make_resume.py
Takes the text files within the folder it is run in and converts them into .tex format.

The script assumes that you'll want to process ALL the text files present, unless you run it with the -f flag and specify the files required. Will by default want 1 entry for experience, 1 entry for project, and 1 skill entry.




Then from the resulting .tex file run `pdflatex resume.tex` to get a pdf file. 
![Resume Preview](resume.png)
