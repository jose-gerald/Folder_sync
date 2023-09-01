# Import libraries and logging configurations
import os 
import time   
import subprocess 
import argparse
import logging

logging.basicConfig(format = ' %(levelname)s - %(message)s ', 
                    level = logging.DEBUG, handlers=[logging.FileHandler('log_file.log'), logging.StreamHandler()] )


path_source = r"C:\Users\zecam\OneDrive\Área de Trabalho\notebook"
path_replica = r"C:\Users\zecam\OneDrive\Área de Trabalho\c programm"

hidden_files = []

# Function to copy content 
def copy(source_path, replica_path): 
# Loop to iterate over every element of source folder   
   for file in os.listdir(source_path):
      s_path = os.path.join(source_path, file)
      r_path = os.path.join(replica_path, file)
        # In case iterable is a file
      if os.path.isfile(s_path) == True: 
           # Open file in 'read mode'21
            with open(s_path,'rb') as content:
               text= content.read()
           # Open file in replica directory in 'write mode' and perform writing 
            with open(r_path, 'wb') as content_replica:
               content_replica.write(text)  
               logging.info(f'[{time.strftime("%Y-%m-%d %H:%M:%S")}] - copied{s_path} to: \n {r_path}')
      elif os.path.isdir(s_path) == True:
       # In case of iterable being a folder the 'copy' function is applied 
                  os.makedirs(r_path, exist_ok= True)
                  logging.info(f'[{time.strftime("%Y-%m-%d %H:%M:%S")}] - created directory : \n {r_path}')
                  copy(s_path, r_path)
      else:
         logging.warning(f'[{time.strftime("%Y-%m-%d %H:%M:%S")}] - skipped {s_path}: \n it is neither a file nor a directory.')
   # Check if all files were copied, if not the error is due to permission ristrictions 
   assert os.listdir(source_path) == os.listdir(replica_path), \
   logging.warning(f'[{time.strftime("%Y-%m-%d %H:%M:%S")}] - there exist files or directories in {source_path} to which permission to access is denied  ')              
                  
# Synchronizing directories function                                                        
def syncfunc(source_path, days= 0, hours = 0, seconds = 0):
        days = int(days)
        hours = int(hours)
        seconds = int(seconds)
        date_sync = days*86400 + hours*3600 + seconds
        for file in os.listdir(source_path):
                  s_path = os.path.join(source_path, file)
                  r_path = os.path.join(path_replica, file)
                  # if path dates dont match apply copy function
                  if os.path.getmtime(s_path) < os.path.getmtime(r_path):
                    copy(source_path, path_replica)
                    # put program to sleep
                    time.sleep(date_sync)
                    subprocess.run(['python','folder_sinc.py'])

# Function to unhidde the 'hidden files'
def unhidde_files(source_path):

   for file in os.listdir(source_path):
      file_path = os.path.join(source_path, file)
      if file[0] == '.':
         new_file = file.lstrip('.')
         new_file_path = os.path.join(source_path, new_file)
         os.rename(file_path, new_file_path)
         hidden_files.append(file)
         logging.info(f'[{time.strftime("%Y-%m-%d %H:%M:%S")}] - {new_file}: \n was striped of its hidden status')

# Function to hidde 'unhidden files'
def hidde_files(source_path):
    for file in hidden_files:
        original_file_path = os.path.join(source_path, file)
        current_file_path = os.path.join(source_path, file.lstrip('.'))
        os.rename(current_file_path, original_file_path)
        logging.info(f'[{time.strftime("%Y-%m-%d %H:%M:%S")}] - {file}: was given hidden status')


# User argument parsing 
parser = argparse.ArgumentParser(description = 'This program is designed to copy two directories and perform periodic synchronization.')

parser.add_argument('path_source', help = 'Path to the source directory.')
parser.add_argument('path_replica', help = 'Path to the replica directory.')
parser.add_argument('--days', default = 0, type = int, help = 'Number of days of the synchronization period (default = 0)')
parser.add_argument('--hours', default = 0, type = int, help = 'Number of hours of the  synchronization period (default = 0)')
parser.add_argument('--seconds', default = 0,type = int, help = 'Number of seconds of the synchronization period (default = 0)')
parser.add_argument('--log-file', default = 'log_file.log', help = 'File logged to program actions')

args = parser.parse_args()

# Program execution block 
unhidde_files(args.path_source)
copy(args.path_source, args.path_replica)
hidde_files(args.path_source)
hidde_files(args.path_replica)
syncfunc(args.path_source, args.days, args.hours, args.seconds)




