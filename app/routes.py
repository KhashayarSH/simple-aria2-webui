from flask import render_template, flash, redirect, url_for, request, send_file
from app import app
from forms import AddDownloadForm, ChangeUrlForm, DownloadControlForm, AddQueueForm, QueueControlForm, DeleteQueueForm, ChangeQueueForm
from download_manager_functions import get_downloads_dm, get_queues_dm, get_downloads_queue_dm, get_status_dm, add_download_dm, remove_download_dm, pause_download_dm, unpause_download_dm, change_download_link_dm, change_download_queue_dm, add_queue_dm, delete_queue_dm, update_queue_dm
from config import BASE_DIR
import json, os, time

filters = ['error', 'complete', 'paused', 'waiting', 'active', 'removed']
displayed_queue = 'All Downloads'

@app.route('/', methods=['GET','POST'])
@app.route('/index', methods=['GET','POST'])
def index():
    queues = get_queues_dm()
    downloads_queue = get_downloads_queue_dm()
    if request.method == 'POST':
        global displayed_queue
        displayed_queue = request.form['queue-select']
        global filters
        filters = []
        for item in request.form:
            filters.append(item)
    change_url_form = ChangeUrlForm()
    download_control_form = DownloadControlForm()
    change_queue_form = ChangeQueueForm()
    downloads = get_downloads_dm(filters, displayed_queue)
    return render_template('index.html', title='Aria2 webui',
                            downloads = downloads,
                            change_url_form = change_url_form,
                            download_control_form = download_control_form, queues=queues, downloads_queue=downloads_queue, change_queue_form=change_queue_form)

@app.route('/index/change_url', methods=['GET','POST'])
def change_url():
    change_url_form = ChangeUrlForm()
    if change_url_form.validate_on_submit():
        flash('URL Changed Successfully', 'success')
        change_download_link_dm(change_url_form.gid.data, change_url_form.url.data)
    return redirect(url_for('index'))

@app.route('/index/download_control', methods=['GET','POST'])
def download_control():
    if request.method == 'POST':
        current_download_status = get_status_dm(request.form['gid'])['status']
        if request.form['control-button'] == 'play':
            if current_download_status == 'waiting' or current_download_status == 'active':
                pause_download_dm(request.form['gid'])
            elif current_download_status == 'paused':
                unpause_download_dm(request.form['gid'])
        elif request.form['control-button'] == 'remove':
            remove_download_dm(request.form['gid'])
    return redirect(url_for('index'))

@app.route('/add_download', methods=['GET','POST'])
def add_download():
    queues = get_queues_dm()
    add_download_form = AddDownloadForm()
    if add_download_form.validate_on_submit():
        flash('Download added', 'success')
        add_download_dm(add_download_form.url.data, request.form['queue-field'])
        return redirect(url_for('add_download'))
    return render_template('add_download.html', title='Add Download', add_download_form=add_download_form, queues = queues)

@app.route('/queues', methods=['GET','POST'])
def queues():
    queues = get_queues_dm()
    queue_control_form = QueueControlForm()
    delete_queue_form = DeleteQueueForm()
    add_queue_form = AddQueueForm()
    if add_queue_form.validate_on_submit():
        flag = 1
        if add_queue_form.name.data == "Main Queue":
            flag = 0
        for item in queues:
            if item['name'] == add_queue_form.name.data:
                flag = 0
                break
        if flag and request.form['start'] and request.form['finish']:
            flash('Queue added', 'success')
            add_queue_dm(request.form['name'], request.form['start'], request.form['finish'])
        if not request.form['start'] or not request.form['finish']:
            flash('All fields of time fields must have values', 'error')
        if not flag:
            flash('Queue name is duplicate', 'error')
        return redirect(url_for('queues'))
    queues = get_queues_dm()
    return render_template('queues.html', title='Queues', add_queue_form = add_queue_form, queue_control_form = queue_control_form, queues = queues, delete_queue_form = delete_queue_form)

@app.route('/queues/queue_control', methods=['GET','POST'])
def queue_control():
    queue_control_form = QueueControlForm()
    queues = get_queues_dm()
    print (queue_control_form.validate_on_submit())
    if request.method == "POST":
        print(request.form)
        flag = 1
        for item in queues:
            if item['name'] == request.form['name']:
                flag = 0
                break
        if flag and request.form['start'] and request.form['finish']:
            flash('Queue Updated', 'success')
            update_queue_dm(request.form['original_name'], request.form['name'], request.form['start'], request.form['finish'])
        if not request.form['start'] or not request.form['finish']:
            flash('All fields of time fields must have values', 'error')
        if not flag:
            flash('Queue name is duplicate', 'error')
    return redirect(url_for('queues'))

@app.route('/queues/delete_queue', methods=['GET','POST'])
def delete_queue():
    if request.method == 'POST':
        delete_queue_dm(request.form['name'])
    return redirect(url_for('queues'))

@app.route('/index/change_queue', methods=['GET','POST'])
def change_queue():
    if request.method == 'POST':
        change_download_queue_dm(request.form['gid'], request.form['change_queue'])
    return redirect(url_for('index'))

@app.route('/downloads', defaults={'req_path': ''})
@app.route('/downloads/<req_path>')
def downloads(req_path):
    # Joining the base and the requested file
    if req_path:
        abs_path = os.path.join(BASE_DIR, req_path)
    else:
        abs_path = BASE_DIR
    # directory contents
    files = os.listdir(BASE_DIR)
    remove_list=[]
    for file in files:
        if file[-6:] == '.aria2':
            remove_list.append(file)

    for file in remove_list:
        files.remove(file)
    files=sorted(files)
    files_with_data = []
    for file in files:
        file_path = os.path.join(BASE_DIR, file)
        new_file = {
            "date" : time.ctime(os.path.getmtime(file_path)),
            "name" : file,
            "size" : os.path.getsize(file_path)
        }
        files_with_data.append(new_file)
    # Return 404 if path doesn't exist
    if req_path != '' and req_path not in files:
        return render_template('404.html')

    # Check if path is a file and serve
    if req_path in files and os.path.isfile(abs_path):
        return send_file(abs_path)

    return render_template('downloads.html', files=files_with_data)
