from flask import render_template, flash, redirect, url_for, request
from app import app
from forms import AddDownloadForm, ChangeUrlForm, DownloadControlForm
from app.aria2rpcfunctions import add_download_rpc, tell_active_download_rpc, tell_waiting_download_rpc, tell_stopped_download_rpc, unpause_all_download_rpc, pause_all_download_rpc, remove_download_rpc, pause_download_rpc, unpause_download_rpc, tell_status_download_rpc, change_url_download_rpc
import json

@app.route('/', methods=['GET','POST'])
@app.route('/index', methods=['GET','POST'])
def index():
    if request.method == 'post':
        request.form.getlist('status_checkbox')

    change_url_form = ChangeUrlForm()
    download_control_form = DownloadControlForm()
    downloads = tell_active_download_rpc()
    downloads += tell_waiting_download_rpc()
    downloads += tell_stopped_download_rpc()
    #print(downloads)
    return render_template('index.html', title='Aria2 webui',
                            downloads = downloads,
                            change_url_form = change_url_form,
                            download_control_form = download_control_form)

@app.route('/index/change_url', methods=['GET','POST'])
def change_url():
    change_url_form = ChangeUrlForm()
    download_control_form = DownloadControlForm()
    if change_url_form.validate_on_submit():
        flash('URL Changed Successfully')
        respose = change_url_download_rpc(change_url_form.gid.data, change_url_form.url.data)
        return redirect(url_for('index'))
    downloads = tell_active_download_rpc()
    downloads += tell_waiting_download_rpc()
    downloads += tell_stopped_download_rpc()
    return render_template('index.html', title='Downloads test',
                            downloads = downloads,
                            change_url_form = change_url_form,
                            download_control_form = download_control_form)

@app.route('/index/download_control', methods=['GET','POST'])
def download_control():
    change_url_form = ChangeUrlForm()
    download_control_form = DownloadControlForm()
    if request.method == 'POST':
        print(request.form)
        current_download_status = tell_status_download_rpc(request.form['gid'])['status']
        if request.form['control-button'] == 'play':
            if current_download_status == 'waiting' or current_download_status == 'active':
                pause_download_rpc(request.form['gid'])
            elif current_download_status == 'paused':
                unpause_download_rpc(request.form['gid'])
        elif request.form['control-button'] == 'remove':
            remove_download_rpc(request.form['gid'])
    downloads = tell_active_download_rpc()
    downloads += tell_waiting_download_rpc()
    downloads += tell_stopped_download_rpc()
    return render_template('index.html', title='Downloads test',
                            downloads = downloads,
                            change_url_form = change_url_form,
                            download_control_form = download_control_form)

@app.route('/add_download', methods=['GET','POST'])
def add_download():
    add_download_form = AddDownloadForm()
    queues = []
    if add_download_form.validate_on_submit():
        flash('Download added')
        respose = add_download_rpc(add_download_form.url.data, 'False')
        return redirect(url_for('index'))
    return render_template('add_download.html', title='Add Download', add_download_form=add_download_form, queues = queues)
