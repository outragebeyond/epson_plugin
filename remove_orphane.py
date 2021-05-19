import os
import shutil
def remove_orphane(monitor_dir,studies_dir):	
	os.chdir(monitor_dir)	
	for file in os.listdir():
		if file.endswith(('.ERR', '.DON')):
			os.remove(file)
			shutil.rmtree(f'{studies_dir}\\{file[0:-4]}')		

remove_orphane(r'C:\EPSON\TDBridge\Orders', r'C:\DBurner\input')