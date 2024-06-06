# Pi Theorem Calculator

This Python module applies the Pi theorem (Buckingham π theorem) to a set of variables with given dimensions.

## Overview

The Pi theorem is used in dimensional analysis to compute dimensionless parameters (Pi terms) from a set of variables. This can simplify physical equations by reducing the number of variables involved.

## Functions

### apply_pi_theorem(variables: dict) -> None:

Applies the Pi theorem to the provided variables and dimensions, printing a list of dimensionless numbers.

## Example Usage

```python
from pi_theorem_calculator import apply_pi_theorem

# Example usage based on (Chen, 1990)
variables: dict = {
    'tau': [0, 1, 0],  		# Tip gap size [L]
    'rho': [1, -3, 0],  	# Density [M L^-3]
    'dt': [0, 0, 1],  		# Time step [T]
    'DeltaP': [1, -1, -2],  # Pressure difference [M L^-1 T^-2]
    'Gamma': [0, 2, -1],  	# Circulation [L^2 T^-1]
    'yv': [0, 1, 0],  		# y coordinate of the vortex [L]
    'zv': [0, 1, 0],  		# z coordinate of the vortex [L]
    'yc': [0, 1, 0],  		# y coordinate of the vortex core [L]
    'zc': [0, 1, 0],  		# z coordinate of the vortex core [L]
    'v': [0, 1, -1],  		# Velocity v [L T^-1]
    'w': [0, 1, -1],  		# Velocity w [L T^-1]
}  							# 'name': [M, L, T]

dimensionless_numbers = apply_pi_theorem(variables)
```

## Author

**V. Caries**
