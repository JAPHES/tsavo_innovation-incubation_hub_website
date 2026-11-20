# TIIH Image Replacement Guide

The banner, homepage introduction, and project photographs listed below come directly from the supplied TIIH presentation. The Whitebox photographs and flyer came from the chairman's feedback document, and the partner logos came from the partners' official websites. Their original pixels are retained. Older unused image placeholders have been removed. The TIIH logo was supplied by the Hub and is used as the website's identity.

Replace a file with an approved image using the same filename to avoid changing Python or template code. Banner text sits over a CSS gradient for readability; the source photographs are not retouched. Export any future photographs as optimized sRGB JPEGs; use PNG for logos requiring transparency.

| File | Recommended size | Appears on | Replacement notes |
|---|---:|---|---|
| `static/images/banners/tiih_training_hero.png` | 1279 × 670 | Home, Services, Featured Innovations, Team, Contact, and Programmes banners | Original workshop photograph from the supplied presentation. |
| `static/images/banners/tiih_outreach_about.jpeg` | 3712 × 2475 | About Us and Partnerships banners | Original outreach photograph from the supplied presentation. |
| `static/images/home/tiih_ideas_enterprise.png` | 772 × 291 | Homepage “Where we cultivate entrepreneurs” section | Original two-scene image from the supplied presentation, displayed without cropping. |
| `static/images/team/chair_dr_mwakio_mwagandi.jpg` | 900 × 1125 | Homepage Chairman message and Team page | Supplied photograph of Dr. Mwakio Mwagandi, used until a team profile photo is uploaded. |
| `static/images/team/amina_ndinya.jpeg` | 720 × 1136 | Amina Ndinya's Team card | Supplied original photograph, used until a profile photo is uploaded. |
| `static/images/team/anne_nyabuti.jpeg` | 626 × 622 | Anne Nyabuti's Team card | Supplied original photograph, used until a profile photo is uploaded. |
| `static/images/placeholders/project_default.jpg` | 1200 × 800 | Project cards and details without uploads | Keep as a neutral fallback or replace with an approved generic innovation image. |
| `static/images/branding/tiih_logo.png` | Up to 1000 × 1000 PNG | Header and browser icon | Supplied TIIH logo, optimized without distortion. Replace only with a newly approved official version. |
| `static/images/branding/tiih_logo_round.png` | 420 × 420 transparent PNG | Circular footer logo | Cropped from the supplied official logo for clear display in the footer. |
| `static/images/innovations/upcycled-cotton-hydro-pellets.png` | 497 × 618 | Hydro-pellets project | Award photograph from the supplied TIIH presentation; it shows an award recipient, not the pellets. |
| `static/images/innovations/blood-bank-presidential-pitch.jpeg` | 719 × 537 | Blood Bank Management System | Original pitching-festival photograph from the supplied presentation. |
| `static/images/innovations/blue-bin-pwani-innovation-week.png` | 387 × 337 | Blue Bin project | Competition graphic from the supplied TIIH presentation. |
| `static/images/innovations/blue-bin-pwani-group.jpeg` | 1600 × 1384 | Blue Bin homepage card | Original group photograph from the supplied presentation. The runner-up graphic remains on the project detail page and catalogue card. |
| `static/images/innovations/multilingual-learning-platform.svg` | 1200 × 800 | Multilingual learning project | Concept illustration, not a screenshot of the platform. Replace with an approved product visual when available. |
| `static/images/programmes/whitebox-bootcamp-facilitator.png` | 425 × 490 | Programmes and Events page | Original photograph and caption supplied in the chairman's feedback document. |
| `static/images/programmes/whitebox-training-2026-flyer.png` | 495 × 739 | Expandable archive flyer on Programmes and Events page | Original flyer supplied in the chairman's feedback document. The event date has passed. |
| `static/images/partners/mbeya-university-logo.jpg` | 640 × 424 | Partnerships page | Official Mbeya University logo from its website. |
| `static/images/partners/cambridge-judge-logo.png` | 235 × 72 | Programmes and Partnerships pages | Official Cambridge Judge Business School logo from its website. |
| `static/images/partners/africa-2100-logo.png` | 2008 × 467 | Programmes and Partnerships pages | Official Africa 2100 logo from its website. |
| `static/images/partners/taita-taveta-county-logo.png` | 210 × 218 | Partnerships page | Official county emblem from its website. |
| `static/images/icons/whatsapp.svg` | 16 × 16 vector | Floating WhatsApp button | Bootstrap Icons asset stored locally so the contact icon stays visible if the icon CDN is unavailable. |

Team members without approved portraits use a text monogram. Coast Innovation Hubs Network uses a text wordmark until an approved logo is provided.

Partner asset sources: [Mbeya University](https://must.ac.tz/), [Cambridge Judge Business School](https://www.jbs.cam.ac.uk/), [Africa 2100](https://www.africa2100.org/), and [Taita Taveta County Government](https://www.taitataveta.go.ke/).
The WhatsApp symbol comes from [Bootstrap Icons](https://icons.getbootstrap.com/icons/whatsapp/).

## Admin-uploaded images

Locally, administrator-uploaded images belong under `media/`, never `static/`. Production uploads use Vercel Blob instead:

- Page banners: `media/banners/`
- Projects: `media/projects/`
- Project galleries: `media/projects/gallery/`
- Team portraits: `media/team/`
- Events: `media/events/`

The website accepts JPG, PNG, and WebP uploads up to 5 MB by default. An uploaded page banner, project cover, or team portrait automatically overrides its static fallback.

## Image safety checklist

Before publishing, confirm that the hub has permission to use the image, every identifiable person has appropriate consent, alt text is accurate, and no private information is visible. Avoid presenting a temporary or illustrative image as a real TIIH activity.
