import getpass

automation_files_dir = "/tmp/automation-temp/"
pictures_dir = automation_files_dir + "automation-screenshots/"
chroot_path = "/data/sunriver/fs/limited/"
working_dir = open(automation_files_dir+'repo_dir.txt','r').read()
username = getpass.getuser()