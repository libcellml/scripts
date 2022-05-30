import os
import shutil
import subprocess

from common import process_command_result


def main():
    user_guides_info = "https://github.com/libcellml/end-to-end-testing"
    parts = user_guides_info.split()
    url = parts[0]
    clone_command = ["git", "-c", "advice.detachedHead=false", "clone", "--depth", "1", url]

    if len(parts) > 1:
        tag = parts[1]
        clone_command.extend(["-b", tag])

    result = subprocess.run(clone_command)
    process_command_result(result)

    # Configure end-to-end testing.
    end_to_end_build_dir = "build-end-to-end-testing"
    if os.path.exists(end_to_end_build_dir):
        shutil.rmtree(end_to_end_build_dir)

    libcellml_build_dir = os.path.join(os.path.abspath('.'), "build-libcellml")
    configure_command = ["cmake", f"-DlibCellML_DIR={libcellml_build_dir}", "-B", end_to_end_build_dir, "-S",
                         "end-to-end-testing/"]
    result = subprocess.run(configure_command)
    process_command_result(result)

    build_command = ["make"]
    result = subprocess.run(build_command, cwd=end_to_end_build_dir)
    process_command_result(result)

    test_command = ["ctest"]
    result = subprocess.run(test_command, cwd=end_to_end_build_dir)
    process_command_result(result)


if __name__ == "__main__":
    main()
