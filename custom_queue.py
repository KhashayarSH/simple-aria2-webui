from os.path import isfile, getsize
import json
from threading import Lock


class QueueHandler():
    # a list of dictionaries for each QUEUE
    QUEUES = 0
    # a single dictionary with gid and QUEUE for that gid
    DOWNLOAD_QUEUE = 0
    queue_lock = 0
    download_queue_lock = 0
    def __init__(self):
        self.QUEUES = []
        self.DOWNLOAD_QUEUE = []
        self.queue_lock = Lock()
        self.download_queue_lock = Lock()
        with self.queue_lock:
            if isfile('QUEUES') and getsize('QUEUES'):
                with open('QUEUES') as json_file:
                    self.QUEUES = json.load(json_file)['QUEUES']
            else:
                with open('QUEUES','w') as json_file:
                    data = {}
                    data['QUEUES'] = []
                    json.dump(data, json_file)

        with self.download_queue_lock:
            if isfile('DOWNLOAD_QUEUE') and getsize('DOWNLOAD_QUEUE'):
                with open('DOWNLOAD_QUEUE') as json_file:
                    self.DOWNLOAD_QUEUE = json.load(json_file)['DOWNLOAD_QUEUE']
            else:
                with open('DOWNLOAD_QUEUE','w') as json_file:
                    data = {}
                    data['DOWNLOAD_QUEUE'] = {}
                    json.dump(data, json_file)

    def get_queues(self):
        return self.QUEUES

    def get_downloads_queue(self):
        return self.DOWNLOAD_QUEUE

    def delete_queue(self, QUEUE):
        with self.queue_lock:
            for item in self.QUEUES:
                if item['name'] == QUEUE:
                    self.QUEUES.remove(item)
                    break
            with open('QUEUES','w') as json_file:
                data = {}
                data['QUEUES'] = self.QUEUES
                json.dump(data, json_file)
        with self.download_queue_lock:
            a = []
            for item in self.DOWNLOAD_QUEUE:
                if self.DOWNLOAD_QUEUE[item] == QUEUE:
                    a.append(item)
            for item in a:
                self.DOWNLOAD_QUEUE.pop(item, None)
            with open('DOWNLOAD_QUEUE','w') as json_file:
                data = {}
                data['DOWNLOAD_QUEUE'] = self.DOWNLOAD_QUEUE
                json.dump(data, json_file)

    def add_queue(self, name, start, finish):
        QUEUE = {'name':name,
                 'start':start,
                 'finish':finish
                 }
        with self.queue_lock:
            self.QUEUES.append(QUEUE)
            with open('QUEUES','w') as json_file:
                data = {}
                data['QUEUES'] = self.QUEUES
                json.dump(data, json_file)

    def change_download_queue(self, gid, QUEUE=''):
        with self.queue_lock:
            if QUEUE == '':
                self.DOWNLOAD_QUEUE.pop(gid, None)
            else:
                self.DOWNLOAD_QUEUE[gid] = QUEUE
            with open('DOWNLOAD_QUEUE','w') as json_file:
                data = {}
                data['DOWNLOAD_QUEUE'] = self.DOWNLOAD_QUEUE
                json.dump(data, json_file)

    def update_queue(self, original_name, name, start, finish):
        with self.queue_lock:
            QUEUE = {'name':name,
                     'start':start,
                     'finish':finish
                     }
            for item in self.QUEUES:
                if item['name'] == original_name:
                    self.QUEUES.remove(item)
                    self.QUEUES.append(QUEUE)
                    break
            with open('QUEUES','w') as json_file:
                data = {}
                data['QUEUES'] = self.QUEUES
                json.dump(data, json_file)
        with self.download_queue_lock:
            for item in self.DOWNLOAD_QUEUE:
                if self.DOWNLOAD_QUEUE[item] == original_name:
                    self.DOWNLOAD_QUEUE[item] = name

            with open('DOWNLOAD_QUEUE','w') as json_file:
                data = {}
                data['DOWNLOAD_QUEUE'] = self.DOWNLOAD_QUEUE
                json.dump(data, json_file)
