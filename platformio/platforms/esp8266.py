from platformio.platforms.base import BasePlatform
from os.path import join, dirname, realpath

class Esp8266Platform(BasePlatform):
    """
        An embedded platform for Espressif ESP8266 (with Ardunet Framework)
    """

    PACKAGES = {

        "toolchain-esp8266": {
            "alias": "toolchain",
            "default": True
        },

        "tool-esptoolpy": {
            "alias": "uploader",
            "default": True
        },

        "framework-ardunet": {
            "default": True
        }
    }

