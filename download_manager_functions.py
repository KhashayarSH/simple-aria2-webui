from aria2rpcfunctions import add_download_rpc, tell_active_download_rpc, tell_waiting_download_rpc, tell_stopped_download_rpc, unpause_all_download_rpc, pause_all_download_rpc, remove_download_rpc, pause_download_rpc, unpause_download_rpc, tell_status_download_rpc, change_url_download_rpc
from app import queue_handler
import datetime

# These functions are used as a facade for Download Manager functionalities merging Queues and aria2rpcfunctions


# Returns a list of tellStatus rpc request results for given filters and queue
def get_downloads_dm(filters, displayed_queue):
    downloads = []
    downloads = tell_active_download_rpc()
    downloads += tell_waiting_download_rpc()
    downloads += tell_stopped_download_rpc()
    downloads_queue = get_downloads_queue_dm()
    a=[]
    for item in downloads:
        if displayed_queue != 'All Downloads':
            if displayed_queue != downloads_queue.get(item['gid'], 'Main Queue'):
                a.append(item)
                continue
        if item['status'] not in filters:
            a.append(item)
    for item in a:
        downloads.remove(item)
    return downloads

# returns tellStatus for given gid
def get_status_dm(gid):
    return tell_status_download_rpc(gid)

# adds a download with the given link and queue
def add_download_dm(link, queue):
    gid = add_download_rpc(link)
    if queue != "Main Queue":
        queue_handler.change_download_queue(gid, queue)

# adds the given link to download with gived gid's uri list
def change_download_link_dm(gid, link):
    return change_url_download_rpc(gid, link)

# pauses download with given gid
def pause_download_dm(gid):
    current_status = get_status_dm(item)['status']
    if current_status == 'active' or current_status == 'waiting':
        return pause_download_rpc(gid)

# unpauses download with given gid
def unpause_download_dm(gid):
    current_status = get_status_dm(item)['status']
    if current_status == 'paused':
        return unpause_download_rpc(gid)

# removes download with given gid
def remove_download_dm(gid):
    current_status = get_status_dm(item)['status']
    if current_status == 'paused' or current_status == 'waiting' or current_status == 'active':
        return remove_download_rpc(gid)

# returns  a list of queues
def get_queues_dm():
    return queue_handler.get_queues()

# returns a dictionary key:gid, value:queue.name
def get_downloads_queue_dm():
    return queue_handler.get_downloads_queue()

# changes queue of a given download
def change_download_queue_dm(gid, queue):
    if queue == "Main Queue":
        queue = ''
    queue_handler.change_download_queue(gid, queue)

# adds a queue with given values to queues
def add_queue_dm(name, start, finish):
    queue_handler.add_queue(name, start, finish)

# delets a queue with given name
def delete_queue_dm(queue):
    queue_handler.delete_queue(queue)

# updates a queue with new values
def update_queue_dm(original_name, name, start, finish):
    queue_handler.update_queue(original_name, name, start, finish)

# unpauses all paused downloads in given queue
def start_queue_dm(queue):
    downloads_queue = get_downloads_queue_dm()
    for item in downloads_queue:
        if downloads_queue[item] == queue:
            if get_status_dm(item)['status'] == 'paused':
                unpause_download_dm(item)

# pauses all active/waiting downloads in given queue
def stop_queue_dm(queue):
    downloads_queue = get_downloads_queue_dm()
    for item in downloads_queue:
        if downloads_queue[item] == queue:
            current_status = get_status_dm(item)['status']
            if current_status == 'active' or current_status == 'waiting':
                pause_download_dm(item)

# checks all queues and starts or stops queues as needed 
def queue_player():
    current_time = datetime.datetime.now()
    current_time = current_time.hour*60+current_time.minute
    queues = get_queues_dm()
    for queue in queues:
        start = int(queue['start'][0:2])*60 + int(queue['start'][3:5])
        finish = int(queue['finish'][0:2])*60 + int(queue['finish'][3:5])
        if start < finish:
            if(start < current_time and current_time < finish):
                start_queue_dm(queue['name'])
            else:
                stop_queue_dm(queue['name'])
        else:
            if(start < current_time or current_time < finish):
                start_queue_dm(queue['name'])
            else:
                stop_queue_dm(queue['name'])
