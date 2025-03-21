![logo](/static/favicon.svg)

# wscales.com

Source code for [wscales.com](https://wscales.com/) static site.

## Overview

Cloudfront serves the static site from an S3 bucket.

### Pages

Pages are HTML files in `pages/`. They are fragments that will be inserted inside a `<main>` tag in the final HTML.

The first line of the file is taken as the page title and stripped before rendering the page.

The output path will be the filename minus '.html'. For example, `pages/about.html` → `build/about/index.html`

### Layouts

Layouts live in `layouts/`. The default is `layouts/default.html`. 

A couple template tags are substituted when rendering: `{{page_content}}` and `{{page_title}}`.

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

## Build and Deploy

### Build

```sh
python bin/build.py
```

Output is in `build/` directory.

### Development

```sh
python -m http.server -d build 8000
```

Serves on [localhost:8000](http://localhost:8000).

### Deploy

Using GitHub Actions: `.github/workflows/deploy.yml`.

#### Environment Variables

```sh
AWS_ACCESS_KEY_ID
AWS_CLOUDFRONT_DISTRIBUTION
AWS_S3_BUCKET
AWS_SECRET_ACCESS_KEY
```

#### Scripts

```sh
sh bin/deploy-s3.sh
sh bin/invalidate-cloudfront.sh
```
