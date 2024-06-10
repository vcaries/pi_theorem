# Pi Theorem Calculator

This Python module applies the Pi theorem (Buckingham π theorem) to a set of variables with given dimensions.

## Overview

The Pi theorem is used in dimensional analysis to compute dimensionless parameters (Pi terms) from a set of variables. This can simplify physical equations by reducing the number of variables involved.

## Functions

### apply_pi_theorem(variables: dict, output: bool = False) -> None | list[sp.Expr]:

Applies the Pi theorem to the provided variables and dimensions, printing a list of dimensionless numbers if `output` is `True`.

## Example Usage

```python
from pi_theorem_calculator import apply_pi_theorem

# Example usage based on (Chen, 1990)
variables: dict = {
    'tau': [0, 1, 0],        # Tip gap size [L]
    'rho': [1, -3, 0],       # Density [M L^-3]
    'dt': [0, 0, 1],         # Time step [T]
    'DeltaP': [1, -1, -2],   # Pressure difference [M L^-1 T^-2]
    'Gamma': [0, 2, -1],     # Circulation [L^2 T^-1]
    'y_v': [0, 1, 0],        # y coordinate of the vortex [L]
    'z_v': [0, 1, 0],        # z coordinate of the vortex [L]
    'y_c': [0, 1, 0],        # y coordinate of the vortex core [L]
    'z_c': [0, 1, 0],        # z coordinate of the vortex core [L]
    'v': [0, 1, -1],         # Velocity v [L T^-1]
    'w': [0, 1, -1],         # Velocity w [L T^-1]
}                            # 'name': [M, L, T]

apply_pi_theorem(variables)
```

## GUI Usage

The Pi Theorem Calculator also includes a graphical user interface (GUI) for easier input and visualization.

### Running the GUI

To launch the GUI, execute the following command in your terminal:

```sh
python gui.py
```

### Using the GUI

1. **Adding Variables:**
   - Enter the variable name and its dimensions (M, L, T) in the respective input fields.
   - Click the "Add Variable" button to add the variable to the list.

2. **Calculating Pi Terms:**
   - After adding all the necessary variables, click the "Calculate Pi Terms" button.
   - The calculated dimensionless Pi terms will be displayed in the "Dimensionless Numbers" section.

### GUI Example

1. **Add Variables:**
   - Variable: `tau`, M: `0`, L: `1`, T: `0`
   - Click "Add Variable".
   - Repeat for other variables like `rho`, `dt`, `DeltaP`, etc.

2. **Calculate Pi Terms:**
   - Click "Calculate Pi Terms".
   - View the results in the "Dimensionless Numbers" section.

### Note

If you encounter the following warning:

```
Warning: Ignoring XDG_SESSION_TYPE=wayland on Gnome. Use QT_QPA_PLATFORM=wayland to run on Wayland anyway.
```

You can set the environment variable `QT_QPA_PLATFORM` to `wayland` to force the application to use the Wayland platform plugin:

```sh
export QT_QPA_PLATFORM=wayland
python gui.py
```

## Author

**V. Caries**
