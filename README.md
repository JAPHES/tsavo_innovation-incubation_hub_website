# Tsavo Innovation & Incubation Hub Website

A complete Django 5.2 institutional website for the Tsavo Innovation & Incubation Hub (TIIH), operating under Taita Taveta University. The public site has six principal pages, an admin-managed homepage, a searchable project showcase, a secure inquiry form, SEO basics, and responsive local imagery.

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
  core/       Site settings, banners, Chair message, programmes, values, focus areas, achievements
  services/   Seven official service categories
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
py -3.14 -m venv .venv
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

The command is idempotent and does not overwrite administrator edits. It creates the verified/general site settings, exact supplied vision and mission, six banners, seven services, four values, six focus areas, five general programme areas, and the clearly marked Chair placeholder. Use `--reset` only when you intentionally want to restore these seeded records.

Optional layout-only project records can be created with:

```powershell
python manage.py seed_demo_projects
```

They are labelled `[DEMO]` and remain unpublished.

## Managing content

Sign in at `/admin/` with a Django superuser.

- **Site settings:** contact details, vision, mission, location, verified social links, and optional verified map URL.
- **Page banners:** text, alt text, and optional uploaded image. Uploads override named static fallbacks.
- **Chair's message:** enter the approved name, title, message, portrait, and published state. Until then, the public site clearly labels the content as awaiting official information.
- **Services:** edit copy, icons, order, and publication.
- **Innovation projects:** add project information, cover, gallery, stage, category, approved public team information, and publishing/featured flags.
- **Team members:** add only approved profiles and contact links, then control ordering and active state.
- **Programmes, events, and achievements:** only published records appear publicly.
- **Homepage fallback content:** when no featured innovations or future events are published, the homepage shows three sample innovation features with dedicated imagery and three upcoming activities so the layout remains complete. Published admin records replace this fallback content automatically.
- **Chair portrait:** the bundled chair image is an AI-generated, non-identifying placeholder and must be replaced with an approved photograph of Dr. Mwakio Mwagandi before formal launch.
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

The tests cover public pages, homepage order, fallbacks, service publishing, project search/filtering/pagination/detail permissions, team ordering, event date handling, inquiry validation/CSRF/PRG duplicate protection/privacy, static assets, sitemap, and robots instructions.

## Production notes

The site is PostgreSQL-ready but deployment infrastructure is intentionally not fabricated. Before going live, provide the real domain, authentic logos, approved Chair content, approved team/project/event/achievement content, confirmed office location and map URL, SMTP credentials, production storage, HTTPS, backups, and an application server/reverse proxy. Run `collectstatic` and review `check --deploy` in the actual deployment environment.
