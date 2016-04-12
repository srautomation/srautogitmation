import getpass

automation_files_dir = "/tmp/automation-temp/"
pictures_dir = automation_files_dir + "automation-screenshots/"
chroot_path = "/data/sunriver/fs/limited/"
working_dir = open(automation_files_dir+'repo_dir.txt','r').read()
username = getpass.getuser()
log_dir = "/tmp/automation-logs/"
sanity_suites = [
                ('top_panel','Base.py'),
                ('phone_app','Base.py'),
                ('app_launcher','AppLauncher.py'),
                ('mail','SanityMailTest.py'),
                #('pcmanfm','Base.py'),
                ('seamless_browser','seamless_sanity.py'),
                ('camera','CameraVLCTest.py'),
                ('settings','account.py'),
                ('settings','keyboard.py'),
                ('settings','settings_menus.py'),
                ('settings','sound.py'),
                ('settings','wallpaperAndScreenSaver.py'),
                ('settings','user_menu.py')
                #audio
                #notification
                ]

