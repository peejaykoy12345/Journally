from flask import Blueprint, render_template, redirect, url_for, abort, request
from flask_login import login_required, current_user
from Journally import db
from Journally.models import Journal, JournalPage
from Journally.forms.journal_forms import CreateJournalForm, CreateJournalPageForm, EditJournalPageForm, DeleteButton, EditButton

journal_bp = Blueprint("journal", __name__)

@journal_bp.route("/journals")
@login_required
def journals():
    journals = Journal.query.filter_by(owner_id=current_user.id).all()

    delete_button = DeleteButton()

    return render_template("journal/list.html", journals=journals, delete_button=delete_button)

@journal_bp.route("/create_journal", methods=["POST", "GET"])
@login_required
def create_journal():
    form = CreateJournalForm()
    if form.validate_on_submit():
        journal = Journal(title = form.title.data, owner_id=current_user.id)
        db.session.add(journal)
        db.session.commit()
        return redirect(url_for("journal.journals"))
    return render_template("journal/create_journal.html", form=form)

@journal_bp.route("/create_journal_page/<int:journal_id>", methods=["POST", "GET"])
@login_required
def create_journal_page(journal_id):
    form = CreateJournalPageForm()
    if form.validate_on_submit():
        journal_page = JournalPage(
            title = form.title.data,
            content = form.content.data,
            owner_id = current_user.id,
            journal_id = journal_id
        )
        db.session.add(journal_page)
        db.session.commit()
        return redirect(url_for("journal.view_journal", journal_id = journal_id))
    return render_template("journal/create_journalpage.html", form=form)

@journal_bp.route("/edit_journal_page/<int:journal_page_id>", methods=["GET", "POST"])
@login_required
def edit_journal_page(journal_page_id):
    page = JournalPage.query.filter_by(id=journal_page_id, owner_id=current_user.id).first_or_404()

    if page.owner_id != current_user.id:
        abort(403)
    form = EditJournalPageForm()
    if request.method == "POST":
        page.title = form.title.data
        page.content = form.content.data
        db.session.commit()
        return redirect(url_for("journal.view_journal", journal_id = page.journal_id))
    if request.method == "GET":
        form.title.data = page.title
        form.content.data = page.content
    return render_template("journal/edit_journal_page.html", form=form)

@journal_bp.route("/journal/<int:journal_id>")
@login_required
def view_journal(journal_id):
    journal = Journal.query.filter_by(id=journal_id, owner_id=current_user.id).first_or_404()

    edit_button = EditButton()
    delete_button = DeleteButton()

    if current_user.id != journal.owner_id:
        abort(403)

    page_num = request.args.get("page", 1, type=int)

    pages = JournalPage.query.filter_by(journal_id=journal.id)\
                      .order_by(JournalPage.date_posted.desc())\
                      .paginate(page=page_num, per_page=5)

    return render_template("journal/view_journal.html", journal=journal, pages=pages, edit_button=edit_button,delete_button=delete_button)

@journal_bp.route("/delete_journal/<int:journal_id>", methods=["POST", "GET"])
@login_required
def delete_journal(journal_id):
    journal = Journal.query.get_or_404(journal_id)

    if journal.owner_id != current_user.id:
        abort(403)

    for page in journal.journal_pages:
        db.session.delete(page)

    db.session.delete(journal)
    db.session.commit()
    
    return redirect(url_for("journal.journals"))

@journal_bp.route("/delete_journal_page/<int:page_id>", methods=["POST", "GET"])
@login_required
def delete_journal_page(page_id):
    page = JournalPage.query.get_or_404(page_id)

    if page.owner_id != current_user.id:
        abort(403)

    db.session.delete(page)
    db.session.commit()

    return redirect(url_for("journal.view_journal", journal_id=page.journal_id))