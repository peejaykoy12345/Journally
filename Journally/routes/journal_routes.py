from flask import Blueprint, render_template
from flask_login import login_required, current_user
from Journally.models import Journal, JournalPage
from Journally.forms.journal_forms import CreateJournalForm, CreateJournalPageForm, EditJournalPageForm

journal_bp = Blueprint("journal", __name__)

@journal_bp.route("/journals")
@login_required
def journals():
    journals = Journal.query.filter_by(owner_id=current_user.id).all()

    return render_template("journal/list.html", journals=journals)

@journal_bp.route("/create_journal")
def create_journal():
    form = CreateJournalForm()
    return render_template("journal/create_journal.html", form=form)