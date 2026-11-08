# FavourBrook

A Django store for Favourbrook — luxury menswear and womenswear, London.
120 products across 12 collections, with basket, checkout, contact and newsletter.

## Open the site

- Desktop icon **Favourbrook** (or `open-favourbrook.bat`) — starts the server if needed and opens the browser.
- Desktop icon **Favourbrook Admin** — opens the admin.
- The server also starts automatically at sign-in (Startup shortcut).

Addresses (this computer only, not a public website):

- Site: http://favourbook.org/ (also http://127.0.0.6/)
- Admin: http://favourbook.org/admin/ — username `admin`, password `FavourBrook@2026`

The name `favourbook.org` is mapped to this machine in the Windows hosts file
(`127.0.0.6`). Remove those two lines to reach the real site again.

## Run manually

```
python manage.py runserver 127.0.0.6:80
```

Requires Python 3.13 with `Django==6.1.2` and `Pillow==12.3.0` (see `requirements.txt`).

## What is in the box

- `core/` — models, views, admin and URLs for the whole store.
- `templates/core/` — base layout, home, collection, product, basket, checkout, contact, pages.
- `static/` — site CSS and JS (menu, search, basket steppers, scroll reveals).
- `media/` — product and home imagery, logos.
- `catalog.json` — the 120 products (name, price, description, collections, image).
- `collections.json` — the 12 collections with their intro copy and nav order.
- `db.sqlite3` — the seeded database, including the admin user.

## Editing content

Everything on the home page (hero panels, product rows, editorial cards, feature
block, wide hero, about band, service icons) and every footer page is editable in
the admin. Products, prices, collections and stock status are editable there too.

## SEO

Each page sets its own title, meta description, canonical and Open Graph tags.
Product pages add Product schema; the layout adds ClothingStore schema.
`/sitemap.xml` and `/robots.txt` are generated from the live catalogue.