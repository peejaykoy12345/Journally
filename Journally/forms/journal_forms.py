from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class CreateJournalForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    create = SubmitField("Create Journal")

class CreateJournalPageForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    content = StringField("Content", validators=[DataRequired()])
    create = SubmitField("Create Page")

class EditJournalPageForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    content = StringField("Content", validators=[DataRequired()])
    create = SubmitField("Save Edits")

class DeleteButton(FlaskForm):
    delete = SubmitField("Delete")