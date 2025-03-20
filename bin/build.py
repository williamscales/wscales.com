import os
import shutil

BUILD_ROOT = "build"
LAYOUT_ROOT = "layouts"
PAGE_ROOT = "pages"
STATIC_ROOT = "static"

pages = {
    "home": {
        "title": "Home",
        "path": "index.html",
    },
    "error": {
        "title": "Error",
        "path": "error.html",
    },
}

layouts = {
    "default": {
        "path": "default.html",
    },
}


def render_page(page, layout):
    """Render a page from a layout and a page."""
    page_path = os.path.join(PAGE_ROOT, page["path"])
    layout_path = os.path.join(LAYOUT_ROOT, layout["path"])
    with open(page_path, "r") as f:
        page_content = f.read()
    with open(layout_path, "r") as f:
        layout_content = f.read()
    return layout_content.replace("{{page_content}}", page_content).replace(
        "{{page_title}}", page["title"]
    )


def check_build_root():
    """Delete the build root and create a new one."""
    if os.path.exists(BUILD_ROOT):
        shutil.rmtree(BUILD_ROOT)
    os.makedirs(BUILD_ROOT)


def copy_static():
    """Copy all files in the static directory to the build root."""
    for item in os.listdir(STATIC_ROOT):
        s = os.path.join(STATIC_ROOT, item)
        d = os.path.join(BUILD_ROOT, item)
        print(d)
        if os.path.isfile(s):
            shutil.copy2(s, d)
        elif os.path.isdir(s):
            shutil.copytree(s, d, dirs_exist_ok=True)


def render_pages():
    """Render all pages and save them to the build root."""
    for _, page in pages.items():
        page_path = os.path.join(BUILD_ROOT, page["path"])
        print(page_path)
        with open(page_path, "w") as f:
            f.write(render_page(page, layouts["default"]))


def build():
    """Build the website."""
    check_build_root()
    render_pages()
    copy_static()


if __name__ == "__main__":
    build()
