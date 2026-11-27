# Tsavo Innovation & Incubation Hub Website

A Django 5.2 institutional website for the Tsavo Innovation & Incubation Hub (TIIH), an organ of Taita Taveta University. The public site has eight pages, a searchable innovation showcase, programme and partnership information, direct contact details, and responsive imagery. The Contact page has no enquiry form; historical enquiries remain available only in the admin.

The design uses the project brief's preliminary green and blue palette. It is visually connected to TTU's current public website but does not claim these colours or the bundled system font stack are certified brand standards. The supplied TIIH logo is integrated in the header, footer, and browser icon. The hero and homepage introduction photographs come from the supplied TIIH presentation; replace any remaining temporary imagery when approved institutional assets are available.

## Technology

- Python 3.12 (pinned in `pyproject.toml`) and Django 5.2 LTS
- SQLite locally; PostgreSQL via `DATABASE_URL`
- Django templates, ORM, forms, authentication, permissions, admin, and sitemaps
- Locally bundled Bootstrap 5, Bootstrap Icons, custom CSS, and vanilla JavaScript
- Pillow for image validation; `python-dotenv` and `dj-database-url` for configuration

## Project structure

```text
apps/
  core/       Site settings, banners, and fixed institutional website content
  services/   Fixed presentation of the seven official service categories
  projects/   Project catalogue and individually approved detail pages
  team/       Approved team profiles
  events/     Admin-managed upcoming events used on the homepage and programmes page
  contact/    Direct contact details, campus directions, and archived enquiries
templates/    Shared and page-specific Django templates
static/       CSS, JavaScript, official branding, and local fallback images
media/        Runtime uploads (ignored by Git)
scripts/      Vercel database preparation during builds
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
With the copied `.env.example`, `createsuperuser` creates an account in local SQLite, not in the deployed PostgreSQL database.

If PowerShell blocks activation, use the environment's Python directly:

```powershell
.\.venv\Scripts\python.exe manage.py runserver
```

## Environment configuration

Copy `.env.example` to `.env` for local development. Leave `DATABASE_URL` empty to use SQLite. Never commit `.env` or use the production database URL for routine local development. Production variables are listed under [Deploying to Vercel](#deploying-to-vercel).

## Initial content

Run:

```powershell
python manage.py seed_initial_data
```

The command is idempotent and does not overwrite administrator edits. It creates the database-backed site settings and eight page banners. The Chairman's message, values, focus areas, programme stories, partnerships, and services are intentionally fixed in source code rather than stored in database tables. The unused achievement storage model is also absent, and the website does not invent unverified achievements. Use `--reset` only when you intentionally want to restore the seeded settings and banners.

Database migrations add the three innovation projects identified in the supplied TIIH presentation, plus Blood Bank Management System from the subsequent project brief. In a fresh database, the homepage features Hydro-Pellets, Blood Bank Management System, and Blue Bin in that order; the catalogue also lists Hydro-Pellets first. Administrators can change publication, feature flags, and order. The multilingual learning project is published in the catalogue but is not featured on the homepage. Blue Bin uses the presentation's group photograph on the homepage and its runner-up graphic in the catalogue and, if enabled, its detail page. Development stages remain unset where none were supplied; Blue Bin also has no stated focus area or technical description. Only Hydro-Pellets has a public detail page initially. To open another project's detail page, review its content and enable **Details public** in the project admin; this adds its View project links and sitemap entry.

The November 2026 chairman feedback adds eight named team members through a data migration. Their roles and biographies remain empty until the hub supplies approved details. Amina Ndinya and Anne Nyabuti now use supplied static portraits; other members without photos use monograms. The same release adds the Programmes and Events and Collaborations & Partnerships pages. The 29 September 2026 Whitebox boot camp is presented as a past activity; only admin-published future events appear under Upcoming events.

## Managing content

Sign in at `/admin/` with an authorized Django staff account. The branded login leads to Django's standard admin dashboard and model editors. Use **Innovation Projects** and **Events** to add or manage content; staff see only the sections their permissions allow, while a superuser sees all registered models. Projects can have a cover and gallery; event records can include an image and registration link. Leave **Published** unchecked while preparing content. Only published events with a future start time appear on the homepage. Administrator sign-in currently uses a password only.

- **Site settings:** public description, contact details, the chairman's WhatsApp number, vision, mission, main objective, location, and optional map URL. Clear the WhatsApp number to hide the floating button. Identity and social URL fields are editable in the admin but are not currently rendered by the public templates.
- **Page banners:** text, alt text, and optional uploaded image. Uploads override named static fallbacks.
- **Innovation projects:** review the four project profiles and add project information, cover, gallery, stage, category, approved public team information, and publishing/featured flags. The homepage order field controls featured-card placement. Uploaded covers replace the bundled project images.
- **Team members:** add approved profiles and each person's LinkedIn URL in `/admin/`. Dr. Mwakio Mwagandi's chairman profile appears first and uses the supplied LinkedIn URL. Each card shows only a LinkedIn icon; until a member's own URL is added, the icon opens the supplied Japhes Murithi contact link. The Chairman, Amina Ndinya and Anne Nyabuti use bundled portraits until a team photo is uploaded. Eight additional names are preloaded from the chairman's feedback without invented roles or biographies.
- **Events:** add upcoming activities and control their publication status. Published future events appear on the homepage and Programmes and Events page.
- **Homepage content:** published, featured innovation projects appear on the homepage. If none are available, the showcase has an empty state. When no future events are published, the events section says there are no upcoming events.
- **Fixed institutional content:** the Chairman's message, services, programme stories, partnerships, values, and focus areas are code-managed and do not appear in `/admin/` or the database. Achievements also have no database model; add only approved achievement content directly to the website if it is supplied later.
- **Chairman portrait:** the supplied photograph of Dr. Mwakio Mwagandi is bundled with the website.
- **Contact messages:** historical inquiries remain private to authorized Django administrators. The public form and submission endpoint are currently disabled. Their model and migrations are retained so existing records remain accessible.

## Images

Bundled website images live in `static/images/`. Local administrator uploads live under `media/`; do not copy them into `static/`.

Tracked fallback images in `static/images/` must exist in the local checkout to appear locally, even when a clean Vercel deployment still has them. Local development uses `media/` for administrator uploads; the deployed site uses Vercel Blob, so production uploads do not automatically appear in a local `media/` folder. After pulling changes, apply migrations to the intended local database and run the static-asset test before troubleshooting missing images.

## Tests and checks

```powershell
python manage.py check
python manage.py makemigrations --check --dry-run
python manage.py test
```

Run `python manage.py check --deploy` with production-like environment variables; local `DJANGO_DEBUG=True` will produce deployment warnings. The GitHub Actions workflow runs this check, Django tests, and `pip-audit` on pushes and pull requests. Tests cover public pages, project publication, admin content editing, login throttling, event visibility, static assets, sitemap, and contact-message privacy.

## Deploying to Vercel

The repository uses [Vercel's Django support](https://vercel.com/changelog/zero-configuration-django-support). Vercel detects `manage.py`, uses the WSGI entry point declared in `pyproject.toml`, installs Python dependencies from `pyproject.toml`, runs its configured build script, and collects static files from `STATIC_ROOT` for its CDN. `requirements.txt` mirrors the dependencies for local setup and CI; keep the two files in sync. See the [Vercel Python runtime documentation](https://vercel.com/docs/functions/runtimes/python) for supported dependency files and Python versions.

The deployment architecture is:

- **Application:** Vercel native Django/Python runtime.
- **Database:** Neon PostgreSQL connected through the Vercel Marketplace.
- **Static files:** Vercel CDN, built from `STATIC_ROOT`.
- **Uploaded public website images:** a public Vercel Blob store.
- **Schema and initial content:** `scripts/vercel_build.py` runs migrations and the idempotent `seed_initial_data` command during deployment.

### 1. Import the repository

In Vercel, select **Add New > Project**, import `JAPHES/tsavo_innovation-incubation_hub_website`, and leave the project root at the repository root. Vercel should identify it as a Python/Django project; do not add a framework override or an output directory.

### 2. Connect PostgreSQL

Connect Neon Postgres to the Vercel project. If Preview deployments are enabled, use a separate Neon branch or database: the build script runs migrations and seeding against whichever database URL that deployment receives. Confirm `DATABASE_URL` exists in each intended environment; `DATABASE_URL_UNPOOLED` is preferred for migrations when available. Do not add a custom variable prefix unless you also update the application to read the prefixed names. The build stops when neither database URL is available.

### 3. Create persistent image storage

Connect a **Public** Vercel Blob store for website images and enable a read-write token variable named `BLOB_READ_WRITE_TOKEN` for Production. This project's Python storage adapter currently requires that exact variable; an OIDC-only connection will not activate it. If Preview deployments need uploads, use a separate Preview store and token. Without `BLOB_READ_WRITE_TOKEN`, Django falls back to local filesystem storage, which is not persistent on Vercel. Public Blob URLs can be opened by anyone with the URL, so upload only approved public images. Local development uses `media/`. See [Vercel Blob setup](https://vercel.com/docs/vercel-blob/using-blob-sdk).

### 4. Add production environment variables

In **Project Settings > Environment Variables**, add these to Production and Preview as appropriate:

```text
DJANGO_DEBUG=False
DJANGO_SECRET_KEY=<a long unique random value>
ALLOWED_HOSTS=tiih.secora.dev,<your-project>.vercel.app
CSRF_TRUSTED_ORIGINS=https://tiih.secora.dev,https://<your-project>.vercel.app
SITE_ORIGIN=https://tiih.secora.dev
```

`DATABASE_URL`, optional `DATABASE_URL_UNPOOLED`, and `BLOB_READ_WRITE_TOKEN` should come from the connected resources. Replace `<your-project>` with the actual Vercel hostname. With `DJANGO_DEBUG=False`, the app defaults to HTTPS redirect, secure session and CSRF cookies, and one-year HSTS; these can be configured explicitly if needed. The build stops on Django deployment-check warnings before applying database migrations.

Administrator sign-in currently uses passwords only. Keep Preview and Production database and Blob resources separate. The public Contact page has no form, so it does not send email notifications.

### 5. Deploy

Push to the production branch or redeploy after the database, Blob store, and required environment variables are connected. During the build, the script uses the unpooled database URL when available, applies migrations, and creates missing seed records without overwriting later administrator edits.

### 6. Create an administrator on a new database

Provision the account against the intended database. The local setup command above creates a local-only account. If an authorized operator can retrieve Production environment variables, they can use the Vercel CLI from a trusted machine:

```powershell
npm install -g vercel
vercel login
vercel link
vercel env pull .env --environment=production
python manage.py createsuperuser
```

This works only if the Production database URL is available to the CLI; sensitive variables may be inaccessible. Never commit `.env` or leave production credentials on a shared machine. Sign in at `/admin/`, upload a small test image, save the record, and confirm its URL uses `blob.vercel-storage.com`.

### 7. Final verification

Check `https://tiih.secora.dev/` and the generated Vercel URL. Visit `/about/`, `/services/`, `/projects/`, `/programmes-events/`, `/partnerships/`, `/team/`, `/contact/`, `/admin/`, and `/sitemap.xml`. Confirm only projects with **Details public** enabled link to a detail page; confirm the Contact page shows the expected email, phone, campus map, and Room C14 directions without a form. Verify that an admin-uploaded image is served from Blob and that public static assets load.

## Production notes

Before each production release, review approved institutional content, office details, database backups, Vercel/Neon access, and the GitHub security workflow. Review service usage limits for the selected plans and run `python manage.py check --deploy` with production-like settings.
