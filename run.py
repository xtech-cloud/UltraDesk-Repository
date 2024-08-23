import os
import json
import datetime
import hashlib
import logging
import colorlog
from flask import Flask, send_from_directory

app = Flask(__name__)
volume_root = "./volume"


def buildLogger(_logger):
    log_colors_config = {
        "DEBUG": "white",
        "INFO": "green",
        "WARING": "yellow",
        "ERROR": "red",
        "CRITICAL": "bold_red",
    }
    handler = logging.StreamHandler()
    handler.setFormatter(
        colorlog.ColoredFormatter(
            fmt="%(log_color)s%(asctime)s [%(levelname)s] - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
            log_colors=log_colors_config,
        )
    )
    _logger.addHandler(handler)
    _logger.setLevel(logging.DEBUG)
    handler.close()


def encrypt(_file):
    with open(_file, "rb") as f:
        hash = hashlib.new("sha256")
        for chunk in iter(lambda: f.read(2**20), b""):
            hash.update(chunk)
        return hash.hexdigest()


def generateApplication(_volume_root, _os):
    applications_path = os.path.join(_volume_root, "applications").replace("\\", "/")
    os_path = os.path.join(applications_path, _os).replace("\\", "/")
    source_path = os.path.join(_volume_root, "source_{}.json".format(_os)).replace(
        "\\", "/"
    )
    if not os.path.exists(os_path):
        os.makedirs(os_path)
    if os.path.exists(source_path):
        log.info("found {}".format(source_path))
        return

    log.info("generate {}".format(source_path))

    manifest = {}
    manifest["version"] = datetime.datetime.utcnow().strftime("%Y%m%d%H%M")
    manifest["applications"] = []
    for app_name in os.listdir(os_path):
        app_path = os.path.join(os_path, app_name).replace("\\", "/")
        meta_path = os.path.join(app_path, "meta.json")
        if not os.path.exists(meta_path):
            continue

        application = {}
        application["name"] = app_name
        application["packages"] = []
        for pkg_name in os.listdir(app_path):
            if not pkg_name.endswith(".7z"):
                continue
            log.debug("add " + pkg_name + "...")
            package = {}
            package["version"] = pkg_name.split("_")[-1].replace(".7z", "")
            package["path"] = os.path.join(app_path, pkg_name).replace("\\", "/")
            package["sha256"] = encrypt(package["path"])
            application["packages"].append(package)

        manifest["applications"].append(application)

    with open(source_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False)


@app.route("/<path:p>")
def download(p):
    log.info("download {}/{}".format(volume_root, p))
    return send_from_directory(volume_root, p, mimetype="application/octet-stream")


"""
main
"""
if __name__ == "__main__":
    log = logging.getLogger("UltraDesk.Repository")
    buildLogger(log)
    log.info("UltraDesk Repository run ...")
    log.info("---------------------------------------------------------")

    if not os.path.exists(volume_root):
        os.makedirs(volume_root)

    generateApplication(volume_root, "windows")

    app.run(host="0.0.0.0", port=80)
