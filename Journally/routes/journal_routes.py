from flask import Blueprint, render_template
from Journally.models import Journal, JournalPage
from Journally.forms.journal_forms import CreateJournalForm, CreateJournalPageForm, EditJournalPageForm

journal_bp = Blueprint("journal", __name__)

@journal_bp.route("/")
@journal_bp.route("/create_journal")
def create_journal():
    return render_template("journal/create_journal.html")