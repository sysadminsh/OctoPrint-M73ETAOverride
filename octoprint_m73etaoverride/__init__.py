from __future__ import absolute_import
import octoprint.plugin
import re
from octoprint.printer.estimation import PrintTimeEstimator

m73time = 1

class M73ETA(octoprint.plugin.OctoPrintPlugin):
  def handle_m73(self, comm_instance, phase, cmd, cmd_type, gcode, *args, **kwargs):
    global m73time
    if gcode and gcode == "M73":
      m = re.search('(?<=R)\w+', cmd)
      if m:
        m73time = m.group(0)

  def get_update_information(*args, **kwargs):
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
    pass

  def estimate(self, progress, printTime, cleanedPrintTime, statisticalTotalPrintTime, statisticalTotalPrintTimeType):
    global m73time
    estimates = 60 * int(m73time)
    return estimates, "estimate"

def m73_create_estimator_factory(*args, **kwargs):
    return M73PrintTimeEstimator

__plugin_name__ = "M73 Eta Override"

def __plugin_load__():
  global __plugin_implementation__
  __plugin_implementation__ = M73ETA()

  global __plugin_hooks__
  __plugin_hooks__ = {
    "octoprint.comm.protocol.gcode.sent": __plugin_implementation__.handle_m73,
    "octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information,
    "octoprint.printer.estimation.factory": m73_create_estimator_factory
  }