from PIL import Image,ImageTk
import pandas as pd
import shutil
import fitz
import os
import io

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

# Returns number of students who haven't got graded
# Input: None
# Output: Number of ungraded students(int)
def len_ungraded():
    return len(sid_ungraded_list())

# Returns sid to grade next
# Input: None
# Output: SID that needs to be graded in string, if it doesn't exist, returns None
def get_next_sid():
    res = sid_ungraded_list()
    if res:
        return str(res[0])
    return None

# Return the file name from sid
# Input: SID (str)
# Output: PDF file name (str)
def get_file(sid:str):
    file_dict = load_pdf_list()
    if sid not in file_dict:
        return None
    return file_dict[sid]

# Return the tuple (sid, file name) that needs to be grade next
# Input: None
# Output: Tuple (sid (str), file (str))
def get_sid_with_file():
    sid = get_next_sid()
    file = get_file(sid)
    return (sid,file)

# Returns list of sid that have been graded
# Input: None
# Output: List of student ID
def sid_graded_list():
    grade_csv = pd.read_csv('save.csv')
    return grade_csv[grade_csv.score.notna()]['sid'].values.tolist()

# Updates score and comment of sid row provided on csv and saves
# Input: sid(int), score(str), comment(str)
# Output: None
def update_grade(sid:str, score:str, comment:str):
    grade_csv = pd.read_csv('save.csv')
    mask = grade_csv['sid']==int(sid)
    grade_csv.loc[mask, 'score'] = str(score)
    grade_csv.loc[mask, 'comment'] = comment
    grade_csv.to_csv('save.csv', index=False)

# Converts pdf to images and saves
# Input: pdf_file_name(string)
# Output: boolean (True if pdf successfully converted)
def convert_pdf_to_images(pdf_file_name, first=False):
    if os.path.exists(IMG_OUTPUT_DIR):
        shutil.rmtree(IMG_OUTPUT_DIR)
    os.makedirs(IMG_OUTPUT_DIR)

    try:
        pdf_document = fitz.open(os.path.join('pdfs',pdf_file_name))
    except Exception as _:
        return None
    
    for page_num in range(pdf_document.page_count):
        page = pdf_document.load_page(page_num)
        pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
        
        image_path = os.path.join(IMG_OUTPUT_DIR, f'page_{page_num + 1}.png')
        pix.save(image_path, 'png')
    
    pdf_document.close()

    # Stich Images
    image_filenames = get_image_filenames()
    images = [Image.open(os.path.join(IMG_OUTPUT_DIR, image)) for image in image_filenames]
    total_width = max(image.width for image in images)
    total_height = sum(image.height for image in images)

    stitched_image = Image.new("RGB", (total_width, total_height), "white")
    y_offset = 0
    for image in images:
        stitched_image.paste(image, (0, y_offset))
        y_offset += image.height

    output = os.path.join(IMG_OUTPUT_DIR, 'pages.png')
    stitched_image.save(output)
    img = Image.open(output)

    if first:
        bio = io.BytesIO()
        img.save(bio, format="PNG")
        del img
        return bio.getvalue()

    return ImageTk.PhotoImage(img)

# Returns list of pngs in correct order
# Input: None
# Output: list of string
def get_image_filenames():
    return sorted([f for f in os.listdir(IMG_OUTPUT_DIR) if f.lower().endswith('.png')])