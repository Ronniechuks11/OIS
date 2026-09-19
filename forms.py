from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, Optional


class AdmissionsInquiryForm(FlaskForm):
    parent_name = StringField(
        "Parent / guardian name", validators=[DataRequired(), Length(max=120)]
    )
    email = StringField("Email", validators=[DataRequired(), Email(), Length(max=120)])
    child_name = StringField("Child's name", validators=[Optional(), Length(max=120)])
    grade = SelectField(
        "Grade applying for",
        choices=[
            ("Preschool", "Preschool"),
            ("Primary (P1–P6)", "Primary (P1–P6)"),
            ("Secondary (S7–S11)", "Secondary (S7–S11)"),
        ],
    )
    message = TextAreaField(
        "Anything else we should know?", validators=[Optional(), Length(max=2000)]
    )


class ContactForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired(), Length(max=120)])
    email = StringField("Email", validators=[DataRequired(), Email(), Length(max=120)])
    subject = SelectField(
        "What's this about?",
        choices=[
            ("General question", "General question"),
            ("Booking a tour", "Booking a tour"),
            ("Admissions", "Admissions"),
            ("Something else", "Something else"),
        ],
    )
    message = TextAreaField("Message", validators=[DataRequired(), Length(max=2000)])
