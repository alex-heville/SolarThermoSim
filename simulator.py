"""
SolarThermoSim - Natural Circulation Heat Loop Simulation

A simple educational simulation of a natural circulation loop using water as the heat transfer fluid.
"""

import math

class Fluid:
    """Base class for fluid properties."""
    
    def __init__(self, name, density, specific_heat, viscosity, thermal_conductivity):
        self.name = name
        self.density = density  # kg/m^3
        self.specific_heat = specific_heat  # J/(kg·K)
        self.viscosity = viscosity  # Pa·s
        self.thermal_conductivity = thermal_conductivity  # W/(m·K)

class Water(Fluid):
    """Water at 20°C."""
    
    def __init__(self):
        super().__init__(
            name="Water",
            density=998.0,  # kg/m^3
            specific_heat=4182.0,  # J/(kg·K)
            viscosity=0.001002,  # Pa·s
            thermal_conductivity=0.598  # W/(m·K)
        )

class NaturalCirculationSimulator:
    """Simulate a natural circulation loop."""
    
    def __init__(self, fluid, loop_height, pipe_diameter, heater_power, cooler_temp):
        """
        Initialize simulation parameters.
        
        Parameters:
        fluid: Fluid object
        loop_height: vertical height of loop (m)
        pipe_diameter: inner diameter of pipe (m)
        heater_power: heat input from solar collector (W)
        cooler_temp: temperature of cooler (cold side) in °C
        """
        self.fluid = fluid
        self.loop_height = loop_height
        self.pipe_diameter = pipe_diameter
        self.heater_power = heater_power
        self.cooler_temp = cooler_temp
        self.cross_section = math.pi * (pipe_diameter / 2) ** 2
        
    def calculate_flow_rate(self, delta_t):
        """
        Estimate flow rate due to buoyancy-driven circulation.
        
        Simplified model: buoyancy pressure head = g * rho * beta * delta_t * height
        Flow resistance approximated with Darcy-Weisbach equation.
        
        Parameters:
        delta_t: temperature difference between hot and cold legs (°C)
        
        Returns:
        flow_rate: volumetric flow rate (m^3/s)
        """
        g = 9.81  # m/s^2
        rho = self.fluid.density
        beta = 0.00021  # thermal expansion coefficient for water (1/K) - approximate
        # For simplicity, assume constant beta; for molten salt we'll need to adjust.
        
        pressure_head = g * rho * beta * delta_t * self.loop_height
        
        # Estimate friction factor (assuming laminar flow for simplicity)
        velocity_guess = 0.1  # initial guess m/s
        reynolds = rho * velocity_guess * self.pipe_diameter / self.fluid.viscosity
        if reynolds < 2000:
            friction_factor = 64 / reynolds if reynolds > 0 else 0.064
        else:
            friction_factor = 0.316 / (reynolds ** 0.25)  # Blasius for turbulent
        
        # Pressure drop due to friction around loop (simplified as single pipe length = 4 * height)
        loop_length = 4 * self.loop_height
        pressure_drop = friction_factor * (loop_length / self.pipe_diameter) * (rho * velocity_guess ** 2) / 2
        
        # Solve for velocity where pressure_head = pressure_drop (iterative)
        # Use simple iteration for demonstration
        tolerance = 1e-6
        max_iter = 100
        for i in range(max_iter):
            reynolds = rho * velocity_guess * self.pipe_diameter / self.fluid.viscosity
            if reynolds < 2000:
                friction_factor = 64 / reynolds if reynolds > 0 else 0.064
            else:
                friction_factor = 0.316 / (reynolds ** 0.25)
            pressure_drop = friction_factor * (loop_length / self.pipe_diameter) * (rho * velocity_guess ** 2) / 2
            residual = pressure_head - pressure_drop
            if abs(residual) < tolerance:
                break
            # Update velocity guess using simple Newton-like step (crude)
            velocity_guess += residual / (rho * velocity_guess * loop_length / self.pipe_diameter) if velocity_guess != 0 else 0.01
            velocity_guess = max(velocity_guess, 1e-5)
        
        flow_rate = velocity_guess * self.cross_section
        return flow_rate
    
    def simulate(self, initial_temp=20.0):
        """
        Run a simple steady-state simulation.
        
        Parameters:
        initial_temp: initial fluid temperature (°C)
        
        Returns:
        dict containing results: flow_rate, hot_temp, cold_temp, delta_t
        """
        # Simplified energy balance: heater_power = flow_rate * rho * cp * delta_t
        # We need to solve iteratively because flow_rate depends on delta_t
        delta_t_guess = 10.0  # °C
        for _ in range(20):
            flow_rate = self.calculate_flow_rate(delta_t_guess)
            # Energy balance: Q = m_dot * cp * delta_t
            mass_flow = flow_rate * self.fluid.density
            if mass_flow > 0:
                delta_t_calc = self.heater_power / (mass_flow * self.fluid.specific_heat)
            else:
                delta_t_calc = delta_t_guess
            # Update guess
            delta_t_guess = 0.5 * delta_t_guess + 0.5 * delta_t_calc
        
        hot_temp = self.cooler_temp + delta_t_guess
        cold_temp = self.cooler_temp
        
        return {
            "flow_rate_m3_s": flow_rate,
            "hot_leg_temp_C": hot_temp,
            "cold_leg_temp_C": cold_temp,
            "temperature_difference_C": delta_t_guess,
            "fluid": self.fluid.name
        }

def main():
    """Example usage of the simulator."""
    water = Water()
    sim = NaturalCirculationSimulator(
        fluid=water,
        loop_height=2.0,
        pipe_diameter=0.05,
        heater_power=1000.0,
        cooler_temp=20.0
    )
    results = sim.simulate()
    print("Natural Circulation Simulation Results:")
    for key, value in results.items():
        print(f"{key}: {value}")

if __name__ == "__main__":
    main()