import nidaqmx
import time

with nidaqmx.Task() as task:
    task.do_channels.add_do_chan("cDAQ1Mod1/port0/line0")

    task.write(True)
    time.sleep(2)
    task.write(False)
