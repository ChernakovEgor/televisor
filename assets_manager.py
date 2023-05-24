import os
import time

def generate_name(report_id: str, num: int):
    local_time = time.localtime()
    time_string = time.strftime("%S%M%H%d%m%Y", local_time)
    seconds = time.time()
    return f"{report_id}_{num}_{time_string}.pdf"

def save_pdf(name: str, data: bytes):
    path = f"data/pdfs/{name}"
    with open(path, 'wb') as f:
        f.write(data) 
        return path 

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
    print(generate_name('1', 1))
    print(generate_name('1', 1))

if __name__ == "__main__":
    main()
