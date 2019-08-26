##
# Written in Python 2.7
###

import os
import zipfile
import shutil
import datetime
import time
import subprocess
from datetime import timedelta

def make_zipfile(target_zip, source_dir):
    relroot = os.path.abspath(os.path.join(source_dir, os.pardir))
    with zipfile.ZipFile(target_zip, "w", zipfile.ZIP_DEFLATED) as zip:
        for root, dirs, files in os.walk(source_dir):
            # add directory (needed for empty dirs)
            zip.write(root, os.path.relpath(root, relroot))
            for file in files:
                filename = os.path.join(root, file)
                if os.path.isfile(filename): # regular files only
                    arcname = os.path.join(os.path.relpath(root, relroot), file)
                    zip.write(filename, arcname)
    print ("Created ", target_zip)

if __name__ =='__main__':
	print('Starting execution')
	
	#compress to zip
	source_folder = 'C:\\Users\\Rodolfo Sanches\\Desktop\\Banco de Dados'
	backups_folder = 'C:\\Users\\Rodolfo Sanches\\Desktop\\backups'
	target_zip = backups_folder + '\\backup'
	zipExtension = '.zip'
	now = time.time()

	#Verifica se o ultimo backup foi feito há pelo menos x horas
	xHoras = 6

	os.chdir(backups_folder)
	files = filter(os.path.isfile, os.listdir(backups_folder))
	files = [os.path.join(backups_folder, f) for f in files] # add path to each file

	files = sorted(files, reverse=True)

	dateLastFile = datetime.datetime.fromtimestamp(os.path.getctime(files[0]))

	nowMinusXhours = datetime.datetime.now() - datetime.timedelta(hours = xHoras)

	if dateLastFile <= nowMinusXhours:
		print("Criando backup")
		#Cria o ZIP
		make_zipfile(target_zip + zipExtension, source_folder)	
				
		#Renomeia para a data
		modifiedTime = os.path.getmtime(target_zip + zipExtension) 
		timeStamp =  datetime.datetime.fromtimestamp(modifiedTime).strftime("%b-%d-%y-%H_%M_%S")
		os.rename(target_zip + zipExtension, target_zip+"_"+timeStamp + zipExtension)
	else:
		print ('Backup ja realizado (intervalo minimo: ' + str(xHoras) + ' horas)')


	# Deleta os backups
	for f in os.listdir(backups_folder):
		if os.stat(os.path.join(backups_folder,f)).st_mtime < now - 7 * 86400:
			print ("Deletando arquivos antigos: " + f)
			os.remove(os.path.join(backups_folder, f))
	
	print('Ending execution')
