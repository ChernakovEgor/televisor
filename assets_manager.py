import os
import logging
import filecmp
import time

data_dir = 'data/'
pdf_dir = 'data/pdfs/'
icon_dir = 'data/icons/'

def generate_name(report_id: str, num: int):
    local_time = time.localtime()
    time_string = time.strftime("%S%M%H%d%m%Y", local_time)
    # seconds = time.time()
    return f"{report_id}_{num}_{time_string}.pdf"

def save_pdf(name: str, data: bytes):
    pdfs = os.listdir(pdf_dir)
    path_to_write = pdf_dir + name
    with open(path_to_write, 'wb') as f:
        f.write(data) 
    for pdf in pdfs:
        comparison = filecmp.cmp(path_to_write, pdf_dir + pdf,  shallow=False)
        if comparison:
            os.remove(path_to_write)
            return pdf
    return name

def clean_up(pdfs_in_table):
    pdfs_on_disk = os.listdir(pdf_dir)
    for pdf in pdfs_on_disk:
        if pdf not in pdfs_in_table:
            logging.info(f"Deleting pdf {pdf}")
            delete_pdf(pdf)
    

def delete_pdf(name):
    if os.path.exists(pdf_dir + name):
        os.remove(pdf_dir + name)

def get_pdf(name: str):
    with open(pdf_dir + name, 'rb') as f:
       return f.read()

def save_icon(name: str, data: bytes):
    icons = os.listdir(icon_dir)
    path_to_write = icon_dir + name
    with open(path_to_write, 'wb') as f:
        f.write(data) 
    for icon in icons:
        comparison = filecmp.cmp(path_to_write, icon_dir + icon, shallow=False)
        if comparison:
            os.remove(path_to_write)
            return icon
    return name

def get_icon(name: str):
    with open(icon_dir + name, 'rb') as f:
       return f.read()

def delete_icon(name):
    if os.path.exists(icon_dir + name):
        os.remove(icon_dir + name)

def main():
    save_pdf('testing', b'999999999')

if __name__ == "__main__":
    main()
