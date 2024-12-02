import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from gtts import gTTS
import PyPDF2
import os

# pdf'ten metne çevirme fonksiyonu

def pdf_to_text(pdf_path):
    text = ""
    with open(pdf_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        num_pages = len(pdf_reader.pages)

        for page_num in range(num_pages):
            page = pdf_reader.pages[page_num]
            text += page.extract_text()

    return text

# metni sese çevirme fonksiyonu

def text_to_speech(text, output_file, lang='en', gender='female'):
    language_map = {
        'en': {'man': 'en-us', 'woman': 'en'},
        'tr': {'man': 'tr', 'woman': 'tr'}
    }

    lang_code = language_map[lang][gender]
    tts = gTTS(text=text, lang=lang_code, slow=False, tld='com', lang_check=False)
    tts.save(output_file)

# dosya adini kontrol edip yeniden adlandırma

def check_and_rename(file_path):
    file_name, file_extension = os.path.splitext(file_path)
    count = 1
    new_file_path = f"{file_name} ({count}){file_extension}"

    while os.path.exists(new_file_path):
        count += 1
        new_file_path = f"{file_name} ({count}){file_extension}"

    return new_file_path

# main dönüştürme

def main(pdf_path, lang='en', gender='female'):
    pdf_filename = os.path.splitext(os.path.basename(pdf_path))[0]
    output_file = f"{pdf_filename}.mp3"
    output_file = check_and_rename(output_file)

    text = pdf_to_text(pdf_path)
    text_to_speech(text, output_file, lang, gender)

# dosya yolunu belirtme-seçme fonksiyonu

def open_file_dialog():
    file_path = filedialog.askopenfilename(title="PDF Dosyası Seç", filetypes=[("PDF files", "*.pdf")])
    entry_path.delete(0, tk.END)
    entry_path.insert(0, file_path)

# sesli dönüştürme fonksiyonu (ses ve dil seçme)

def convert_to_audio():
    pdf_path = entry_path.get()
    selected_language = language_var.get()
    selected_gender = gender_var.get()
    main(pdf_path, lang=selected_language, gender=selected_gender)

# tkinter penceresi dönüşüm başlatma

root = tk.Tk()
root.title("PDF to Audio Converter")

# butonlar ve menü tasarımı

button_browse = tk.Button(root, text="Dosya Seç", command=open_file_dialog)
button_browse.pack(pady=10)

entry_path = tk.Entry(root, width=50)
entry_path.pack(pady=10)

languages = ['en', 'tr']
language_var = tk.StringVar(value=languages[0])
language_dropdown = ttk.Combobox(root, textvariable=language_var, values=languages, state='readonly')
language_dropdown.pack(pady=10)


# seslendirme döngüsü

genders = ['man', 'woman']
gender_var = tk.StringVar(value=genders[1])
gender_dropdown = ttk.Combobox(root, textvariable=gender_var, values=genders, state='readonly')
gender_dropdown.pack(pady=10)

button_convert = tk.Button(root, text="Dönüştür", command=convert_to_audio)
button_convert.pack(pady=10)

root.mainloop()
