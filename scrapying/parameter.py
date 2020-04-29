import os 

SCR_PATH = 'scrapying/'
ROOT_PATH = os.getcwd() + '/' + SCR_PATH

INPUT_PATH = ROOT_PATH + 'input/'

OUTPUT_PATH = ROOT_PATH + 'output/'
UNZIP_PATH = OUTPUT_PATH + 'unzip/'
ZIP_PATH = OUTPUT_PATH + 'zip/'
RESULT_PATH = OUTPUT_PATH + 'dict/'
BADFILE_PATH = ZIP_PATH + 'bad_zip/'    

if os.path.isdir(OUTPUT_PATH) == False:
    os.mkdir(OUTPUT_PATH)
if os.path.isdir(ZIP_PATH) == False:    
    os.mkdir(ZIP_PATH)
if os.path.isdir(UNZIP_PATH) == False:    
    os.mkdir(UNZIP_PATH)
if os.path.isdir(RESULT_PATH) == False:    
    os.mkdir(RESULT_PATH)
if os.path.isdir(BADFILE_PATH) == False:    
    os.mkdir(BADFILE_PATH)

# paths of dictionary files 
DICT_SCR = RESULT_PATH + 'char_list.txt'

# paths of shop name files 
SHOP_NAME_LIST_SCR = RESULT_PATH + 'name_list.txt' 

ZIP_FILE = RESULT_PATH + "zip.txt"