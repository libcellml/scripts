import os
import subprocess

from common import process_command_result, update_xml_figure_numbering


def main():
    base_documentation_command = ['sphinx-build', '-b', '-c', '_build', '-d', '_doctrees',
                                  '../../libcellml/docs', 'developer_docs']
    build_html_documentation_command = base_documentation_command[:]
    build_html_documentation_command.insert(2, 'html')
    result = subprocess.run(build_html_documentation_command, cwd="build-libcellml/docs")
    process_command_result(result)

    build_xml_documentation_command = base_documentation_command[:]
    build_xml_documentation_command.insert(2, 'xml')
    result = subprocess.run(build_xml_documentation_command, cwd="build-libcellml/docs")
    process_command_result(result)

    # Apply numfig manually because Sphinx only supports numfig for HTML and Latex.
    update_xml_figure_numbering(os.path.join('build-libcellml', 'docs', 'developer_docs'))


if __name__ == "__main__":
    main()
