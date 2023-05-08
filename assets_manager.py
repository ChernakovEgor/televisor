import os
import logging
from io import BytesIO
import filecmp
import time

data_dir = 'data/'
pdf_dir = 'data/pdfs/'
icon_dir = 'data/icons/'

def generate_name(report_id: str, num: int):
    local_time = time.localtime()
    time_string = time.strftime("%S%M%H%d%m%Y", local_time)
    seconds = time.time()
    return f"{report_id}_{num}_{time_string}.pdf"

def save_pdf(name: str, data: bytes):
    pdfs = os.listdir("data/pdfs/")
    path_to_write = f"data/pdfs/{name}"
    with open(path_to_write, 'wb') as f:
        f.write(data) 
    for pdf in pdfs:
        comparison = filecmp.cmp(path_to_write, f"data/pdfs/{pdf}",  shallow=False)
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
    if os.path.exists(f"data/pdfs/{name}"):
        os.remove(f"data/pdfs/{name}")

def get_pdf(name: str):
    with open(f"data/pdfs/{name}", 'rb') as f:
       return f.read()

def save_icon(name: str, data: bytes):
    path = f"data/icons/{name}"
    with open(path, 'wb') as f:
        f.write(data)
        return path

def get_icon(name: str):
    with open(f"data/icons/{name}", 'rb') as f:
       return f.read()

def delete_icon(name):
    if os.path.exists(f"data/icons/{name}"):
        os.remove(f"data/icons/{name}")

def main():
    clean_up(['dummy.pdf'])

if __name__ == "__main__":
    main()
