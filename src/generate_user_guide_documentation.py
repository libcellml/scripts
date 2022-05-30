import os
import subprocess

from common import process_command_result, update_xml_figure_numbering


def main():
    user_guides_info = "https://github.com/libcellml/userguides"
    parts = user_guides_info.split()
    url = parts[0]
    clone_command = ["git", "-c", "advice.detachedHead=false", "clone", "--depth", "1", url]

    if len(parts) > 1:
        tag = parts[1]
        clone_command.extend(["-b", tag])

    result = subprocess.run(clone_command)
    process_command_result(result)

    build_html_documentation_command = ['sphinx-build', '.', 'build', '-b', 'html']
    result = subprocess.run(build_html_documentation_command, cwd="userguides")
    process_command_result(result)

    build_xml_documentation_command = ['sphinx-build', '.', 'build', '-b', 'xml']
    result = subprocess.run(build_xml_documentation_command, cwd="userguides")
    process_command_result(result)

    # Apply numfig manually because Sphinx only supports numfig for HTML and Latex.
    update_xml_figure_numbering(os.path.join('userguides', 'build'))


if __name__ == "__main__":
    main()
