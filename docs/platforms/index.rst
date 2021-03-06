.. _platforms:

Platforms & Embedded Boards
===========================

*PlatformIO* has pre-built different development platforms for popular OS
(*Mac OS X, Linux (+ARM) and Windows*). Each of them include compiler,
debugger, uploader (for embedded) and many other useful tools.

Also it has pre-configured settings for most popular **Embedded Platform
Boards**. You have no need to specify in :ref:`projectconf` type or frequency of
MCU, upload protocol or etc. Please use ``board`` option.

.. toctree::
    :maxdepth: 2

    atmelavr
    atmelsam
    stm32
    timsp430
    titiva
    teensy
    creating_platform
