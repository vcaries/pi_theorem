"""
    This module applies the Pi theorem (Buckingham π theorem) to a set of variables with given dimensions.

    The Pi theorem is used in dimensional analysis to compute dimensionless parameters (Pi terms) from
    a set of variables. This can simplify physical equations by reducing the number of variables involved.

    Functions:
        apply_pi_theorem(variables: dict) -> None:
            Applies the Pi theorem to the provided variables and dimensions, printing a list of dimensionless numbers.

    Example usage based on Chen, G.T.; Greitzer, E.M.; Tan, C.S.; Marble, F.E. Similarity Analysis of Compressor Tip Clearance Flow Structure 1990:
		variables: dict = {
			'tau': [0, 1, 0],  		# Tip gap size [L]
			'rho': [1, -3, 0],  	# Density [M L^-3]
			'dt': [0, 0, 1],  		# Time step [T]
			'DeltaP': [1, -1, -2],  # Pressure difference [M L^-1 T^-2]
			'Gamma': [0, 2, -1],  	# Circulation [L^2 T^-1]
			'y_v': [0, 1, 0],  		# y coordinate of the vortex [L]
			'z_v': [0, 1, 0],  		# z coordinate of the vortex [L]
			'y_c': [0, 1, 0],  		# y coordinate of the vortex core [L]
			'z_c': [0, 1, 0],  		# z coordinate of the vortex core [L]
			'v': [0, 1, -1],  		# Velocity v [L T^-1]
			'w': [0, 1, -1],  		# Velocity w [L T^-1]
		}  							# 'name': [M, L, T]
        apply_pi_theorem(variables)

    author: V. Caries (creator)
"""

# Import necessary packages
import sympy as sp


def apply_pi_theorem(variables: dict, output: bool = False) -> None | list[sp.Expr]:
    """
        Apply the Pi theorem to the given variables and their dimensions and print the dimensionless numbers.
        :param variables: Dictionary of variable names and their dimensions. Each dimension is a list of integers representing the base dimensions (e.g., [M, L, T]).
        :type variables: dict[str, list[int]]
        :param output: Whether to return the dimensionless numbers instead of printing them. Default is False.
        :type output: bool
        :return: None if output is False, otherwise a list of dimensionless numbers.
        :rtype: None | list[sp.Expr]
    """
    # Extract data from the dictionary
    names: list[str] = list(variables.keys())
    dimensions: list[list[int]] = list(variables.values())

    # Number of variable
    n: int = len(names)

    # Create symbols for each variable name
    var_symbols: list[sp.Symbol] = sp.symbols(names)

    # Create the dimension matrix
    dim_matrix: sp.Matrix = sp.Matrix(dimensions).transpose()

    # Calculate the rank of the dimension matrix
    rank: int = dim_matrix.rank()

    # Number of dimensionless Pi terms
    pi_terms_count: int = n - rank

    # Null space of the dimension matrix (basis for the Pi terms)
    null_space: list[sp.Matrix] = dim_matrix.nullspace()

    # Ensure we have the correct number of null space vectors
    if len(null_space) != pi_terms_count:
        raise ValueError('The null space does not have the expected number of vectors.')

    # Create the dimensionless Pi terms
    pi_terms: list[sp.Expr] = []
    for basis_vector in null_space:
        pi_term: int = 1
        for exponent, var_symbol in zip(basis_vector, var_symbols):
            pi_term *= var_symbol ** exponent

        pi_terms.append(sp.simplify(pi_term))

    if output:
        return pi_terms

    # Print the dimensionless numbers
    print('Dimensionless Numbers:')
    for i, pi_term in enumerate(pi_terms, 1):
        sp.pprint(sp.Eq(sp.symbols(f'Pi_{i}'), pi_term))


if __name__ == '__main__':
    # Example usage based on (Chen, 1990)
    variables: dict = {
        'tau': [0, 1, 0],  		# Tip gap size [L]
        'rho': [1, -3, 0],  	# Density [M L^-3]
        'dt': [0, 0, 1],  		# Time step [T]
        'DeltaP': [1, -1, -2],  # Pressure difference [M L^-1 T^-2]
        'Gamma': [0, 2, -1],  	# Circulation [L^2 T^-1]
        'y_v': [0, 1, 0],  		# y coordinate of the vortex [L]
        'z_v': [0, 1, 0],  		# z coordinate of the vortex [L]
        'y_c': [0, 1, 0],  		# y coordinate of the vortex core [L]
        'z_c': [0, 1, 0],  		# z coordinate of the vortex core [L]
        'v': [0, 1, -1],  		# Velocity v [L T^-1]
        'w': [0, 1, -1],  		# Velocity w [L T^-1]
    }  							# 'name': [M, L, T]

    # Perform the pi theorem
    apply_pi_theorem(variables)
