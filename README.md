# OctoPrint M73 Eta Override

Plugin that overrides OctoPrint ETA to values from last M73 gcode sent to the printer.
Very usable with Prusa Slic3r which is adding M73 to generated gcodes and which is better than normal estimation.

## Setup

Install via the bundled [Plugin Manager](https://github.com/foosel/OctoPrint/wiki/Plugin:-Plugin-Manager)
or manually using this URL:

    https://github.com/sysadminsh/OctoPrint-M73Override


## Configuration

No configuration required. Just install plugin and it will start to overriding OctoPrint ETA with last M73 gcode.
Please note that if printer is starting (heating or leveling bed) ETA will show less than one minute.