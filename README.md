# SolarThermoSim

A Python-based simulation for a simple natural circulation heat loop, intended for educational purposes.

## Overview

This repository contains a basic simulation of a natural circulation loop, where buoyancy-driven flow is induced by heating one leg of a closed loop. The simulation is currently limited to using **water** as the heat transfer fluid.

## Installation and Usage

1. Clone the repository:
   ```bash
   git clone https://github.com/alex-heville/SolarThermoSim.git
   cd SolarThermoSim
   ```

2. Ensure you have Python 3.6 or later installed.

3. Run the simulation:
   ```bash
   python simulator.py
   ```

## System Parameters

The simulation models a simple vertical loop with the following default parameters:

- **Fluid:** Water at 20°C
- **Loop height:** 2.0 m
- **Pipe diameter:** 0.05 m
- **Heater power:** 1000.0 W
- **Cooler temperature:** 20.0 °C

These parameters can be adjusted by editing the `main()` function in `simulator.py`.

## Simulation Method

The simulation uses a simplified steady‑state approach:

1. The buoyancy pressure head is estimated from the temperature difference between the hot and cold legs.
2. The flow resistance is approximated with the Darcy–Weisbach equation.
3. An iterative solver balances the pressure head and the friction loss to obtain the flow rate.
4. The energy balance (heater power = mass flow × specific heat × temperature difference) is satisfied.

## Output

Running the script prints a dictionary containing:

- `flow_rate_m3_s` – volumetric flow rate (m³/s)
- `hot_leg_temp_C` – temperature of the hot leg (°C)
- `cold_leg_temp_C` – temperature of the cold leg (°C)
- `temperature_difference_C` – temperature difference between hot and cold legs (°C)
- `fluid` – name of the fluid used

## Limitations

- The model is highly simplified and intended for educational demonstration only.
- Fluid properties (density, specific heat, viscosity, thermal conductivity) are taken as constant values at a reference temperature.
- Thermal expansion coefficient is fixed (approximate value for water).
- The loop geometry is idealized as a single vertical height with a total length of four times the height.

## Future Enhancements

Planned improvements include:

- Adding support for other heat‑transfer fluids (e.g., molten salts, oils)
- Implementing temperature‑dependent fluid properties
- Allowing user‑specified parameters via command‑line arguments or a configuration file
- Adding a simple GUI or visualisation of the loop behaviour

## License

This project is provided under the MIT License. See the LICENSE file for details.

## Contributing

Contributions are welcome! Please open an issue to discuss proposed changes before submitting a pull request.