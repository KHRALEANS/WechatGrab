# %%
import re
import os
from xmlrpc.client import Boolean
from email_tools import send_qq_smtp_email

# %%
def isDateTime(line):
    if re.match(r'(([\w\s\,]+[\s]{1})|^)\d{2}\:\d{2}$', line.rstrip()):
        return True
    else:
        return False

# %%
def isUpdated(oldFile, newFile):
    with open(oldFile) as f:
        ofLines = f.readlines()
    with open(newFile) as f:
        nfLines = f.readlines()
    identity = False
    while len(ofLines) and len(nfLines):
        ol = ofLines.pop()
        nl = nfLines.pop()
        if ol != nl:
            return not identity
        if isDateTime(ol):
            identity = True
            return not identity
    if len(ofLines) == len(nfLines):
        identity = True
    return not identity

# %%
def list_txt_files(file_dir):
    txt_files = []
    for file in os.listdir(file_dir):
        if os.path.isfile(os.path.join(file_dir, file)):
            if re.match(r'[\w]+\_[\w\-]+\.txt' ,file):
                txt_files.append(file)
    return txt_files

def list_contact_folders(file_dir):
    contact_folders = []
    for file in os.listdir(file_dir):
        if os.path.isdir(os.path.join(file_dir, file)):
            if re.match(r'^[\w]+$', file):
                contact_folders.append(file)
    return contact_folders

# %%
# list_txt_files('data/')

# %%
# list_contact_folders('data/')
# %%
def contacts_in_current_dir(file_dir):
    current_txt_files = list_txt_files(file_dir)
    current_txt_contacts = []
    for current_txt_file in current_txt_files:
        contact = current_txt_file.split('_')[0]
        if contact not in current_txt_contacts:
            current_txt_contacts.append(contact)
    return current_txt_contacts
# %%
month_dic = {"January":1, "February":2, "March":3, "April":4, "May":5, "June":6, "July":7, "August":8, "September":9, "October":10, "November":11, "December":12}

# %%
def month_str2num(month_str):
    if re.match(r'^[jJ](an|AN)\.?[a-zA-Z]*$', month_str):
        return 1
    if re.match(r'^[fF](eb|EB)\.?[a-zA-Z]*$', month_str):
        return 2
    if re.match(r'^[mM](ar|AR)\.?[a-zA-Z]*$', month_str):
        return 3
    if re.match(r'^[aA](pr|PR)\.?[a-zA-Z]*$', month_str):
        return 4
    if re.match(r'^[mM](ay|AY)$', month_str):
        return 5
    if re.match(r'^[jJ](un|UN)[eE]?$', month_str):
        return 6
    if re.match(r'^[jJ](ul|UL)[yY]?$', month_str):
        return 7
    if re.match(r'^[aA](ug|UG)\.?[a-zA-Z]*$', month_str):
        return 8
    if re.match(r'^[sS](ep|EP)[tT]?\.?[a-zA-Z]*$', month_str):
        return 9
    if re.match(r'^[oO](ct|CT)\.?[a-zA-Z]*$', month_str):
        return 10
    if re.match(r'^[nN](ov|OV)\.?[a-zA-Z]*$', month_str):
        return 11
    if re.match(r'^[dD](ec|EC)\.?[a-zA-Z]*$', month_str):
        return 12
    return 0
# %%
def is_newer_than(file1: str, file2: str):
    """file1 is newer than file2

    Args:
        file1 (str): _description_
        file2 (str): _description_

    Returns:
        bool: _description_
    """
    file1_items = file1.split('_')[-1].split('.')[0].split('-')
    file2_items = file2.split('_')[-1].split('.')[0].split('-')
    if int(file1_items[0]) < int(file2_items[0]):
        return False
    elif int(file1_items[0]) > int(file2_items[0]):
        return True
    elif month_str2num(file1_items[1]) < month_str2num(file1_items[1]):
        return False
    elif month_str2num(file1_items[1]) > month_str2num(file1_items[1]):
        return True
    elif int(file1_items[2]) < int(file2_items[2]):
        return False
    elif int(file1_items[2]) > int(file2_items[2]):
        return True
    elif int(file1_items[3]) < int(file2_items[3]):
        return False
    elif int(file1_items[3]) > int(file2_items[3]):
        return True
    elif int(file1_items[4]) < int(file2_items[4]):
        return False
    elif int(file1_items[4]) > int(file2_items[4]):
        return True
    elif int(file1_items[5]) < int(file2_items[5]):
        return False
    elif int(file1_items[5]) > int(file2_items[5]):
        return True
    else:
        return False
