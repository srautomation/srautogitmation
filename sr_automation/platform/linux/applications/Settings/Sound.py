from sr_automation.platform.linux.applications.Settings.Settings_submenu import Settings_submenu

class Sound(Settings_submenu):
    
    SOUND_SUBMENU = (870, 200)
    MUTE_BUTTON = "Mute"
    OUTPUT_LABEL = "Output volume"


    def __init__(self, settings):
        super(Sound, self).__init__(settings, self.SOUND_SUBMENU)

    def change_output_volume_level(self, _value):
        self._app.child(name=self.OUTPUT_LABEL).parent.parent.child(roleName="slider").value = _value*1000
