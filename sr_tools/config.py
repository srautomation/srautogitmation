import getpass

automation_files_dir = "/tmp/automation-temp/"
pictures_dir = automation_files_dir + "automation-screenshots/"
chroot_path = "/data/sunriver/fs/limited/"
workdir_filename = automation_files_dir+'repo_dir.txt'
username = getpass.getuser()
log_dir = "/tmp/automation-logs/"
sanity_suites = [
                ('top_panel','Base.py'),
                ('basic_remoting','Base.py'),
                ('app_launcher','AppLauncher.py'),
                #('pcmanfm','Base.py'),
                ('settings','account.py'),
                ('settings','keyboard.py'),
                ('settings','settings_menus.py'),
                ('settings','sound.py'),
                ('settings','wallpaperAndScreenSaver.py'),
                ('settings','user_menu.py'),
                ('seamless_browser','seamless_sanity.py'),
                ('mail','SanityMailTest.py'),
                #audio
                ('alarm','Base.py'),
                ('camera','CameraVLCTest.py')
                ]

def get_working_dir():
    import os.path 
    if os.path.isfile(workdir_filename) is True:
        return open(workdir_filename,'r').read()
    else:
        raise Exception("missing config file. run setup file first")
