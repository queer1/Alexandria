import argparse
import os
import zipfile

def run_crack(zipFile,dictionaryFile):
	for password in dictionaryFile.readlines():
		password = password.strip()
		try:
			zipFile.extractall(pwd=password)
			print "Password found: %s" % password
			return
		except:
			pass
	print "Password not found..."		

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('-f',metavar="ZIP FILE",type = str,required = True,help = "The zip file password protected")
	parser.add_argument('-d',metavar="DICTIONARY",type = str, required = True,help = "The dictionary file containing passwords")
	parser.add_argument('-v','--version', action = 'version', version = '1.0')
	args = parser.parse_args()
	
	if os.path.isfile(args.f):
		try:
			zipFile = zipfile.ZipFile(args.f,"r")
		except IOError:
			exit("Error while opening file: %s.."%args.f)
	else:
		exit("%s is not a valid file..."%args.f)

	if os.path.isfile(args.d):
		try:
			dictionaryFile = open(args.d,"r")
		except IOError:
			exit("Error while opening file: %s.."%args.d)
	else:
		exit("%s is not a valid file..."%args.d)
	
	run_crack(zipFile,dictionaryFile)
	zipFile.close()
	dictionaryFile.close()
