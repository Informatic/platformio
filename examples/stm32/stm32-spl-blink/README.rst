How to buid PlatformIO based project
====================================

1. `Install PlatformIO <http://docs.platformio.org/en/latest/installation.html>`_
2. Download `source code with examples <https://github.com/ivankravets/platformio/archive/develop.zip>`_
3. Extract ZIP archive
4. Run these commands:

.. code-block:: bash

    # Change directory to example
    > cd platformio-develop/examples/stm32/stm32-spl-blink

    # Process example project
    > platformio run

    # Upload firmware
    > platformio run --target upload

    # Clean build files
    > platformio run --target clean
