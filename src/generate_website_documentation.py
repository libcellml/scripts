import json
import os
import shutil
import subprocess

from packaging.version import Version, parse

from common import process_command_result, determine_libcellml_version


def _cleanup_versions(versions):
    remove_versions = []
    index = 0
    while index < len(versions):
        next_ = index + 1
        v = parse(versions[index])
        v_next = None
        if next_ < len(versions):
            v_next = parse(versions[next_])

        if v_next is None:
            index += 1
        else:
            if v.major == v_next.major and v.minor == v_next.minor:
                remove_versions.append(versions[next_])
                versions.pop(next_)
            else:
                index += 1

    for version in remove_versions:
        shutil.rmtree(f"investigate-documentation/public/generated/{version}")


def _write_versions_file(versions):
    content = f"""// This file is generated do not edit!
// Changes made here will be overwritten when a release is made.
export const getDocumentationVersions = () => {{
  return {versions}
}}
"""
    with open("investigate-documentation/src/js/versions.js", "w") as f:
        f.write(content)


def _write_documentation_availability_file(location):
    directories = next(os.walk(location))[1]
    with open(os.path.join(location, "directories.json"), "w") as f:
        json.dump(directories, f)


def _remove_surplus_html_files(location):
    current_dir = os.path.abspath(os.path.curdir)
    working_dir = os.path.join(current_dir, location)
    os.chdir(working_dir)

    for root, dirs, files in os.walk(".", topdown=False):
        for name in files:
            parts = os.path.splitext(name)
            if len(parts) == 2 and parts[1] == ".html":
                os.remove(os.path.join(root, name))

    os.chdir(current_dir)


def _do_documentation_version_update():
    documentation_versions = os.listdir("investigate-documentation/public/generated/")
    documentation_versions.sort(key=Version)
    documentation_versions.reverse()
    _cleanup_versions(documentation_versions)

    _write_versions_file(documentation_versions)

    for version in documentation_versions:
        _write_documentation_availability_file("investigate-documentation/public/generated/" + version)


def main():
    here = os.path.abspath(os.path.dirname(__file__))
    # The first section prepares a libCellML build.
    result = subprocess.run(["python", os.path.join(here, "prepare_libcellml.py")])
    process_command_result(result)

    libcellml_version = determine_libcellml_version()
    print(f"libcellml version: {libcellml_version}")

    # This second section deals with building the API documentation.
    result = subprocess.run(["python", os.path.join(here, "generate_api_documentation.py")])
    process_command_result(result)

    src = "build-libcellml/docs/doxygen-xml/"
    dst = f"investigate-documentation/public/generated/v{libcellml_version}/api"
    if os.path.isdir(dst):
        shutil.rmtree(dst)

    shutil.copytree(src, dst)

    # This third section deals with building the API documentation.
    result = subprocess.run(["python", os.path.join(here, "generate_developer_documentation.py")])
    process_command_result(result)

    # Copy over user guide documentation.
    src = "build-libcellml/docs/developer_docs/"
    # Make sure the destination is empty (surely only useful when testing this script).
    dst = f"investigate-documentation/public/generated/v{libcellml_version}/developer"
    if os.path.isdir(dst):
        shutil.rmtree(dst)

    shutil.copytree(src, dst)

    # Remove all .html files that are no longer required.
    _remove_surplus_html_files(dst)

    # This forth section deals with running the end-to-end testing.
    result = subprocess.run(["python", os.path.join(here, "run_end_to_end_testing.py")])

    # This fifth section deals with building the user guide documentation.
    if result.returncode == 0:
        result = subprocess.run(["python", os.path.join(here, "generate_user_guide_documentation.py")])
        process_command_result(result)

        # Copy over user guide documentation.
        src = "userguides/build/"
        # Make sure the destination is empty (surely only useful when testing this script).
        dst = f"investigate-documentation/public/generated/v{libcellml_version}/userguides"
        if os.path.isdir(dst):
            shutil.rmtree(dst)

        shutil.copytree(src, dst)

        # Remove all .html files that are no longer required.
        _remove_surplus_html_files(dst)

    # Lastly we update the available versions directories and information.
    _do_documentation_version_update()


if __name__ == "__main__":
    main()
