#!/usr/bin/env python3
import os
import platform
import subprocess
import sys
from tempfile import NamedTemporaryFile

import requests
import pandas as pd
import semver
from github import Github
from tqdm import tqdm


SRC_REPO = "cgohlke/geospatial-wheels"


def get_python_version():
    return f"{sys.version_info.major}.{sys.version_info.minor}"

def is_windows():
    return platform.system().lower() == "windows"

def get_architecture():
    machine = platform.machine().lower()
    if is_windows():
        if machine == "amd64" or machine == "x86_64":
            return "win_amd64"
        elif machine == "x86" or machine == "i386":
            return "win32"
        elif machine == "arm64" or machine == "aarch64":
            return "win_arm64"
    return machine

def get_wheel_url(python_version, architecture):
    g = Github()
    repo = g.get_repo(SRC_REPO)
    releases = repo.get_releases()

    wheels = list()

    for release in releases:
        tag = release.tag_name
        assets = release.assets
        for asset in assets:
            whl_url = asset.browser_download_url

            binary_name = asset.name[:-4]  # remove ".whl"
            binary_name_elms = binary_name.split("-")
            distribution, version, python_tag, abi_tag, platform = binary_name_elms
            try:
                version = semver.Version.parse(version)
            except ValueError:
                v = version.split(".")
                version = semver.Version(
                    major=int(v[0]),
                    minor=int(v[1]),
                    patch=int(v[2]),
                    prerelease=None,
                    build=v[3],
                )

            wheels.append(
                {
                    "distribution": distribution,
                    "version_major": version.major,
                    "version_minor": version.minor,
                    "version_patch": version.patch,
                    "version_build": version.build,
                    "python_tag": python_tag,
                    "abi_tag": abi_tag,
                    "platform": platform,
                    "whl_url": whl_url,
                }
            )

    all_assets = pd.DataFrame().from_records(wheels).convert_dtypes()

    latest_assets = (
        all_assets.query("distribution == 'gdal'")
        .sort_values(
            by=["version_major", "version_minor", "version_patch", "version_build"],
            ascending=False,
        )
        .drop_duplicates(
            subset=["distribution", "python_tag", "abi_tag", "platform"], keep="first"
        )
        .reset_index(drop=True)
    )

    lookup = dict()
    for asset in latest_assets.to_dict("records"):
        if asset["platform"] not in lookup:
            lookup[asset["platform"]] = dict()

        if asset["abi_tag"] not in lookup[asset["platform"]]:
            lookup[asset["platform"]][asset["abi_tag"]] = dict()

        if asset["python_tag"] not in lookup[asset["platform"]][asset["abi_tag"]]:
            lookup[asset["platform"]][asset["abi_tag"]][asset["python_tag"]] = dict()

        if asset["version_build"]:
            version_build = f"+{asset["version_build"]}"
        else:
            version_build = ""

        lookup[asset["platform"]][asset["abi_tag"]][asset["python_tag"]][
            asset["distribution"]
        ] = {
            "version": f"{asset["version_major"]}.{asset["version_minor"]}.{asset["version_patch"]}{version_build}",
            "url": asset["whl_url"],
        }

    return lookup[architecture][python_version][python_version]["gdal"]["url"]


def main():
    if is_windows():
        python_version = get_python_version()
        architecture = get_architecture()
        wheel_url = get_wheel_url(f"cp{python_version.replace(".", "")}", architecture)
        
        if not wheel_url:
            print(f"No GDAL wheel found for Python {python_version} on {architecture}")
            sys.exit(1)
        
        print(f"Downloading GDAL wheel for Python {python_version} on {architecture}")
        
        # Extract filename from URL
        wheel_filename = wheel_url.split('/')[-1]
        
        # Download with progress bar
        response = requests.get(wheel_url, stream=True)
        total_size = int(response.headers.get('content-length', 0))
        
        # Use tempfile.gettempdir() to get temp directory and join with original filename
        wheel_path = os.path.join(os.path.dirname(NamedTemporaryFile().name), wheel_filename)
        
        with open(wheel_path, 'wb') as f:
            with tqdm(total=total_size, unit='iB', unit_scale=True) as pbar:
                for data in response.iter_content(chunk_size=1024):
                    size = f.write(data)
                    pbar.update(size)

        # install dependencies
        subprocess.check_call([sys.executable, "-m", "pip", "install", wheel_path])
        subprocess.check_call([sys.executable, "-m", "pip", "install", "gdal"])

        # Clean up
        os.unlink(wheel_path)

    else:
        # On Unix systems, just use pip but install to user site (but some system require --break-system-packages which is not used here)
        subprocess.check_call([sys.executable, "-m", "pip", "install", "GDAL", "--user"])

if __name__ == "__main__":
    main()
