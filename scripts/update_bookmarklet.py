#!/usr/bin/env python3
"""
Update Bookmarklet Script

This script reads the source JavaScript file and updates the bookmarklet in the HTML file
using a template-based approach. It's designed to be used as a pre-commit hook.

Features:
- Idempotence: The script will only update the HTML if the bookmarklet content needs to change
- Fast skip: The script will check if the source file is newer than the target file
- Template-based: Uses Jinja2 templates to cleanly separate content from presentation
- Proper minification: Uses terser for reliable JavaScript minification
"""

import hashlib
import os
import subprocess
import sys
import tempfile
import urllib.parse

from jinja2 import Template


def minify_js_with_terser(js_code):
    """
    Minify JavaScript code using terser.
    Requires terser to be installed globally (npm install -g terser)
    """
    # Create a temporary file for the input
    with tempfile.NamedTemporaryFile(suffix=".js", mode="w+", delete=False) as temp_input:
        temp_input.write(js_code)
        temp_input_path = temp_input.name

    try:
        # Run terser to minify the code
        result = subprocess.run(
            [
                "terser",
                temp_input_path,
                "--compress",
                "--mangle",
                "--format",
                "semicolons=false",
            ],
            capture_output=True,
            text=True,
            check=True,
        )
        minified_js = result.stdout.strip()
        # URL-encode the minified JavaScript
        encoded_js = urllib.parse.quote(minified_js)
        return encoded_js
    except subprocess.CalledProcessError as e:
        print(f"Error running terser: {e}")
        print(f"Stderr: {e.stderr}")
        sys.exit(1)  # Exit if terser fails
    except FileNotFoundError:
        print("terser not found. Please install terser: npm install -g terser")
        sys.exit(1)  # Exit if terser is not installed
    finally:
        # Clean up the temporary file
        if os.path.exists(temp_input_path):
            os.unlink(temp_input_path)


def get_file_hash(file_path):
    """Get the hash of a file's contents."""
    with open(file_path, "rb") as f:
        return hashlib.md5(f.read()).hexdigest()


def main():
    # Paths
    src_path = "src/readmoo-readdict-helper.js"
    html_path = "index.html"
    template_path = "templates/index.html"

    # Check if source files exist
    for path in [src_path, template_path]:
        if not os.path.exists(path):
            print(f"Error: Required file {path} not found!")
            sys.exit(1)

    # Fast skip: Check if everything is up to date
    if os.path.exists(html_path):
        # Get the timestamps of all the relevant files
        src_mtime = os.path.getmtime(src_path)
        template_mtime = os.path.getmtime(template_path)
        html_mtime = os.path.getmtime(html_path)

        # If both source files are older than the HTML file, we can skip
        if max(src_mtime, template_mtime) < html_mtime:
            print(f"HTML file {html_path} is up to date. No changes needed.")
            return 0

    # Read the JavaScript file
    with open(src_path, "r", encoding="utf-8") as f:
        js_code = f.read()

    # Minify the JavaScript for the bookmarklet using terser
    minified_js = minify_js_with_terser(js_code)

    # Read the template file
    with open(template_path, "r", encoding="utf-8") as f:
        template_content = f.read()

    # Create the template object
    template = Template(template_content)

    # Render the template with the bookmarklet code and source code
    rendered_html = template.render(BOOKMARKLET_CODE=minified_js, SOURCE_CODE=js_code)

    # Check if the output file exists and if it's different from what we'd generate
    if os.path.exists(html_path):
        with open(html_path, "r", encoding="utf-8") as f:
            current_html = f.read()

        if current_html == rendered_html:
            print(f"HTML file {html_path} content is already up to date. No changes needed.")
            return 0

    # Write the rendered HTML to the output file
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(rendered_html)

    print(
        f"Bookmarklet updated successfully in {html_path} from template {template_path} and source {src_path}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
