
automation_files_dir = "/tmp/automation-temp/"
pictures_dir = automation_files_dir + "automation-screenshots/"
chroot_path = "/data/sunriver/fs/limited/"
log_dir = "/tmp/automation-logs/"
sanity_suites = [
                ('top_panel','Base.py'),
                ('phone_app','Base.py'),
                ('app_launcher','AppLauncher.py'),
                ('seemless_browser','seemless_sanity.py')
                ]
