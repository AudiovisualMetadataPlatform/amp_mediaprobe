#!/bin/env python3

from amp.package import *
import argparse
import logging
from pathlib import Path
import subprocess
import sys
import tempfile
import shutil

def main():
    parser = argparse.ArgumentParser()    
    parser.add_argument("--debug", default=False, action="store_true", help="Turn on debugging")    
    parser.add_argument("--package", default=False, action="store_true", help="Build package instead of install")
    parser.add_argument("destination", help="Destination for build (should be an AMP_ROOT for non-package)")
    args = parser.parse_args()
    logging.basicConfig(format="%(asctime)s [%(levelname)-8s] (%(filename)s:%(lineno)d)  %(message)s",
                        level=logging.DEBUG if args.debug else logging.INFO)



    # Build the container
    # Just some scripts, nothing to build.

    # Install the container
    destdir = Path(args.destination)
    if args.package:
        # create a temporary directory for the build.
        tempdir = tempfile.TemporaryDirectory()
        destdir = Path(tempdir.name)

    target = destdir / "data/MediaProbe"
    target.mkdir(parents=True, exist_ok=True)    
    logging.info(f"Copying files to {target!s}")
    try: 
        for file in ('media_probe/__init__.py', 
                     'LICENSE',
                     'media_probe_schema.json',
                     'media_probe.py',
                     'README.md'):
            dfile = target / file
            if not dfile.parent.exists():
                dfile.parent.mkdir(parents=True)
            shutil.copyfile(file, dfile)
            shutil.copystat(file, dfile)                     
    except Exception as e:
        logging.error(f"Failed to copy file: {e}")
        exit(1)

    # Package it, if needed
    if args.package:
        try:
            new_package = create_package("mediaprobe", "1.0.0", "data/MediaProbe",
                                         Path(args.destination), target)                                                                                    
            logging.info(f"New package in {new_package}")    
        except Exception as e:
            logging.error(f"Failed to build backage: {e}")
            exit(1)


if __name__ == "__main__":
    main()
