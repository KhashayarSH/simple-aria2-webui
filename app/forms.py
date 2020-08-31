from flask_wtf import FlaskForm
from flask_wtf.html5 import URLField
from wtforms import SubmitField, HiddenField
from wtforms.validators import url, DataRequired

FILTERS = ['error', 'complete', 'paused', 'waiting', 'active', 'removed']

class AddDownloadForm(FlaskForm):
    url = URLField('URL', validators=[url(), DataRequired()])
    submit = SubmitField('Add Download')

class ChangeUrlForm(FlaskForm):
    url = URLField('', validators=[url(), DataRequired()])
    gid = HiddenField('')
    change_url = SubmitField('Change URL')

class DownloadControlForm(FlaskForm):
    gid = HiddenField('gid')
    status = HiddenField()
    control_button = SubmitField()
