import nidaqmx
import time

AI_CH = "cDAQ1Mod2/ai0"           # Pin B (Output Signal High)
DO_POWER = "cDAQ1Mod1/port0/line0"   # Pin F (Power High)

with nidaqmx.Task() as ai, nidaqmx.Task() as do:

    # Alimentar el sensor
    do.do_channels.add_do_chan(DO_POWER)
    do.write(True)
    print("Sensor encès")

    # Entrada analògica simple (respecte GND)
    ai.ai_channels.add_ai_voltage_chan(AI_CH)

    try:
        while True:
            v = ai.read()
            print(f"Voltatge del sensor: {v:.4f} V")
            time.sleep(0.5)

    except KeyboardInterrupt:
        print("Aturant...")

    finally:
        do.write(False)
        print("Sensor apagat")
