# ---------------------------------------------------------------------------
# HOW TO GET A GMAIL APP PASSWORD (required — your normal Gmail password
# will NOT work here, Google blocks that for security):
#
#   1. Go to https://myaccount.google.com/security
#   2. Turn on "2-Step Verification" if it isn't already on (required
#      before Google will let you create an app password).
#   3. Go to https://myaccount.google.com/apppasswords
#   4. Under "Select app", choose "Mail". Under "Select device", choose
#      "Other" and name it something like "Easy Africa website".
#   5. Google shows you a 16-character code (e.g. "abcd efgh ijkl mnop").
#      Copy it with no spaces and paste it as DJANGO_EMAIL_HOST_PASSWORD
#      below.
#
# This file is for your own reference / local use. On Render (or wherever
# you deploy), set these same values as real environment variables in the
# dashboard — do NOT upload this .env file itself to your repo or host.
# ---------------------------------------------------------------------------

DJANGO_SECRET_KEY=replace-with-a-real-random-secret-key
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=easyafrica.com,www.easyafrica.com

DATABASE_URL=your-neon-connection-string-here

# Gmail SMTP settings
DJANGO_EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
DJANGO_EMAIL_HOST=smtp.gmail.com
DJANGO_EMAIL_PORT=587
DJANGO_EMAIL_USE_TLS=True
DJANGO_EMAIL_HOST_USER=youraddress@gmail.com
DJANGO_EMAIL_HOST_PASSWORD=your16characterapppassword
DJANGO_DEFAULT_FROM_EMAIL=youraddress@gmail.com
CONTACT_FORM_RECIPIENT=youraddress@gmail.com

# Media storage (Cloudinary) — leave blank to use local disk instead
CLOUDINARY_CLOUD_NAME=
CLOUDINARY_API_KEY=
CLOUDINARY_API_SECRET=
