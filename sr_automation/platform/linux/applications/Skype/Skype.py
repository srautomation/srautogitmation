import time
import Skype4Py

class Skype(object):
    INPUT_DEVICE_TYPE_FILE = Skype4Py.callIoDeviceTypeFile

    def __init__(self, linux):
        self._linux = linux
        self._Skype4Py = linux._rpyc.modules.Skype4Py
        self._skype = self._Skype4Py.Skype(Events=self._SkypeEvents())
        self._input_device = { 'DeviceType' : ''
                             ,
                                'Value'      : '' }

    def start(self):
        if not self._skype.Client.IsRunning:
            self._skype.Client.Start()
        self._skype.Client.Focus()
        if self._skype.Attach() != 0: # Failed to attach
            time.sleep(1)
            return self._skype.Attach()
        else: 
            return 0

    def stop(self):
        self._linux.cmd("killall skype", shell=True)

    def grab_focus(self):
        return self._skype.Client.Focus()

    @property
    def input_device(self):
        return self._input_device

    @input_device.setter
    def input_device(self, value):
        ''' 
        Sets the input device. 
        Value must be a 2 items squence of device_type and value.
        '''
        try:
            self._input_device['DeviceType'], self._input_device['Set'] = value
        except ValueError:
            raise ValueError('Must supply a 2 items sequence to input_device')

    def place_call(self, number):
        'Calls number and returns a call object'
        return self._skype.PlaceCall(number)

    class _SkypeEvents(object):
        def CallStatus(_self, call, status):
            ' A callback for the event that the status of a call changes '
            wav_file = self._input_device['Value']
            if status == self._Skype4Py.clsInProgress and wav_file != '':
                call.InputDevice(self._input_device , wav_file)
