# Odense International School — Flask backend

Converts the static mockup into a working Flask site: Jinja2 `base.html` +
blocks instead of duplicated nav/footer, and both forms (admissions inquiry,
contact) wired to real routes with server-side validation, a shared
`Inquiry` database table, and a best-effort email notification.

## Setup

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env            # then edit .env if you want real email sending
python app.py
```

Visit http://127.0.0.1:5000 — the SQLite database (`instance/ois.db`) and
its `inquiries` table are created automatically on first run.

## How the forms work

- Both forms POST to their own page's route (`/admissions`, `/contact`).
- Flask-WTF validates server-side (required fields, real email format) and
  supplies CSRF protection automatically via `form.hidden_tag()`.
- On success: the submission is saved as a row in the `inquiries` table,
  a best-effort notification email is sent to `ADMIN_EMAIL`, a flash
  message confirms it, and the visitor is redirected back to the same page
  (POST/redirect/GET, so refreshing never re-submits).
- On failure: the page re-renders with the visitor's other answers intact
  and field-level error messages under the offending inputs.
- **Email is optional.** If `MAIL_SERVER` isn't set in `.env`, the app
  skips sending and just logs that it did — inquiries are never lost, they
  just live in the database until you configure email or query it directly.

To read what's come in without setting up email:

```bash
python -c "
from app import create_app
from models import Inquiry
app = create_app()
with app.app_context():
    for i in Inquiry.query.order_by(Inquiry.created_at.desc()).all():
        print(i.created_at, i.source, i.name, i.email)
"
```

## Adding real photos

Drop HD photos into `static/images/`, named exactly as listed in
`static/images/SHOT-LIST.txt` (e.g. `hero-campus.jpg`). Every template
already points at `static/images/...` via `url_for`, so no code changes
are needed — the placeholder `.img-slot` divs will show the real photo as
soon as a same-named file exists.

One thing worth knowing: the `data-label` badge overlay on each
`.img-slot` is driven by CSS (`::after` with `content: attr(data-label)`)
and shows unconditionally — it doesn't detect whether a real image loaded
underneath. Once a page's photos are all in, remove that page's
`data-label` attributes (or I can strip them for you) so the badges
disappear before it goes live.

## Still bracketed in the copy — do not fill these in without the school

- `admissions.html` — application fee, one-time enrollment fee, the
  "can Danish families apply" FAQ answer, and the sibling/relocating-family
  priority policy FAQ answer.
- `contact.html` — office hours.
- `about.html` — the testimonial blockquote (currently a placeholder quote
  and attribution).

## Project layout

```
app.py            # application factory
config.py         # env-driven settings
extensions.py     # db / mail / csrf instances
models.py         # Inquiry model
forms.py          # AdmissionsInquiryForm, ContactForm (Flask-WTF)
routes.py         # all page routes + form handling + email helper
templates/        # base.html + one template per page
static/css, static/js, static/images
```
