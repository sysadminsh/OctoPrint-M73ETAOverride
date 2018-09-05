# OctoPrint M73 ETA Override

Plugin that overrides OctoPrint ETA to values from last M73 gcode sent to the printer.

The last Sli3cr Prusa Edition implemented M73 gcode injecting to the generated gcodes. This M73 estimations works a much better for Prusa printers than normal OctoPrint ETA estimator. M73 are displayed on Prusa LCD already directly after receiving gcode so there is nothing to change but I think that it will be good to make this better estimation available also on other OctoPrint sources (web/mobile etc) so this plugin will override OctoPrint estimation with estimation from last M73 gcode sended.

## Setup

Install via the bundled [Plugin Manager](https://github.com/foosel/OctoPrint/wiki/Plugin:-Plugin-Manager)
or manually using this URL:

    https://github.com/sysadminsh/OctoPrint-M73ETAOverride/archive/master.zip


## Configuration

No configuration required. Just install plugin and it will start to overriding OctoPrint ETA with last M73 gcode.

Please note that if printer is starting (heating or leveling bed) ETA will show less than one minute.