"""Prepare generated, non-institutional website photography and neutral placeholders."""

import argparse
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps

ROOT = Path(__file__).resolve().parent.parent
STATIC = ROOT / "static" / "images"


def save_crop(source, destination, size, centering=(0.5, 0.5), quality=88):
    image = Image.open(source).convert("RGB")
    image = ImageOps.fit(image, size, method=Image.Resampling.LANCZOS, centering=centering)
    destination.parent.mkdir(parents=True, exist_ok=True)
    image.save(destination, "JPEG", quality=quality, optimize=True, progressive=True)


def font(size, bold=False):
    choices = [
        Path("C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf"),
        Path("C:/Windows/Fonts/segoeuib.ttf" if bold else "C:/Windows/Fonts/segoeui.ttf"),
    ]
    for choice in choices:
        if choice.exists():
            return ImageFont.truetype(str(choice), size)
    return ImageFont.load_default()


def neutral_portrait(destination, label):
    image = Image.new("RGB", (800, 1000), "#e7f0e9")
    draw = ImageDraw.Draw(image)
    for y in range(image.height):
        ratio = y / image.height
        colour = (int(231 - 48 * ratio), int(240 - 28 * ratio), int(233 - 42 * ratio))
        draw.line((0, y, image.width, y), fill=colour)
    draw.ellipse((270, 210, 530, 470), fill="#739382")
    draw.rounded_rectangle((150, 500, 650, 950), radius=170, fill="#739382")
    draw.rounded_rectangle((115, 835, 685, 925), radius=18, fill="#123326")
    text_box = draw.textbbox((0, 0), label, font=font(28, True))
    draw.text(((800 - (text_box[2] - text_box[0])) / 2, 865), label, fill="white", font=font(28, True))
    destination.parent.mkdir(parents=True, exist_ok=True)
    image.save(destination, "JPEG", quality=88, optimize=True, progressive=True)


def logo_placeholder(destination, title, subtitle):
    image = Image.new("RGB", (600, 600), "#ffffff")
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle((26, 26, 574, 574), radius=85, fill="#087832")
    draw.ellipse((120, 105, 480, 465), outline="#8ce6a5", width=18)
    title_font = font(105 if len(title) <= 4 else 68, True)
    box = draw.textbbox((0, 0), title, font=title_font)
    draw.text(((600 - (box[2] - box[0])) / 2, 215), title, fill="white", font=title_font)
    sub_font = font(19, True)
    sub = subtitle.upper()
    sub_box = draw.textbbox((0, 0), sub, font=sub_font)
    draw.text(((600 - (sub_box[2] - sub_box[0])) / 2, 510), sub, fill="white", font=sub_font)
    destination.parent.mkdir(parents=True, exist_ok=True)
    image.save(destination, "PNG", optimize=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--hero", required=True)
    parser.add_argument("--about", required=True)
    parser.add_argument("--services", required=True)
    parser.add_argument("--projects", required=True)
    parser.add_argument("--team", required=True)
    parser.add_argument("--contact", required=True)
    args = parser.parse_args()

    save_crop(args.hero, STATIC / "banners/home_hero.jpg", (1920, 900), (0.55, 0.5))
    save_crop(args.about, STATIC / "banners/about_banner.jpg", (1920, 650), (0.56, 0.5))
    save_crop(args.services, STATIC / "banners/services_banner.jpg", (1920, 650), (0.58, 0.5))
    save_crop(args.projects, STATIC / "banners/projects_banner.jpg", (1920, 650), (0.55, 0.5))
    save_crop(args.team, STATIC / "banners/team_banner.jpg", (1920, 650), (0.5, 0.5))
    save_crop(args.contact, STATIC / "banners/contact_banner.jpg", (1920, 650), (0.5, 0.5))
    save_crop(args.services, STATIC / "home/about_hub.jpg", (1400, 1050), (0.7, 0.5))
    save_crop(args.projects, STATIC / "placeholders/project_default.jpg", (1200, 800), (0.72, 0.5))
    neutral_portrait(STATIC / "team/chair_photo.jpg", "CHAIR'S PHOTOGRAPH")
    neutral_portrait(STATIC / "placeholders/team_member_default.jpg", "TEAM PHOTOGRAPH")
    logo_placeholder(STATIC / "branding/ttu_logo.png", "TTU", "Logo placeholder")


if __name__ == "__main__":
    main()
