import nidaqmx

with nidaqmx.Task() as task:
    task.ai_channels.add_ai_voltage_chan("cDAQ1Mod2/ai0")
    value = task.read()
    print("Voltage:", value)
