# TIIH Image Replacement Guide

All bundled photographs are temporary, AI-generated, non-institutional images. They do **not** depict TIIH facilities, personnel, programmes, or projects. The TIIH logo was supplied by the Hub and is used as the website's hub identity; the TTU logo remains an explicitly labelled placeholder.

Replace a file with an approved image using the same filename to avoid changing Python or template code. For banners, keep the main subject away from the left side because page headings are placed there. Export photographs as optimized sRGB JPEGs; use PNG for logos requiring transparency.

| File | Recommended size | Appears on | Replacement notes |
|---|---:|---|---|
| `static/images/banners/home_hero.jpg` | 1920 × 900 | Homepage hero | Wide approved innovation or collaboration photograph; leave space on the left. |
| `static/images/banners/about_banner.jpg` | 1920 × 650 | About Us banner | Approved hub collaboration or facility photograph. |
| `static/images/banners/services_banner.jpg` | 1920 × 650 | Services banner | Approved training, mentoring, or prototyping photograph. |
| `static/images/banners/projects_banner.jpg` | 1920 × 650 | Projects banner | Approved innovation or field-testing photograph. |
| `static/images/banners/team_banner.jpg` | 1920 × 650 | Team banner | Approved group photograph, with consent from everyone shown. |
| `static/images/banners/contact_banner.jpg` | 1920 × 650 | Contact banner | Approved TIIH or TTU location photograph. |
| `static/images/home/about_hub.jpg` | 1400 × 1050 | Homepage About the Hub section | Approved photograph of the hub, students, or facility. |
| `static/images/team/chair_dr_mwakio_mwagandi.jpg` | 900 × 1125 | Homepage Chair message fallback | Supplied photograph of Dr. Mwakio Mwagandi, cropped for the homepage. Admin upload takes priority. |
| `static/images/placeholders/project_default.jpg` | 1200 × 800 | Project cards and details without uploads | Keep as a neutral fallback or replace with an approved generic innovation image. |
| `static/images/placeholders/team_member_default.jpg` | 800 × 1000 | Team profiles without uploads | Keep neutral; individual admin uploads take priority. |
| `static/images/branding/tiih_logo.png` | Up to 1000 × 1000 PNG | Header and browser icon | Supplied TIIH logo, optimized without distortion. Replace only with a newly approved official version. |
| `static/images/branding/tiih_logo_round.png` | 420 × 420 transparent PNG | Circular footer logo | Cropped from the supplied official logo for clear display in the footer. |
| `static/images/innovations/*.jpg` | 1200 × 800 | Homepage innovation showcase | Generated concept photography for the three homepage innovation features. Replace with approved project photography when available. |
| `static/images/branding/ttu_logo.png` | 600 × 600 transparent PNG | Reserved institutional asset | Replace with the authentic TTU logo when supplied and approved for this site. |

## Admin-uploaded images

Uploaded images belong under `media/`, never `static/`:

- Page banners: `media/banners/`
- Projects: `media/projects/`
- Project galleries: `media/projects/gallery/`
- Team and Chair portraits: `media/team/`
- Programmes, events, and achievements: their matching `media/` folders

The website accepts JPG, PNG, and WebP uploads up to 5 MB by default. An uploaded page banner, Chair photo, project cover, or team portrait automatically overrides its static fallback.

## Image safety checklist

Before publishing, confirm that the hub has permission to use the image, every identifiable person has appropriate consent, alt text is accurate, and no private information is visible. Avoid presenting a temporary or illustrative image as a real TIIH activity.
