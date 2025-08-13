from flask import Blueprint, render_template, redirect, url_for, abort, request
from flask_login import login_required, current_user
from Journally import db
from Journally.models import Journal, JournalPage
from Journally.forms.journal_forms import CreateJournalForm, CreateJournalPageForm, EditJournalPageForm

journal_bp = Blueprint("journal", __name__)

@journal_bp.route("/journals")
@login_required
def journals():
    journals = Journal.query.filter_by(owner_id=current_user.id).all()

    return render_template("journal/list.html", journals=journals)

@journal_bp.route("/create_journal", methods=["POST", "GET"])
def create_journal():
    form = CreateJournalForm()
    if form.validate_on_submit():
        journal = Journal(title = form.title.data, owner_id=current_user.id)
        db.session.add(journal)
        db.session.commit()
        return redirect(url_for("journal.journals"))
    return render_template("journal/create_journal.html", form=form)

@journal_bp.route("/journal/<int:journal_id>")
@login_required
def view_journal(journal_id):
    journal = Journal.query.filter_by(id=journal_id, user_id=current_user.id).first_or_404()

    if current_user.id != journal.owner_id:
        abort(403)

    page_num = request.args.get("page", 1, type=int)

    pages = JournalPage.query.filter_by(journal_id=journal.id)\
                      .order_by(JournalPage.created_at.desc())\
                      .paginate(page=page_num, per_page=5)

    return render_template("journal/view.html", journal=journal, pages=pages)
