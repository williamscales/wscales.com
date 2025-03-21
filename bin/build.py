import os
import shutil

BUILD_ROOT = "build"
LAYOUT_ROOT = "layouts"
PAGE_ROOT = "pages"
STATIC_ROOT = "static"


def check_build_root() -> None:
    """Delete the build root and create a new one."""
    if os.path.exists(BUILD_ROOT):
        shutil.rmtree(BUILD_ROOT)
    os.makedirs(BUILD_ROOT)


def get_layout(layout_path: str = "default.html") -> str:
    """Get the layout content from a file."""
    with open(os.path.join(LAYOUT_ROOT, layout_path), "r") as f:
        return f.read()


def get_pages() -> list[str]:
    """Find all pages in the pages directory."""
    return os.listdir(PAGE_ROOT)


def get_page(page_path: str) -> tuple[str, str]:
    """Get the page content from a file."""
    with open(os.path.join(PAGE_ROOT, page_path), "r") as f:
        page_content = f.read()
        page_title = page_content.split("\n")[0]
        page_content = "\n".join(page_content.split("\n")[1:])
        return page_content, page_title


def render_page(page_path: str, layout: str) -> str:
    """Render a page from a layout and a page."""
    page_content, page_title = get_page(page_path)
    return layout.replace("{{page_content}}", page_content).replace(
        "{{page_title}}", page_title
    )


def render_pages(pages: list[str], layout: str) -> None:
    """Render all pages and save them to the build root."""
    for page_path in pages:
        page_name = page_path.replace(".html", "")

        if page_name == "index":
            output_dir = BUILD_ROOT
        else:
            output_dir = os.path.join(BUILD_ROOT, page_name)
        output_path = os.path.join(output_dir, "index.html")

        print(output_path)

        os.makedirs(output_dir, exist_ok=True)

        with open(output_path, "w") as f:
            f.write(render_page(page_path, layout))


def copy_static() -> None:
    """Copy all files in the static directory to the build root."""
    for item in os.listdir(STATIC_ROOT):
        source_path = os.path.join(STATIC_ROOT, item)
        destination_path = os.path.join(BUILD_ROOT, item)

        print(destination_path)

        if os.path.isfile(source_path):
            shutil.copy2(source_path, destination_path)
        elif os.path.isdir(source_path):
            shutil.copytree(source_path, destination_path, dirs_exist_ok=True)


def build() -> None:
    """Build the website."""
    check_build_root()
    layout = get_layout()
    pages = get_pages()
    render_pages(pages, layout)
    copy_static()


if __name__ == "__main__":
    build()
