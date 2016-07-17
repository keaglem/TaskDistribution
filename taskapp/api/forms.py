from flask_wtf import Form
from flask_wtf.file import FileField
import wtforms as wtf
from wtforms.validators import InputRequired, NumberRange


class UploadForm(Form):
    script_name = wtf.StringField('Script Name', [InputRequired()])
    script_version = wtf.DecimalField('Script Version', [InputRequired()])
    simulation_name = wtf.StringField('Simulation Name', [InputRequired()])
    simulation_version = wtf.DecimalField('Simulation Version', [InputRequired()])
    file = FileField('Script File', validators=[InputRequired()],
                     description='Script file listing simulations')
    submit_button = wtf.SubmitField('Upload Form')

