"""
    Build script for test.py
    test-builder.py
"""

from os.path import join
from SCons.Script import AlwaysBuild, Builder, Default, DefaultEnvironment

env = DefaultEnvironment()

# A full list with the available variables
# http://www.scons.org/doc/production/HTML/scons-user.html#app-variables
env.Replace(
    AR="xtensa-lx106-elf-ar",
    AS="xtensa-lx106-elf-gcc",
    # CC="xtensa-lx106-elf-gcc",
    CC="xtensa-lx106-elf-g++", # FIXME
    CXX="xtensa-lx106-elf-g++",
    OBJCOPY="xtensa-lx106-elf-objcopy",
    RANLIB="xtensa-lx106-elf-ranlib",
    FW_TOOL="esptool",

    ARFLAGS=["cru"],

    ASFLAGS=[],
    CCFLAGS=["-Os", "-g", "-O2", "-Wpointer-arith", "-Wundef", "-Werror",
             "-Wl,-EL", "-fno-inline-functions", "-nostdlib", "-mlongcalls",
             "-mtext-section-literals"],
    CXXFLAGS=["-Os", "-g", "-O2", "-Wpointer-arith", "-Wundef", "-Werror",
              "-Wl,-EL", "-fno-inline-functions", "-nostdlib", "-mlongcalls",
              "-mtext-section-literals", "-fno-rtti", "-fno-exceptions"],
    LINKFLAGS=["-L$SDK_BASE/lib", "-nostdlib", "-Wl,--no-check-sections", "-u call_user_start",
               "-Wl,-static", "-Wl,--allow-multiple-definition"],

    LDSCRIPT_PATH="eagle.app.v6.ld",
    CPPDEFINES=["__ets__", "ICACHE_FLASH"],

    SDK_BASE='$PIOPACKAGES_DIR/toolchain-esp8266/xtensa-lx106-elf/sysroot/usr',
    LIBPATH=['$SDK_BASE/lib'],
    CPPPATH=[
        '$SDK_BASE/include',
        '$SDK_BASE/include/espressif',
        '$SDK_BASE/include/freertos',
        '$SDK_BASE/include/json',
        '$SDK_BASE/include/lwip',
        '$SDK_BASE/include/lwip/ipv4',
        '$SDK_BASE/include/lwip/ipv6',
        '$SDK_BASE/include/ssl',
        '$SDK_BASE/include/udhcp',
        '$SDK_BASE/include/extra_include',
        ],

    UPLOADER=join("$PIOPACKAGES_DIR", "tool-esptoolpy", "esptool.py"),
    #UPLOADPORT="/dev/serial/by-id/usb-Silicon_Labs_CP2102_USB_to_UART_Bridge_Controller_0001-if00-port0",
    UPLOADCMD=[
        "$UPLOADER --port $UPLOAD_PORT write_flash 0x00000 $BUILD_DIR/0x00000.bin",
        "$UPLOADER --port $UPLOAD_PORT write_flash 0x40000 $BUILD_DIR/0x40000.bin",
        ]
)

env.Append(
    BUILDERS=dict(
        ElfToBin1=Builder(
            action=" ".join([
                "$FW_TOOL",
                "-eo", "$SOURCES",
                "-bo", "$TARGET",
                "-bs", ".text",
                "-bs", ".data",
                "-bs", ".rodata",
                "-bc", "-ec",
                ]),
            suffix=".bin"
        ),
        ElfToBin2=Builder(
            action=" ".join([
                "$FW_TOOL",
                "-eo", "$SOURCES",
                "-es", ".irom0.text",
                "$TARGET",
                "-ec",
                ]),
            suffix=".bin"
        )
    )
)

# The source code of "platformio-build-tool" is here
# https://github.com/ivankravets/platformio/blob/develop/platformio/builder/tools/platformio.py

CORELIBS = env.ProcessGeneral()

#
# Target: Build executable and linkable firmware
#
target_elf = env.BuildFirmware(
    CORELIBS +
    ["gcc", "hal", "phy", "pp", "net80211",
     "wpa", "main", "freertos", "lwip", "udhcp"])

#
# Target: Build the .bin file
#
target_bin1 = env.ElfToBin1(join("$BUILD_DIR", "0x00000"), target_elf)
target_bin2 = env.ElfToBin2(join("$BUILD_DIR", "0x40000"), target_elf)

target_bin = env.Alias(["target_bin"], [target_bin1, target_bin2])

#
# Target: Upload firmware
#
upload = env.Alias(["upload"], target_bin, "$UPLOADCMD")
AlwaysBuild(upload)
env.AutodetectUploadPort()

serial = env.Alias(["serial"], [], "pyser.py $UPLOAD_PORT")
AlwaysBuild(serial)

#
# Target: Define targets
#
Default(target_bin)
