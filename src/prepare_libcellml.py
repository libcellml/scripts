import subprocess

from common import process_command_result


def main():
    libcellml_info = "https://github.com/cellml/libcellml"
    parts = libcellml_info.split()
    url = parts[0]
    clone_command = ["git", "-c", "advice.detachedHead=false", "clone", "--depth", "1", url]

    if len(parts) > 1:
        tag = parts[1]
        clone_command.extend(["-b", tag])

    result = subprocess.run(clone_command)
    process_command_result(result)

    configure_command = ["cmake", "-S", "libcellml", "-B", "build-libcellml", "-G", "Ninja", "-DBUILD_TYPE=Release"]
    result = subprocess.run(configure_command)
    process_command_result(result)

    build_command = ["ninja"]
    result = subprocess.run(build_command, cwd="build-libcellml")
    process_command_result(result)

    install_libcellml_command = ["pip", "install", "-e", "build-libcellml/src/bindings/python/"]
    result = subprocess.run(install_libcellml_command)
    process_command_result(result)


if __name__ == "__main__":
    main()
