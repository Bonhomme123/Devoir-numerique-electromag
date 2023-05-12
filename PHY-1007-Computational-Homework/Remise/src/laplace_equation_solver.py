import numpy as np

from src.fields import ScalarField


def augmenter(A):
    """
    La fonction augmenter ajoute un coutour de zéros à un array numpy 2D.
    """
    s = A.shape
    c = [[0]]*s[0]
    r = [0]*(s[1]+2)
    A = np.hstack([c, A, c])
    A = np.vstack([r, A, r])
    return(A)

class LaplaceEquationSolver:
    """
    A Laplace equation solver used to compute the resultant potential field P in 2D-space generated by a constant
    voltage field V (for example due to wires).
    """

    def __init__(self, nb_iterations: int = 10000):                             #1000 itérations n'étaient pas suffisantes
        """
        Laplace solver constructor. Used to define the number of iterations for the relaxation method.

        Parameters
        ----------
        nb_iterations : int
            Number of iterations performed to obtain the potential by the relaxation method (default = 1000).
        """
        self.nb_iterations = nb_iterations


    def solve(self, constant_voltage: ScalarField, ) -> ScalarField:
        """
        Solve the Laplace equation to compute the potential field given a constant voltage field.

        Parameters
        ----------
        constant_voltage : ScalarField
            A scalar field V : ℝ² → ℝ ; (x, y) → V(x, y), where V(x, y) is the wires' voltage at a given point (x, y)
            in space.

        Returns
        -------
        potential : ScalarField
            A scalar field P : ℝ² → ℝ ; (x, y) → P(x, y), where P(x, y) is the electric potential at a given point
            (x, y) in space. The difference between P and V is that P gives the potential in the whole world, i.e in
            the wires and in the empty space between the wires, while the field V always gives V(x, y) = 0 if (x, y)
            is not a point belonging to an electric wire.
        """
        #Le code est ici:
        potentiel = constant_voltage #On initialise le potentiel
        masque = [] #On créé un masque pour retirer les valeurs des fils entre chaque itération
        for r in constant_voltage:
            row = []
            for v in r:
                if v != 0:
                    row += [0]
                else:
                    row += [1]
            masque += [row]
        masque = np.array(masque)


        for _ in range(self.nb_iterations):
            #code ici:
            potentiel = augmenter(augmenter(potentiel))# On ajoute 2 contours de zéros afin que les donnés sur les bords ne soient pas coupées
            potentiel = potentiel[2:,1:-1] + potentiel[1:-1,2:] + potentiel[1:-1,:-2] +potentiel[:-2,1:-1]
            potentiel = potentiel / 4
            potentiel = potentiel[1:-1, 1:-1]
            potentiel = potentiel*masque + constant_voltage #On reset les fils.

        return potentiel





