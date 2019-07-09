# OctoPrint M73 ETA Override

Plugin that overrides OctoPrints’ ETA to values from the last M73 gcode sent to the printer.

As of Sli3cr Prusa Edition version 1.41.0, M73 gcode injecting is supported to the generate accurate gcode estimations. M73 estimations works a much better for Prusa printers than the normal OctoPrint ETA estimator. Currently, M73 is displayed on the Prusa LCD immediately after receiving gcode, so there is nothing to change. I think it will be beneficial to expose this more accurate estimation on other OctoPrint sources (web/mobile etc), so this plugin will override OctoPrints’ estimation with the value of the last M73 gcode sent to the printer.

## Setup

Install via the bundled [Plugin Manager](https://github.com/foosel/OctoPrint/wiki/Plugin:-Plugin-Manager)
or manually using this URL:

    https://github.com/sysadminsh/OctoPrint-M73ETAOverride/archive/master.zip


## Configuration

No configuration is required. Just install plugin and it will start to override OctoPrints’ ETA with last M73 gcode value.

**Please note**: if printer is preparing itself (heating or leveling the bed), the ETA will show less than one minute.
