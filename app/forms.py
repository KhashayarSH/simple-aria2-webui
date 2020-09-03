from flask_wtf import FlaskForm
from flask_wtf.html5 import URLField
from wtforms import SubmitField, HiddenField, StringField
from wtforms.validators import url, DataRequired

class AddDownloadForm(FlaskForm):
    url = URLField('', validators=[url(), DataRequired()])
    submit = SubmitField('Add Download')

class ChangeUrlForm(FlaskForm):
    url = URLField('', validators=[url(), DataRequired()])
    gid = HiddenField('')
    change_url = SubmitField('Change URL')

class DownloadControlForm(FlaskForm):
    gid = HiddenField('gid')
    status = HiddenField()
    control_button = SubmitField()

class AddQueueForm(FlaskForm):
    name = StringField('', validators=[DataRequired()])
    submit = SubmitField('Add Queue')

class QueueControlForm(FlaskForm):
    name = StringField('', validators=[DataRequired()])
    original_name = HiddenField('')
    submit = SubmitField('Update Queue')

class DeleteQueueForm(FlaskForm):
    name = HiddenField('')
    Delete_button = SubmitField()

class ChangeQueueForm(FlaskForm):
    gid = HiddenField('')
