import nidaqmx
import time
from nidaqmx.constants import TerminalConfiguration

# --- Canals ---
AI_POS = "cDAQ1Mod2/ai0"      # Pin B (Output Signal High)
AI_NEG = "cDAQ1Mod2/ai4"      # Pin C (Output Signal Low)
DO_POWER = "cDAQ1Mod1/port0/line0"   # Pin F (Power High)

# --- Crear tasques ---
with nidaqmx.Task() as ai, nidaqmx.Task() as do:

    # Sortida digital per alimentar el sensor
    do.do_channels.add_do_chan(DO_POWER)
    do.write(True)   # encén el sensor
    print("Sensor encès")

    # Entrada analògica diferencial
    ai.ai_channels.add_ai_voltage_chan(
        f"{AI_POS}:{AI_NEG}",
        terminal_config=TerminalConfiguration.DIFFERENTIAL
    )

    try:
        while True:
            v = ai.read()    # llegeix voltatge
            print(f"Voltatge del sensor: {v:.3f} V")
            time.sleep(0.5)

    except KeyboardInterrupt:
        print("Aturant...")

    finally:
        do.write(False)
        print("Sensor apagat")
