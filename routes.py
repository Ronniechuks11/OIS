from flask import Blueprint, current_app, flash, redirect, render_template, url_for
from flask_mail import Message

from extensions import db, mail
from forms import AdmissionsInquiryForm, ContactForm
from models import Inquiry

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index():
    return render_template("index.html")


@main_bp.route("/about")
def about():
    return render_template("about.html")


@main_bp.route("/programmes")
def programmes():
    return render_template("programmes.html")


@main_bp.route("/life")
def life():
    return render_template("life.html")


@main_bp.route("/admissions", methods=["GET", "POST"])
def admissions():
    form = AdmissionsInquiryForm()

    if form.validate_on_submit():
        inquiry = Inquiry(
            source="admissions",
            name=form.parent_name.data.strip(),
            email=form.email.data.strip(),
            child_name=(form.child_name.data or "").strip() or None,
            grade=form.grade.data,
            message=(form.message.data or "").strip() or None,
        )
        db.session.add(inquiry)
        db.session.commit()
        _send_inquiry_notification(inquiry)
        flash(
            "Thanks — we've received your inquiry and will follow up to arrange a tour.",
            "success",
        )
        return redirect(url_for("main.admissions", _anchor="apply"))

    if form.errors:
        flash("Please check the highlighted fields below and try again.", "error")

    return render_template("admissions.html", form=form)


@main_bp.route("/contact", methods=["GET", "POST"])
def contact():
    form = ContactForm()

    if form.validate_on_submit():
        inquiry = Inquiry(
            source="contact",
            name=form.name.data.strip(),
            email=form.email.data.strip(),
            subject=form.subject.data,
            message=form.message.data.strip(),
        )
        db.session.add(inquiry)
        db.session.commit()
        _send_inquiry_notification(inquiry)
        flash("Thanks for reaching out — we'll get back to you shortly.", "success")
        return redirect(url_for("main.contact"))

    if form.errors:
        flash("Please check the highlighted fields below and try again.", "error")

    return render_template("contact.html", form=form)


def _send_inquiry_notification(inquiry: Inquiry) -> None:
    """Best-effort email notification. Never blocks or fails the request —
    the inquiry is already safely committed to the database by the time
    this runs, so a mail-server hiccup should not show the visitor an error.
    """
    if not current_app.config.get("MAIL_SERVER"):
        current_app.logger.info(
            "MAIL_SERVER not configured — skipping email for inquiry id=%s "
            "(saved to database only)",
            inquiry.id,
        )
        return

    lines = [f"New {inquiry.source} inquiry from {inquiry.name} <{inquiry.email}>", ""]
    if inquiry.child_name:
        lines.append(f"Child's name: {inquiry.child_name}")
    if inquiry.grade:
        lines.append(f"Grade applying for: {inquiry.grade}")
    if inquiry.subject:
        lines.append(f"Subject: {inquiry.subject}")
    if inquiry.message:
        lines.append("")
        lines.append("Message:")
        lines.append(inquiry.message)

    try:
        msg = Message(
            subject=f"OIS website — new {inquiry.source} inquiry",
            recipients=[current_app.config["ADMIN_EMAIL"]],
            body="\n".join(lines),
        )
        mail.send(msg)
    except Exception:
        current_app.logger.exception(
            "Failed to send inquiry notification email (id=%s)", inquiry.id
        )