# %%
def get_two_recent_files(fileNames: list):
    filenames = fileNames.copy()
    assert len(filenames) >= 2
    for i in range(0,len(filenames)-1):
        if is_newer_than(filenames[i],filenames[i+1]):
            tmp = filenames[i+1]
            filenames[i+1] = filenames[i]
            filenames[i] = tmp
    for i in range(0,len(filenames)-2):
        if is_newer_than(filenames[i],filenames[i+1]):
            tmp = filenames[i+1]
            filenames[i+1] = filenames[i]
            filenames[i] = tmp
    newest_file = filenames[-1]
    second_newest_file = filenames[-2]
    return newest_file, second_newest_file
# %%
def make_dir_from_list(path_to_dir, dir_names):
    full_dirs = [os.path.join(path_to_dir,dir) for dir in dir_names]
    having_made = []
    for fdir in full_dirs:
        if os.path.exists(fdir):
            continue
        try:
            os.mkdir(fdir)
            having_made.append(fdir)
        except Exception as e:
            print("error: ", e, "when making dir ", fdir)
            print("having made ", having_made, "success")
            return
    return having_made

def get_config(config_file):
    with open(config_file) as f:
        configLines = f.readlines()
    config = {}
    for i,line in enumerate(configLines):
        if line.strip() == "abs_path:":
            config['CUR_PATH'] = configLines[i+1].strip()
        elif line.strip() == "SENDER_USERNAME:":
            config['SENDER_USERNAME'] = configLines[i+1].strip()
        elif line.strip() == "SENDER_PASSWORD:":
            config['SENDER_PASSWORD'] = configLines[i+1].strip()
        elif line.strip() == "RECEIVER:":
            config['RECEIVER'] = configLines[i+1].strip()
    return config

# %%

if __name__ == '__main__':
    # get current path
    CUR_PATH = os.path.dirname(os.path.realpath(__file__))
    data_path = os.path.join(CUR_PATH, 'data/')
    # read config
    config = get_config(os.path.join(CUR_PATH, 'config/config.txt'))
    # contacts in new-added txt files
    contacts_ofNewTXT = contacts_in_current_dir(data_path)
    # make new contact-folders if there is new contact in txt files
    new_contact_folders = make_dir_from_list(data_path, contacts_ofNewTXT)
    # filenames of new-added txt files
    text_files = list_txt_files(data_path)

    # move new-added txt files to contact-folders
    for text_file in text_files:
        contact = text_file.split('_')[0]
        tar_dir = os.path.join(data_path, contact)
        cur_file = os.path.join(data_path, text_file)
        tar_file = os.path.join(tar_dir, text_file)
        os.rename(cur_file, tar_file)
        
    # cd each contact-folder, check if updated, then send to email
    for contact in contacts_ofNewTXT:
        contact_dir = os.path.join(data_path, contact)
        contact_text_files = list_txt_files(contact_dir)
        if len(contact_text_files) < 2:
            if len(contact_text_files) == 0:
                continue
            newer_file = os.path.join(contact_dir, contact_text_files[0])
            with open(newer_file) as f:
                msg = f.read()
            result = send_qq_smtp_email(msg, contact, config)
        else:
            newest_file, second_newest_file = get_two_recent_files(contact_text_files)
            older_file = os.path.join(contact_dir, second_newest_file)
            newer_file = os.path.join(contact_dir, newest_file)
            if isUpdated(older_file, newer_file):
                with open(newer_file) as f:
                    msg = f.read()
                result = send_qq_smtp_email(msg, contact, config)

