import octoprint.plugin
import re
from octoprint.printer.estimation import PrintTimeEstimator

m73time = 1

class M73ETA(octoprint.plugin.OctoPrintPlugin):
  def sent_m73(self, comm_instance, phase, cmd, cmd_type, gcode, *args, **kwargs):
    global m73time
    if gcode and gcode == "M73":
      m = re.search('(?<=R)\w+', cmd)
      if m:
        m73time = m.group(0)

class CustomPrintTimeEstimator(PrintTimeEstimator):
  def __init__(self, job_type):
    pass

  def estimate(self, progress, printTime, cleanedPrintTime, statisticalTotalPrintTime, statisticalTotalPrintTimeType):
    global m73time
    estimates = 60 * int(m73time)
    return estimates, "estimate"

def create_estimator_factory(*args, **kwargs):
    return CustomPrintTimeEstimator

def __plugin_load__():
  global __plugin_implementation__
  __plugin_implementation__ = M73ETA()

  global __plugin_hooks__
  __plugin_hooks__ = {
    "octoprint.comm.protocol.gcode.sent": __plugin_implementation__.sent_m73,
    "octoprint.printer.estimation.factory": create_estimator_factory
  }