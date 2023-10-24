#Autor : Mackey CHARLES
#Abstract : This script helps to convert a pdf into latex format using the mathpix api

from argparse import ArgumentParser
from alive_progress import alive_bar
import time
from os import path,listdir
from re import search
import requests
import json

def is_file(obj):
    return path.isfile(obj)

def is_pdf(obj):
    return search('\.pdf$',obj)

def convert_to_tex(obj):
    options = {
        "conversion_formats": {"docx": False, "tex.zip": True},
        "math_inline_delimiters": ["$", "$"],
        "rm_spaces": True
                }
    request = requests.post('https://api.mathpix.com/v3/pdf',headers=header,data={"options_json":json.dumps(options)},files={"file":open(obj,"rb")})
    data = json.loads(request.text.encode('utf8'))
    return data

def checking_status(data_obj):
    if 'pdf_id' in data_obj:
        
        
        i = 0
        while i<10:
            request =requests.get(f"https://api.mathpix.com/v3/pdf/{data_obj['pdf_id']}",headers=header) 
            response_data = json.loads(request.text.encode('utf8')) 
            if "status" in response_data:
                if response_data['status'] == "completed": return True
                elif response_data['status']=='error':return False
                else: pass
            else: return False
            i +=1
        return False

def checking_conv(data_obj):
    i = 0
    while(i<10):
        request =requests.get(f"https://api.mathpix.com/v3/converter/{data_obj['pdf_id']}",headers=header)
        response_data =json.loads(request.text.encode('utf8'))
        if 'status' in response_data:
            if response_data['status']=="completed": return True
            elif response_data['status']=="error":return False
    
    return False

def download_zip(data_obj,pdf):
    request=requests.get(f"https://api.mathpix.com/v3/pdf/{data_obj['pdf_id']}.tex",headers=header)
    with open(pdf.replace('.pdf','.tex.zip'),'wb') as file:
        file.write(request.content)
    

def main():
    if not args.p : directory = '.'
    elif path.isdir(args.p) : directory= args.p
    else : directory = None
    if not directory: list_of_files = [args.p]
    else:
        path_of_files = [directory+'/'+obj for obj in listdir(directory)]
        list_of_files = list(filter(is_file,path_of_files))
        
    list_of_pdf = list(filter(is_pdf,list_of_files))

    quantity = len(list_of_pdf)

    with alive_bar(quantity) as bar:
        for pdf in list_of_pdf:
            conv_data  = convert_to_tex(pdf)
            if checking_status(conv_data):
                if checking_conv(conv_data): download_zip(conv_data,pdf)

            bar()

if __name__=="__main__":
    parser  = ArgumentParser()
    parser.add_argument("APP_ID",help='The APP_ID provided by mathpix')
    parser.add_argument("APP_KEY" , help="The APP_KEY provided by mathpix")
    parser.add_argument("-p",help='Path of the pdf file or the folder of pdf(s) you want to convert')
    args = parser.parse_args()
    header = {
           "app_id": args.APP_ID,
            "app_key": args.APP_KEY, 
            }

    main()

