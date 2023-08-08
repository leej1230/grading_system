import pandas as pd
from os import listdir

# Read all pdf under directory 'pdfs' and return dict
# Input: None
# Output: dict {student ID (string) : file Name (string)}
def load_pdf_list():
    sid_to_file_name = {}

    for file_name in listdir('pdfs'):
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
def sid_list():
    grade_csv = pd.read_csv('save.csv')
    return grade_csv[grade_csv.score != None].values.tolist()

# Updates score and comment of sid row provided on csv and saves
# Input: sid(int), score(str), comment(str)
# Output: None
def update_grade(sid:int, score:str, comment:str):
    grade_csv = pd.read_csv('save.csv')
    mask = grade_csv['sid']==sid
    grade_csv.loc[mask, 'score'] = str(score)
    grade_csv.loc[mask, 'comment'] = comment
    grade_csv.to_csv('save.csv', index=False)

print(sid_list())