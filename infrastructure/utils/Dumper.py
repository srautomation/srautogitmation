from logbook import Logger
import csv

log = Logger("Dumper")

class Dumper(object):
    '''
        Collects samples with samples_description and dumps them into csv_file
    '''
    def __init__(self, csv_file, *samples_description):
        self._csv_file_path = csv_file
        self._headers = tuple(samples_description)
        self._samples = []
        self._csv = None
    
    def __enter__(self):
        pass

    def __exit__(self, type, value, traceback):
        self.save()

    def append(self, **sample):
        self._samples.append(sample)
        log.info("Added sample to dumper")

    def save(self):
        with open(self._csv_file_path, 'a') as csv_file:
            self._csv = csv.DictWriter(csv_file, self._headers)
            if not self._has_headers():
                self._csv.writeheader()
            self._csv.writerows(self._samples)
            log.info("Saved samples to csv file: %s" % self._csv_file_path)

    def _has_headers(self):
        try:
            with open(self._csv_file_path) as csv_file:
                reader = csv.DictReader(csv_file)
                if reader.fieldnames:
                    return tuple(reader.fieldnames) == self._headers
                else: 
                    return False
        except IOError as e:
            if e.errno == 2:    return False
            else:               raise e
