# Tsavo Innovation & Incubation Hub Website

A complete Django 5.2 institutional website for the Tsavo Innovation & Incubation Hub (TIIH), operating under Taita Taveta University. The public site has six principal pages, a searchable project showcase, a secure inquiry form, SEO basics, and responsive local imagery.

The design uses the project brief's preliminary green and blue palette. It is visually connected to TTU's current public website but does not claim these colours or the bundled system font stack are certified brand standards. The supplied TIIH logo is integrated in the header, footer, and browser icon; replace the remaining temporary photography and TTU placeholder with approved institutional assets before launch.

## Technology

- Python 3.12+ and Django 5.2 LTS
- SQLite locally; PostgreSQL via `DATABASE_URL`
- Django templates, ORM, forms, authentication, permissions, admin, and sitemaps
- Bootstrap 5, Bootstrap Icons, custom CSS, and vanilla JavaScript
- Pillow for image validation; `python-dotenv` and `dj-database-url` for configuration

## Project structure

```text
apps/
  core/       Site settings, banners, and fixed institutional website content
  services/   Fixed presentation of the seven official service categories
  projects/   Project catalogue, filtering, details, gallery
  team/       Approved team profiles
  events/     Admin-managed events used on the homepage
  contact/    Validated private inquiry workflow
templates/    Shared and page-specific Django templates
static/       CSS, JavaScript, branding placeholders, and local fallback images
media/        Runtime uploads (ignored by Git)
tsavo_hub/    Project settings and root URLs
```

## Windows PowerShell setup

From the `tsavo-hub-website` folder:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
Copy-Item .env.example .env
python manage.py migrate
python manage.py seed_initial_data
python manage.py createsuperuser
python manage.py runserver
```

Open `http://127.0.0.1:8000/`. The administration site is at `http://127.0.0.1:8000/admin/`.

If PowerShell blocks activation, use the environment's Python directly:

```powershell
.\.venv\Scripts\python.exe manage.py runserver
```

## Environment configuration

Copy `.env.example` to `.env`. Never commit `.env`. Local development defaults to SQLite and the console email backend. For production:

1. Set `DJANGO_DEBUG=False`.
2. Supply a strong `SECRET_KEY`.
3. Set the deployed host in `ALLOWED_HOSTS` and HTTPS origins in `CSRF_TRUSTED_ORIGINS`.
4. Set a PostgreSQL `DATABASE_URL`.
5. Configure SMTP variables and secure-cookie/HTTPS settings.
6. Set `SITE_ORIGIN` only after the real public domain is confirmed.
7. Serve collected static files and user uploads through appropriate production storage.

## Initial content

Run:

```powershell
python manage.py seed_initial_data
```

The command is idempotent and does not overwrite administrator edits. It creates the database-backed site settings and six page banners. The Chair's message, values, focus areas, programmes, achievements, and services are intentionally fixed in source code rather than stored in database tables. Use `--reset` only when you intentionally want to restore the seeded settings and banners.

Optional layout-only project records can be created with:

```powershell
python manage.py seed_demo_projects
```

They are labelled `[DEMO]` and remain unpublished.

## Managing content

Sign in at `/admin/` with a Django superuser.

- **Site settings:** contact details, vision, mission, location, verified social links, and optional verified map URL.
- **Page banners:** text, alt text, and optional uploaded image. Uploads override named static fallbacks.
- **Innovation projects:** add project information, cover, gallery, stage, category, approved public team information, and publishing/featured flags.
- **Team members:** add only approved profiles and contact links, then control ordering and active state.
- **Events:** add upcoming activities and control their publication status.
- **Homepage fallback content:** when no featured innovations or future events are published, the homepage shows three sample innovation features with dedicated imagery and three upcoming activities so the layout remains complete. Published admin records replace this fallback content automatically.
- **Fixed institutional content:** the Chair's message, services, programmes, values, focus areas, and achievements are code-managed and do not appear in `/admin/` or the database.
- **Chair portrait:** the supplied photograph of Dr. Mwakio Mwagandi is bundled with the website.
- **Contact messages:** inquiries are private to authorized Django administrators. Mark them read from the list.

## Images

See [IMAGE_REPLACEMENT_GUIDE.md](IMAGE_REPLACEMENT_GUIDE.md) for every temporary filename, recommended dimensions, location, and replacement workflow. Administrator uploads live under `media/`; do not copy them into `static/`.

## Tests and checks

