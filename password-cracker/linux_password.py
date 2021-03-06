import crypt
import argparse
import os
import threading



def run_crack(passFile, dictionary,semaphore):
	lock = threading.Lock()
	for line in passFile:
		user,hashed = line.split(':')[0:2]
		if hashed[0] == '$':
			if not semaphore:
				password = run_test(user,hashed,dictionary)
			else:
				semaphore.acquire()
				t = threading.Thread(target=run_test, args=(user,hashed,dictionary))  
				t.start()

def run_test(user,hashed,dictionary):
	dictFile = open(dictionary,"r")
	algorithm, salt = hashed.split("$")[1:3]
	completed_salt = "${}${}".format(algorithm, salt)
	hashedPass = hashed.split("$")[3]
	for password in dictFile.readlines():
		password = password.strip()
		if crypt.crypt(password,completed_salt) == hashed:
			lock.acquire()
			print "Pasword found.. %s:%s" % (user,password)
			lock.release()
			dictFile.close()
			semaphore.release()
			return 
	lock.acquire()
	print "Password not found for user: %s" % user
	lock.release()
	dictFile.close()
	semaphore.release()
	return 


if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('-p',metavar="SHADOW FILE",type = str, default ="/etc/shadow",help = "The file with accounts (shadow format)")
	parser.add_argument('-t',metavar="THREADS NUMBER",type = int, default =0,help = "The number of threads to accelerate the process")
	parser.add_argument('-d',metavar="DICTIONARY",type = str, required = True,help = "The dictionary file containing passwords")
	parser.add_argument('-v','--version', action = 'version', version = '1.0')
	args = parser.parse_args()
	
	if args.p:
		if os.path.isfile(args.p):
			try:
				passFile = open(args.p, "r")
			except IOError:
				if args.p == "/etc/shadow" and not os.geteuid() == 0:
					exit("You must run this as root..")
				else:
					exit("Error while opening file: %s.."%args.p)
		else:
			exit("%s is not a valid file..."%args.p)

	if not os.path.isfile(args.d):
		exit("Dictionary file does not exist or is invalid..")
	if args.t > 1:
		semaphore = threading.BoundedSemaphore(value=args.t)
	else:
		semaphore =  None 
	run_crack(passFile, args.d, semaphore)
			

	passFile.close()
