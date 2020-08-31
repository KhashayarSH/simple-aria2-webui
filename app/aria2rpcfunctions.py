import json
from config import TOKEN, JSONRPC_LINK, opener

# adds a download with given link to given queue.
def add_download_rpc(link, queue):
    jsonreq = json.dumps({'jsonrpc':'2.0', 'id':'qwer', 'method':'aria2.addUri',
                         'params':['token:'+TOKEN, [link]]})
    c = opener.open(JSONRPC_LINK, jsonreq)
    data = json.load(c)['result']
    return data

# removes a download with given ID.
def remove_download_rpc(download_id):
    jsonreq = json.dumps({'jsonrpc':'2.0', 'id':'qwer', 'method':'aria2.remove',
                         'params':['token:'+TOKEN, download_id]})
    c = opener.open(JSONRPC_LINK, jsonreq)

# removes a download with given ID.
def change_url_download_rpc(download_id, link):
    jsonreq = json.dumps({'jsonrpc':'2.0', 'id':'qwer', 'method':'aria2.changeUri',
                         'params':['token:'+TOKEN, download_id, 1, [], [link]]})
    c = opener.open(JSONRPC_LINK, jsonreq)

# pauses a download with given ID.
def pause_download_rpc(download_id):
    jsonreq = json.dumps({'jsonrpc':'2.0', 'id':'qwer', 'method':'aria2.pause',
                         'params':['token:'+TOKEN, download_id]})
    c = opener.open(JSONRPC_LINK, jsonreq)

# pauses all downloads.
def pause_all_download_rpc():
    jsonreq = json.dumps({'jsonrpc':'2.0', 'id':'qwer', 'method':'aria2.pauseAll',
                         'params':['token:'+TOKEN]})
    c = opener.open(JSONRPC_LINK, jsonreq)

# unpauses(moves to waiting queue) a download with given ID.
def unpause_download_rpc(download_id):
    jsonreq = json.dumps({'jsonrpc':'2.0', 'id':'qwer', 'method':'aria2.unpause',
                         'params':['token:'+TOKEN, download_id]})
    c = opener.open(JSONRPC_LINK, jsonreq)

# unpauses (moves to waiting queue) all downloads.
def unpause_all_download_rpc():
    jsonreq = json.dumps({'jsonrpc':'2.0', 'id':'qwer', 'method':'aria2.unpauseAll',
                         'params':['token:'+TOKEN]})
    c = opener.open(JSONRPC_LINK, jsonreq)

# returns a json object containing the given params.
# files is a json object itself.
def tell_status_download_rpc(download_id):
    jsonreq = json.dumps({'jsonrpc':'2.0', 'id':'qwer',
                         'method':'aria2.tellStatus',
                         'params':['token:'+TOKEN, download_id,
                                    ['gid', 'status', 'dir', 'totalLength',
                                     'completedLength', 'downloadSpeed', 'files',
                                     'errorCode', 'errorMessage', 'connections',
                                     'pieceLength', 'numPieces', 'connections']]})
    c = opener.open(JSONRPC_LINK, jsonreq)
    data = json.load(c)['result']
    return data

# returns a list of downloads with status == active.
# each element of list is a the same object that tell_status_download returns.
def tell_active_download_rpc():
    jsonreq = json.dumps({'jsonrpc':'2.0', 'id':'qwer',
                         'method':'aria2.tellActive',
                         'params':['token:'+TOKEN,
                                    ['gid', 'status', 'dir', 'totalLength',
                                     'completedLength', 'downloadSpeed', 'files',
                                     'errorCode', 'errorMessage', 'connections',
                                     'pieceLength', 'numPieces', 'connections']]})
    c = opener.open(JSONRPC_LINK, jsonreq)
    data = json.load(c)['result']
    return data

# returns a list of downloads with status == waiting.
# each element of list is a the same object that tell_status_download returns.
def tell_waiting_download_rpc():
    jsonreq = json.dumps({'jsonrpc':'2.0', 'id':'qwer',
                         'method':'aria2.tellWaiting',
                         'params':['token:'+TOKEN, 0, 100,
                                    ['gid', 'status', 'dir', 'totalLength',
                                     'completedLength', 'downloadSpeed', 'files',
                                     'errorCode', 'errorMessage', 'connections',
                                     'pieceLength', 'numPieces', 'connections']]})
    c = opener.open(JSONRPC_LINK, jsonreq)
    data = json.load(c)['result']
    return data

# returns a list of downloads with status == stopped.
# each element of list is a the same object that tell_status_download returns.
def tell_stopped_download_rpc():
    jsonreq = json.dumps({'jsonrpc':'2.0', 'id':'qwer',
                         'method':'aria2.tellStopped',
                         'params':['token:'+TOKEN, -1, 100,
                                    ['gid', 'status', 'dir', 'totalLength',
                                     'completedLength', 'downloadSpeed', 'files',
                                     'errorCode', 'errorMessage', 'connections',
                                     'pieceLength', 'numPieces', 'connections']]})
    c = opener.open(JSONRPC_LINK, jsonreq)
    data = json.load(c)['result']
    return data
