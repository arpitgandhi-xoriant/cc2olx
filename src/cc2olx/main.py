import logging
import os.path

from cc2olx.settings import collect_settings
from cc2olx import filesystem
from cc2olx import models
from cc2olx.models import Cartridge
from cc2olx import olx


if __name__ == '__main__':
    settings = collect_settings()
    logging.basicConfig(**settings['logging_config'])
    logger = logging.getLogger()
    workspace = settings['workspace']
    filesystem.create_directory(workspace)
    for input_file in settings['input_files']:
        print("Converting", input_file)
        cartridge = Cartridge(input_file)
        data = cartridge.load_manifest_extracted()
        cartridge.normalize()
        # print()
        # print("=" * 100)
        # import json; print(json.dumps(cartridge.normalized, indent=4))
        xml = olx.OlxExport(cartridge).xml()
        olx_filename = os.path.join(workspace, cartridge.directory + "-course.xml")
        with open(olx_filename, "w") as olxfile:
            olxfile.write(xml)
        tgz_filename = os.path.join(workspace, cartridge.directory + "-onefile.tar.gz")
        olx.onefile_tar_gz(tgz_filename, xml.encode("utf8"), "course.xml")
