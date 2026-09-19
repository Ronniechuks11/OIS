from datetime import datetime, timezone

from extensions import db


class Inquiry(db.Model):
    """One row per form submission, from either admissions.html or contact.html.

    `source` tells the two apart. admissions inquiries populate
    child_name/grade and leave subject empty; contact messages populate
    subject and leave child_name/grade empty.
    """

    __tablename__ = "inquiries"

    id = db.Column(db.Integer, primary_key=True)
    source = db.Column(db.String(20), nullable=False)  # 'admissions' or 'contact'
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    child_name = db.Column(db.String(120))
    grade = db.Column(db.String(60))
    subject = db.Column(db.String(60))
    message = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return f"<Inquiry {self.id} {self.source} {self.name!r}>"