```powershell
python manage.py check
python manage.py makemigrations --check --dry-run
python manage.py test
python manage.py check --deploy
```

The tests cover public pages, homepage order, fallbacks, fixed-content schema removal, project search/filtering/pagination/detail permissions, team ordering, event date handling, inquiry validation/CSRF/PRG duplicate protection/privacy, static assets, sitemap, and robots instructions.

## Deploying to Vercel

The repository is prepared for Vercel's native Django runtime. Vercel detects `manage.py` and the WSGI entry point, installs `requirements.txt`, runs the build hook in `pyproject.toml`, collects static files for its CDN, and serves the application as a Python Function.

The deployment architecture is:

- **Application:** Vercel native Django/Python runtime.
- **Database:** Neon PostgreSQL connected through the Vercel Marketplace.
- **Static files:** Vercel CDN, built from `STATIC_ROOT`.
- **Uploaded public website images:** a public Vercel Blob store.
- **Schema and initial content:** `scripts/vercel_build.py` runs migrations and the idempotent `seed_initial_data` command during deployment.

### 1. Import the repository

In Vercel, select **Add New > Project**, import `JAPHES/tsavo_innovation-incubation_hub_website`, and leave the project root at the repository root. Vercel should identify it as a Python/Django project; do not add a framework override or an output directory.

### 2. Connect PostgreSQL before the first successful deployment

Open the Vercel project, go to **Storage/Marketplace**, add **Neon Postgres**, and connect it to Production and Preview. Confirm that Vercel has added `DATABASE_URL` and `DATABASE_URL_UNPOOLED`. The build hook deliberately stops with a clear error when no PostgreSQL URL exists, preventing an accidental production SQLite deployment.

### 3. Create persistent image storage

From the project's **Storage** tab, create a **Blob** store with **Public** access and connect it to Production and Preview. Public access is intentional because these uploads are website banners, team portraits, event images, and innovation-gallery images. Vercel injects `BLOB_READ_WRITE_TOKEN`; when that variable is present, Django automatically uses `VercelBlobStorage`. Local development continues to use `media/`.

### 4. Add production environment variables

In **Project Settings > Environment Variables**, add these to Production and Preview as appropriate:

```text
DJANGO_DEBUG=False
DJANGO_SECRET_KEY=<a long unique random value>
ALLOWED_HOSTS=.vercel.app
CSRF_TRUSTED_ORIGINS=https://*.vercel.app
SITE_ORIGIN=https://<your-production-domain>
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
SECURE_HSTS_SECONDS=31536000
```

`DATABASE_URL`, `DATABASE_URL_UNPOOLED`, and `BLOB_READ_WRITE_TOKEN` should come from the connected Vercel resources rather than being entered manually. For a custom domain, add that hostname to `ALLOWED_HOSTS` and its full `https://` origin to `CSRF_TRUSTED_ORIGINS`, separated from existing values with commas.

Configure SMTP before relying on inquiry notifications:

```text
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=<smtp-host>
EMAIL_PORT=587
EMAIL_HOST_USER=<smtp-user>
EMAIL_HOST_PASSWORD=<smtp-password>
EMAIL_USE_TLS=True
DEFAULT_FROM_EMAIL=<verified-sender>
CONTACT_NOTIFICATION_EMAIL=tiih@ttu.ac.ke
```

### 5. Deploy

Redeploy after the database, Blob store, and required environment variables are connected. During the build, Vercel uses the unpooled database URL when available, applies migrations, and creates missing seed records without overwriting later administrator edits.

### 6. Create the first administrator

Install the Vercel CLI locally, link the project, pull the Production variables into the ignored `.env` file, then create the account against the hosted database:

```powershell
npm install -g vercel
vercel login
vercel link
vercel env pull .env --environment=production
python manage.py createsuperuser
```

Never commit `.env`; it is already ignored. Sign in at `/admin/`, upload a small test image, save the record, and confirm the image URL uses `blob.vercel-storage.com`.

### 7. Final verification

Check `/`, `/about/`, `/services/`, `/projects/`, `/team/`, `/contact/`, `/admin/`, and `/sitemap.xml`. Submit one contact inquiry, verify it appears in the admin, and confirm the notification email after SMTP is configured. Add the final custom domain only after the generated Vercel URL is working.

## Production notes

Before public launch, confirm the real domain, approved institutional content, office location and map URL, SMTP credentials, database backups, and ownership of the Vercel/Neon resources. Review Vercel and Neon usage limits for the selected plans and run `python manage.py check --deploy` with the production environment.
