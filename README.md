# wscales.com

Source code for [wscales.com](https://wscales.com/) static site.

## Overview

Cloudfront serves the static site from an S3 bucket.

### Pages

Pages are fragments of HTML in `pages/`.

Pages have hardcoded metadata in `bin/build.py`, no autodiscovery.

### Layouts

Layouts live in `layouts/` and have a couple fields that are substituted when rendering: `{{page_content}}` and `{{page_title}}`.

```html
<html>
    <head>
        <title>{{page_title}}</title>
    </head>
    <body>
        <header>...</header>
        <main>{{page_content}}</main>
        <footer>...</footer>
    </body>
</html>
```

### Static Files

Static files live in `static/`. Building copies the contents of this directory to the build root.

### Adding a New Page
1. Write the page as a new HTML fragment file in `pages/`.
2. Update `pages` data structure in `bin/build.py` with the HTML fragment path and page metadata.

## Build and Deploy

### Environment Variables

```sh
AWS_ACCESS_KEY_ID
AWS_CLOUDFRONT_DISTRIBUTION
AWS_S3_BUCKET
AWS_SECRET_ACCESS_KEY
```

### Build

```sh
python bin/build.py
```

Output is in `build/` directory.

### Deploy

```sh
sh bin/deploy-s3.sh
sh bin/invalidate-cloudfront.sh
```