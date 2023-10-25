# mathpix_pdf_2_tex


## Hello World
This project permits to use the mathpix api in a more plug and play way (in my opinion).
It helps you convert a pdf to Latex or a every pdf in the current directory or a given directory. It provides a zip files as output with the tex.file and  possibles images.

### Nota Bene
Im not a programming guru neither a python guru so the project is prone to error . Feel free to helps it to rise

## Setup

### Creating Your virtual environment
As any new python3 project you shoud start by creating a virtualenv to not mess with system packages

```python3 -m venv```

Now you should activate it for further manipulations

`cd venv ; source ./bin/activate`

### Installing requirements
Install the required libraries via the command

`pip3 install -r requirements.txt`

### Configuring your credentials
You should add your APP_ID and APP_KEY in the config.ini file
``` 
[API]
endpoint = https://api.mathpix.com/v3

[Credentials]
APP_ID = <your_APP_ID>
APP_KEY = <your_APP_KEY>
```

## Example usage
``` Bash
usage: pdf_to_tex_Mathpix.py [-h] [-p P]

options:
  -h, --help  show this help message and exit
  -p P        Path of the pdf file or the folder of pdf(s) you want to convert
 ```

 ### Note
 This scripts take the the pdf provided via the `-p` option or scans The paths provided via the `-p` options for pdf(s). If any path are provided it scans for the current directory.

 It deletes the data on the server after downloading the zip files. you can prevent this by commentig the call of the function `delete_on_server()` on line 99.
### Enjoy
`python3 mathpix_pdf_to_tex -p <file_path>`
