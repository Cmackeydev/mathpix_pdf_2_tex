# mathpix_pdf_2_tex


## Hello World
This project permits to use the mathpix api in a more plug and play way (in my opinion).
It helps you convert a pdf to Latex or a every pdf in the current directory or a given directory

### Nota Bene
Im not a programming guru neither a python guru so the project is prone to error . Feel free to helps it to rise

### Creating Your virtual environment
As any new python3 project you shoud start by creating a virtualenv to not mess with system packages
`python3 -m venv`
Now you should activate it for further manipulations
`cd venv ; source ./bin/activate`

### Installing requirements
Install the required libraries via the command
`pip3 install -r requirements.txt`

### Configuring your credentials
YOu should add your APP_ID and APP_KEY in the config.ini file

### Enjoy
`python3 mathpix_pdf_to_tex -p <file_path>`
