import pandas as pd
import shutil
import fitz
import os

IMG_OUTPUT_DIR = 'page_cache'

# Read all pdf under directory 'pdfs' and return dict
# Input: None
# Output: dict {student ID (string) : file Name (string)}
def load_pdf_list():
    sid_to_file_name = {}

    for file_name in os.listdir('pdfs'):
        sid = file_name.split('@')[0]
        sid_to_file_name[sid] = file_name

    return sid_to_file_name

# Returns list of sid from csv file IN ORDER
# Input: None
# Output: List of student ID
def sid_list():
    grade_csv = pd.read_csv('save.csv')
    return grade_csv['sid'].values.tolist()

# Returns list of sid that haven't been graded
# Input: None
# Output: List of student ID
def sid_ungraded_list():
    grade_csv = pd.read_csv('save.csv')
    return grade_csv[grade_csv.score.isna()]['sid'].values.tolist()

# Returns list of sid that have been graded
# Input: None
# Output: List of student ID
def sid_graded_list():
    grade_csv = pd.read_csv('save.csv')
    return grade_csv[grade_csv.score.notna()]['sid'].values.tolist()

# Updates score and comment of sid row provided on csv and saves
# Input: sid(int), score(str), comment(str)
# Output: None
def update_grade(sid:int, score:str, comment:str):
    grade_csv = pd.read_csv('save.csv')
    mask = grade_csv['sid']==sid
    grade_csv.loc[mask, 'score'] = str(score)
    grade_csv.loc[mask, 'comment'] = comment
    grade_csv.to_csv('save.csv', index=False)

# Converts pdf to images and saves
# Input: pdf_file_name(string)
# Output: boolean (True if pdf successfully converted)
def convert_pdf_to_images(pdf_file_name):
    if os.path.exists(IMG_OUTPUT_DIR):
        shutil.rmtree(IMG_OUTPUT_DIR)
    os.makedirs(IMG_OUTPUT_DIR)

    try:
        pdf_document = fitz.open(os.path.join('pdfs',pdf_file_name))
    except Exception as _:
        return False
    
    for page_num in range(pdf_document.page_count):
        page = pdf_document.load_page(page_num)
        pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
        
        image_path = os.path.join(IMG_OUTPUT_DIR, f'page_{page_num + 1}.png')
        pix.save(image_path, 'png')
    
    pdf_document.close()
    return True

# Returns list of pngs in correct order
# Input: None
# Output: list of string
def get_image_filenames():
    return sorted([f for f in os.listdir(IMG_OUTPUT_DIR) if f.lower().endswith('.png')])