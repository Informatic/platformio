"""
    Build script for Ardunet Framework (based on Wiring).
"""

from os import listdir, walk
from os.path import isfile, join

from SCons.Script import DefaultEnvironment, Return

env = DefaultEnvironment()

#
# Determine framework directory
#

PLATFORMFW_DIR = join("$PIOPACKAGES_DIR",
                      "framework-ardunet")

env.Replace(PLATFORMFW_DIR=PLATFORMFW_DIR)

#
# Base
#

env.Prepend(
    CPPPATH=[
        join("$BUILD_DIR", "FrameworkArdunet")
    ]
)

#
# Target: Build Core Library
#


libs = []

envsafe = env.Clone()
envsafe.Prepend(
    CPPPATH=[
        join("$PLATFORMFW_DIR", "src", "include"),
        join("$PLATFORMFW_DIR", "include", "espressif")
    ]
)

libs.append(envsafe.BuildLibrary(
    join("$BUILD_DIR", "FrameworkArdunet"),
    join("$PLATFORMFW_DIR", "src")
))

Return("libs")
