# TIIH website security and administrator access

## Administrator sign-in

The site requires an authenticator-app code after a staff member's password. On the first sign-in after this release, staff are directed to `/mfa/security/` to add an authenticator app. Scan the QR code, confirm one six-digit code, and save the one-time recovery codes somewhere separate from the phone. The admin dashboard remains unavailable until enrollment and verification are complete. The MFA pages offer a **Sign out** button even when enrollment cannot be completed.

Five failed admin password attempts trigger a 15-minute database-backed lockout. Successful and failed login records are visible to authorized administrators through the Axes admin entries. A remembered session lasts at most eight hours; without **Remember me**, it ends when the browser closes. Avoid shared administrator accounts and give each staff member only the permissions needed for their role.

If a device and recovery codes are both lost, verify the staff member's identity through a separate channel before an authorized operator runs django-mfa's `mfa_reset` management command against the **production** database. For a password lockout, wait for the 15-minute expiry or have an authorized operator use Axes' reset command after checking the account. Never send an MFA secret or recovery code in email or chat.

## Production and Preview settings

- Keep `DJANGO_DEBUG=False`, use a unique high-entropy `DJANGO_SECRET_KEY`, and keep `SESSION_COOKIE_SECURE=True`, `CSRF_COOKIE_SECURE=True`, and HTTPS enforcement enabled. The app now refuses to start with debug enabled on Vercel.
- Set `ALLOWED_HOSTS` to the actual production and approved preview hostnames. Set `CSRF_TRUSTED_ORIGINS` to their exact HTTPS origins where practical; avoid broad wildcard trust.
- In Vercel, verify that **Preview uses a different Neon branch/database and different Blob write token/store from Production**. The build applies migrations to whichever `DATABASE_URL_UNPOOLED` or `DATABASE_URL` it receives; code cannot infer whether two secrets point at the same database. Restrict production-only integration credentials to Production in Vercel.
- Keep Neon and Blob credentials out of Git, local screenshots, and issue reports. Database backups also contain readable authenticator-app secrets; limit database access and keep backups encrypted.
- Configure a Vercel Firewall rule for repeated `/admin/login/` POST requests as another layer. Observe the rule in log mode first so legitimate staff are not blocked. Review Axes lockouts and Vercel logs regularly, and set up alerts in the hosting dashboard for unusual login and error spikes. Database logging alone does not send alerts.
- Schedule `python manage.py mfa_prune --quiet` against the production database at least daily to remove expired MFA rate-limit records. It is safe to run after migrations; it does not reset active factors.

## Content and dependencies

Uploaded Vercel Blob images are intentionally public. Upload only approved public images, never identity documents or other private files. When changing a CDN URL, update its `integrity` hash and test the page; a mismatch intentionally blocks the asset. The public Content Security Policy allows only the current CDN, Vercel Blob images, and Google Maps frame.

GitHub runs tests, Django's deployment checks, and `pip-audit` on pushes, pull requests, and weekly. Dependabot checks Python and GitHub Actions dependencies weekly. Investigate any failed security job before deploying. These checks complement, but do not replace, reviewing Vercel, Neon, GitHub, and domain-account MFA and access permissions.
