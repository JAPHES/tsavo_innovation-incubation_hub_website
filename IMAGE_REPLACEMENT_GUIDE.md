# TIIH Image Replacement Guide

The banner, homepage introduction, and project photographs listed below come directly from the supplied TIIH presentation. Their original pixels are retained. Some unused older placeholders and generic fallback images remain in the repository. The TIIH logo was supplied by the Hub and is used as the website's identity; the TTU logo remains an explicitly labelled placeholder.

Replace a file with an approved image using the same filename to avoid changing Python or template code. Banner text sits over a CSS gradient for readability; the source photographs are not retouched. Export any future photographs as optimized sRGB JPEGs; use PNG for logos requiring transparency.

| File | Recommended size | Appears on | Replacement notes |
|---|---:|---|---|
| `static/images/banners/tiih_training_hero.png` | 1279 × 670 | Home, Services, Projects, Team, and Contact banners | Original workshop photograph from the supplied presentation. |
| `static/images/banners/tiih_outreach_about.jpeg` | 3712 × 2475 | About Us banner | Original outreach photograph from the supplied presentation. |
| `static/images/home/tiih_ideas_enterprise.png` | 772 × 291 | Homepage “Where ideas meet enterprise” section | Original two-scene image from the supplied presentation, displayed without cropping. |
| `static/images/team/chair_dr_mwakio_mwagandi.jpg` | 900 × 1125 | Homepage Chair message and Team page | Supplied photograph of Dr. Mwakio Mwagandi, used until a team profile photo is uploaded. |
| `static/images/placeholders/project_default.jpg` | 1200 × 800 | Project cards and details without uploads | Keep as a neutral fallback or replace with an approved generic innovation image. |
| `static/images/placeholders/team_member_default.jpg` | 800 × 1000 | Team profiles without uploads | Keep neutral; individual admin uploads take priority. |
| `static/images/branding/tiih_logo.png` | Up to 1000 × 1000 PNG | Header and browser icon | Supplied TIIH logo, optimized without distortion. Replace only with a newly approved official version. |
| `static/images/branding/tiih_logo_round.png` | 420 × 420 transparent PNG | Circular footer logo | Cropped from the supplied official logo for clear display in the footer. |
| `static/images/innovations/upcycled-cotton-hydro-pellets.png` | 497 × 618 | Hydro-pellets project | Award photograph from the supplied TIIH presentation; it shows an award recipient, not the pellets. |
| `static/images/innovations/blue-bin-pwani-innovation-week.png` | 387 × 337 | Blue Bin project | Competition graphic from the supplied TIIH presentation. |
| `static/images/innovations/multilingual-learning-platform.svg` | 1200 × 800 | Multilingual learning project | Concept illustration, not a screenshot of the platform. Replace with an approved product visual when available. |
| `static/images/branding/ttu_logo.png` | 600 × 600 transparent PNG | Reserved institutional asset | Replace with the authentic TTU logo when supplied and approved for this site. |

## Admin-uploaded images

Uploaded images belong under `media/`, never `static/`:

- Page banners: `media/banners/`
- Projects: `media/projects/`
- Project galleries: `media/projects/gallery/`
- Team portraits: `media/team/`
- Events: `media/events/`

The website accepts JPG, PNG, and WebP uploads up to 5 MB by default. An uploaded page banner, project cover, or team portrait automatically overrides its static fallback.

## Image safety checklist

Before publishing, confirm that the hub has permission to use the image, every identifiable person has appropriate consent, alt text is accurate, and no private information is visible. Avoid presenting a temporary or illustrative image as a real TIIH activity.
