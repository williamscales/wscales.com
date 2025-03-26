import os
import shutil

PROJECT_ROOT = os.path.realpath(os.path.join(os.path.dirname(__file__), ".."))
BUILD_ROOT = os.path.join(PROJECT_ROOT, "build")
LAYOUT_ROOT = os.path.join(PROJECT_ROOT, "layouts")
PAGE_ROOT = os.path.join(PROJECT_ROOT, "pages")
STATIC_ROOT = os.path.join(PROJECT_ROOT, "static")


def check_build_root():
    """Delete the build root and create a new one."""
    if os.path.exists(BUILD_ROOT):
        print("💥 Deleting existing build root...")
        shutil.rmtree(BUILD_ROOT)

    os.makedirs(BUILD_ROOT)
    print(f"📁 Build root created at {BUILD_ROOT}")


def get_layout(layout_file: str = "default.html") -> str:
    """Get the layout content from a file."""
    layout_path = os.path.join(LAYOUT_ROOT, layout_file)
    print(f"🖼️ Got layout from {layout_path}")

    with open(layout_path, "r") as file:
        return file.read()


def get_pages() -> list[str]:
    """Find all pages in the pages directory."""
    return os.listdir(PAGE_ROOT)


def get_page(page_path: str) -> tuple[str, str]:
    """Get the page content from a file."""
    with open(os.path.join(PAGE_ROOT, page_path), "r") as file:
        page_content = file.read()
        page_title = page_content.split("\n")[0]
        page_content = "\n".join(page_content.split("\n")[1:])
        return page_content, page_title


def render_page(page_path: str, layout: str) -> str:
    """Render a page from a layout and a page."""
    page_content, page_title = get_page(page_path)

    return layout.replace("{{page_content}}", page_content).replace(
        "{{page_title}}", page_title
    )


def render_pages(pages: list[str], layout: str):
    """Render all pages and save them to the build root."""
    print("🖌️ Rendering pages...")
    for page_path in pages:
        page_name = page_path.replace(".html", "")

        if page_name == "index":
            output_dir = BUILD_ROOT
        else:
            output_dir = os.path.join(BUILD_ROOT, page_name)
        output_path = os.path.join(output_dir, "index.html")
        os.makedirs(output_dir, exist_ok=True)

        with open(output_path, "w") as file:
            file.write(render_page(page_path, layout))

        print(f"🖌️ {os.path.join(PAGE_ROOT, page_path)} → {output_path}")


def copy_static():
    """Copy all files in the static directory to the build root."""
    print("➡️ Copying static files...")
    for item in os.listdir(STATIC_ROOT):
        source_path = os.path.join(STATIC_ROOT, item)
        destination_path = os.path.join(BUILD_ROOT, item)

        if os.path.isfile(source_path):
            shutil.copy2(source_path, destination_path)
        elif os.path.isdir(source_path):
            shutil.copytree(source_path, destination_path, dirs_exist_ok=True)

        print(f"➡️ {source_path} → {destination_path}")


def build():
    """Build the website."""
    print("🏗️ Building...")
    check_build_root()
    layout = get_layout()
    pages = get_pages()
    render_pages(pages, layout)
    copy_static()
    print("🏗️ Build complete")


if __name__ == "__main__":
    build()
