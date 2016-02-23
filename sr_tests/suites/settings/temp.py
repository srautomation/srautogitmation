import rpyc
connect1 = rpyc.classic.connect('192.168.1.39')
connect1.modules.dogtail.procedural.run('sunriversettings')

