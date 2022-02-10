from __future__ import absolute_import, unicode_literals
import octoprint.plugin
import re
from octoprint.printer.estimation import PrintTimeEstimator

m73time = None
feedRate = 100

class M73ETA(octoprint.plugin.OctoPrintPlugin,octoprint.plugin.RestartNeedingPlugin,octoprint.plugin.ReloadNeedingPlugin):
  def handle_m73(self, comm_instance, phase, cmd, cmd_type, gcode, *args, **kwargs):
    global m73time
    global feedRate

    # Feedrate
    if gcode == "M220":
      m = re.search('(?<=S)\d+(\.\d+)?', cmd)
      if m:
        feedRate = float(m.group(0))

    if gcode == "M73":
      m = re.search('(?<=R)\d+(\.\d+)?', cmd)
      if m:
        m73time = float(m.group(0))

  def get_update_information(self):
    return dict(
        m73etaoverride=dict(
            displayName=self._plugin_name,
            displayVersion=self._plugin_version,

            type="github_release",
            current=self._plugin_version,
            user="sysadminsh",
            repo="OctoPrint-M73ETAOverride",

            pip="https://github.com/sysadminsh/OctoPrint-M73ETAOverride/archive/{target}.zip"
        )
    )

class M73PrintTimeEstimator(PrintTimeEstimator):
  def __init__(self, job_type):
    super(M73PrintTimeEstimator, self).__init__(job_type)

  def estimate(self, progress, printTime, cleanedPrintTime, statisticalTotalPrintTime, statisticalTotalPrintTimeType):
    global m73time

    if m73time == None:
      return super(M73PrintTimeEstimator, self).estimate(progress, printTime, cleanedPrintTime, statisticalTotalPrintTime, statisticalTotalPrintTimeType)

    estimates = int(round(60 * m73time / (feedRate / 100.0)))
    return estimates, "estimate"

def m73_create_estimator_factory(*args, **kwargs):
    return M73PrintTimeEstimator

__plugin_name__ = "M73 ETA Override"
__plugin_pythoncompat__ = ">=2.7,<4"

def __plugin_load__():
  global __plugin_implementation__
  __plugin_implementation__ = M73ETA()

  global __plugin_hooks__
  __plugin_hooks__ = {
    "octoprint.comm.protocol.gcode.sent": __plugin_implementation__.handle_m73,
    "octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information,
    "octoprint.printer.estimation.factory": m73_create_estimator_factory
  }
