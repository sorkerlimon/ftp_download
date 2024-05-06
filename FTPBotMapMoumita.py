import paramiko
from datetime import datetime
import os

def serve_login():
    sftp_host = 'ftp03.datatree.com'
    sftp_port = 22 
    sftp_username = '$IMQA'
    sftp_password = '$qamst$'

    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(hostname=sftp_host, port=sftp_port, username=sftp_username, password=sftp_password)
    
    sftp_client = ssh_client.open_sftp()

    return sftp_client, ssh_client



def download_misc_text_files(sftp_client, local_directory,download_date):
    text_file_path = 'locations.txt'  

    with open(text_file_path, 'r') as f:
        folders = f.readlines()

    for folder in folders:
        print(f"[INFO]-->> Currently, downloading from this{ folder }")
        folder = folder.strip()
        sftp_path = '/' + folder
        sftp_client.chdir(sftp_path) 
        files = sftp_client.listdir_attr()
        # misc_text_files = [file for file in files if file.filename.endswith('.txt') and 'CAPR_Prod_Misc' in file.filename]
        # misc_text_files = [file for file in files if file.filename.endswith('.txt') and ('CAPR_Prod_Misc' in file.filename or 'CAPR_Prod_Exception' in file.filename)]
        misc_text_files = [file for file in files if file.filename.endswith('.txt') and (('CAPR_Prod_Misc' in file.filename or 'CAPR_Prod_Exception' in file.filename) or ('EPR_Prod_Misc' in file.filename or 'EPR_Prod_Exception' in file.filename) or ('EPR_Prod_Daily_Take' in file.filename or 'CAPR_Prod_Daily_Take' in file.filename))]

        if misc_text_files:
            if not os.path.exists(local_directory):
                os.makedirs(local_directory)
            today_date = datetime.now().strftime('%Y-%m-%d')
            for file_attr in misc_text_files:
                file_to_download = file_attr.filename
                local_path = os.path.join(local_directory, file_to_download)
                try:
                    upload_date = datetime.fromtimestamp(file_attr.st_mtime).strftime('%Y-%m-%d')
                    if upload_date == download_date:
                        sftp_client.get(file_to_download, local_path)
                        print(f"{file_to_download} (Uploaded Date: {upload_date}) downloaded successfully.")
                except Exception as e:
                    print(f"An error occurred while downloading {file_to_download}: {e}")
        else:
            print(f"No Prod_Misc text files found in the {folder} directory.")





if __name__ == "__main__":
    today_date = datetime.now().strftime('%Y-%m-%d')
    target_date = datetime(year=2024, month=12, day=28)
    current_date = datetime.now()
    print(f'''
                                                █████ █████ ██████   ██████ █████      
                                                 ███   ███   ██████ ██████   ███       
                                                 ███   ███   ███  ███  ███   ███                   
                                                 ███   ███   ███       ███   ███    
                                                █████ █████ █████     █████ █████
                                                            V-0.0.2 (System Team)  
          
                                                   🎉🎉    FTP Download Bot   🎉🎉 
                                                              {today_date}                                                   
    ''')

    if current_date < target_date: 
        try:
            username = input('Enter username : ').lower()
            password = input('Enter password : ').lower()
            if username == 'iimi' and password == 'iimi':
                sftp_client, ssh_client = serve_login()
                local_directory = input("Enter the local directory path where you want to save the files: ")
                download_date = input("Enter the Date (2024-03-16): ")
                print("\n")
                download_misc_text_files(sftp_client,local_directory,download_date)
                input("Press any key to close.")
            else:
                print("Username and password  incorrect 😢😢😢")

        except Exception as e:
            print(f"An error occurred: {e}")
            
    else:
        print("Update your software!")


# pyinstaller --onefile --icon=logo.ico BotMap.py