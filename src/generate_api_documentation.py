import subprocess

from common import process_command_result


def main():
    build_website_docs_documentation_command = ["ninja", "website_docs"]
    result = subprocess.run(build_website_docs_documentation_command, cwd="build-libcellml")
    process_command_result(result)


if __name__ == "__main__":
    main()
