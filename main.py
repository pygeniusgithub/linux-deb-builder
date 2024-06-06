import subprocess
import os
import argparse

def download_packages_from_metapackage(metapackages):
    for metapackage in metapackages:
        try:
            subprocess.run(["apt", "download", metapackage], check=True)
            print(f"Successfully downloaded packages from '{metapackage}'.")
        except subprocess.CalledProcessError as e:
            print(f"Failed to download packages from '{metapackage}': {e}")

def copy_downloaded_packages_to_current_directory():
    try:
        subprocess.run(["cp", "-r", "/var/cache/apt/archives/.", "."], check=True)
        print("Copied downloaded packages to current directory.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to copy downloaded packages: {e}")

def unpack_and_resolve_dependencies(target_directory):
    os.makedirs(target_directory, exist_ok=True)
    deb_files = [f for f in os.listdir('.') if f.endswith('.deb')]

    for deb_file in deb_files:
        try:
            subprocess.run(["dpkg-deb", "-x", deb_file, target_directory], check=True)
            print(f"Unpacked '{deb_file}' to '{target_directory}'.")
        except subprocess.CalledProcessError as e:
            print(f"Failed to unpack '{deb_file}': {e}")

    # Resolving dependencies (this is a simplified approach)
    try:
        subprocess.run(["apt-get", "install", "-f"], check=True)
        print("Resolved dependencies.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to resolve dependencies: {e}")

def main():
    parser = argparse.ArgumentParser(description="Download, copy, unpack, and resolve dependencies for metapackages.")
    parser.add_argument("mode", choices=['1', '2'], help="1: Download and copy mode, 2: Full package unpacker mode.")
    parser.add_argument("target_directory", help="The directory where packages will be unpacked (only used in mode 2).")
    parser.add_argument("--metapackages", nargs='+', default=["ubuntu-standard", "ubuntu-minimal", "linux-base"], help="List of metapackages to download.")
    
    args = parser.parse_args()

    download_packages_from_metapackage(args.metapackages)
    copy_downloaded_packages_to_current_directory()

    if args.mode == '2':
        unpack_and_resolve_dependencies(args.target_directory)

if __name__ == "__main__":
    main()
