from __future__ import absolute_import
import octoprint.plugin
import re
from octoprint.printer.estimation import PrintTimeEstimator
from octoprint.filemanager.analysis import GcodeAnalysisQueue

m73time = None

class M73ETA(octoprint.plugin.OctoPrintPlugin,octoprint.plugin.RestartNeedingPlugin,octoprint.plugin.ReloadNeedingPlugin):
  def handle_m73(self, comm_instance, phase, cmd, cmd_type, gcode, *args, **kwargs):
    global m73time
    if gcode and gcode == "M73":
      m = re.search('(?<=R)\w+', cmd)
      if m:
        m73time = m.group(0)

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

    estimates = 60 * int(m73time)
    return estimates, "estimate"

def m73_create_estimator_factory(*args, **kwargs):
    return M73PrintTimeEstimator

class M73AnalysisQueue(GcodeAnalysisQueue):
  def _do_analysis(self, high_priority=False):
    results = super(M73AnalysisQueue, self)._do_analysis(high_priority=high_priority)
    for line in open(self._current.absolute_path):
      m = re.match('M73.*R(\d+)', line)
      if m:
        results['estimatedPrintTime'] = int(m.group(1))*60
        break
    return results

def m73_gcode_analysis_queue(*args, **kwargs):
  return dict(gcode=lambda finished_callback: M73AnalysisQueue(finished_callback))

__plugin_name__ = "M73 ETA Override"

def __plugin_load__():
  global __plugin_implementation__
  __plugin_implementation__ = M73ETA()

  global __plugin_hooks__
  __plugin_hooks__ = {
    "octoprint.comm.protocol.gcode.sent": __plugin_implementation__.handle_m73,
    "octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information,
    "octoprint.printer.estimation.factory": m73_create_estimator_factory,
    "octoprint.filemanager.analysis.factory": m73_gcode_analysis_queue
  }
