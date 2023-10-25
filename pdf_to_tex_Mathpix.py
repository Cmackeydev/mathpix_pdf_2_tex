#Autor : Mackey CHARLES
#Abstract : This script helps to convert a pdf into latex format using the mathpix api

from argparse import ArgumentParser
from configparser import ConfigParser
from alive_progress import alive_bar
import time
from os import path,listdir
from re import search
import requests
import json
import traceback

def is_file(obj):
    return path.isfile(obj)

def is_pdf(obj):
    return search('\.pdf$',obj)

def pdf_sent(request_rep):
    if request_rep is None : return False
    if 'pdf_id' in request_rep: return True
    return False

def request_status(request_rep):
    if 'status' not in request_rep:return None
    if request_rep['status']=='completed':return True
    elif request_rep['status']=='error':return False
    return None

def request_checker(request_str):
    for i in range(10):
        time.sleep(1)
        try:
            request =requests.get(f"{request_str}",headers=header) 
            if request_status(json.loads(request.text.encode('utf8'))):return True
        except Exception:return False
    return False

def checking_status(data_obj):
        return request_checker(f"{endpoint_base}/pdf/{data_obj['pdf_id']}")

def checking_conv(data_obj):
    return request_checker(f"{endpoint_base}/converter/{data_obj['pdf_id']}")

def delete_on_server(data_obj):
    requests.delete(f"{endpoint_base}/pdf/{data_obj['pdf_id']}",headers=header)

def pdf_to_convert(access_path):
    if not access_path : directory = '.'
    elif path.isdir(access_path) : directory= access_path
    else : directory = None
    if not directory: list_of_files = [access_path]
    else:
        path_of_files = [directory+'/'+obj for obj in listdir(directory)]
        list_of_files = list(filter(is_file,path_of_files))
    return list(filter(is_pdf,list_of_files))

def convert_to_tex(obj):
    options = {
        "conversion_formats": {"docx": False, "tex.zip": True},
        "math_inline_delimiters": ["$", "$"],
        "rm_spaces": True
                }
    try:
        request = requests.post(f'{endpoint_base}/pdf',headers=header,data={"options_json":json.dumps(options)},files={"file":open(obj,"rb")})
    except Exception:
        return None
    return json.loads(request.text.encode('utf8'))



def download_zip(data_obj,pdf):
    try:
        request=requests.get(f"{endpoint_base}/pdf/{data_obj['pdf_id']}.tex",headers=header)
        with open(pdf.replace('.pdf','.tex.zip'),'wb') as file:
            file.write(request.content)
        return True
    except Exception: return False
    
def main():
    list_of_pdf = pdf_to_convert(args.p)
    quantity = len(list_of_pdf)
    failed_conversion = []

    with alive_bar(quantity) as bar:
        for pdf in list_of_pdf:
            conv_data  = convert_to_tex(pdf)
            if pdf_sent(conv_data):
                if checking_status(conv_data):
                    if checking_conv(conv_data): 
                        download_zip(conv_data,pdf)
                        delete_on_server(conv_data)
                    else:failed_conversion.append(pdf)
                else:failed_conversion.append(pdf)
            else: failed_conversion.append(pdf)
            bar()

    print('\t\t Conversion Status')
    for pdf in list_of_pdf:
        status = "failed" if pdf in failed_conversion else "succed"
        print(f" \t\t\t {pdf} : {status}")

if __name__=="__main__":
    parser  = ArgumentParser()
    parser.add_argument("-p",help='Path of the pdf file or the folder of pdf(s) you want to convert')
    args = parser.parse_args()
    config = ConfigParser()
    config.read('config.ini')
    endpoint_base = config['API']['endpoint']
    header = {
           "app_id": config['Credentials']['APP_ID'],
            "app_key": config['Credentials']['APP_KEY'], 
            }

    main()

