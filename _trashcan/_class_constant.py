

class Signature:
    pass


class FunctionSymbol:
    """



    Bibliography:
        * Signature (Computer Science). Encyclopedia of Mathematics. URL: http://encyclopediaofmath.org/index.php?title=Signature_(Computer_Science)&oldid=29399

    """
    def __init__(
            self,
            domain,
            codomain,
            arity: int,
            signature: Signature):
        self._arity = 0

    @property
    def arity(self):
        """Arity.

        *Every function symbol f∈F is assigned an arity ar:F⟶N0 giving the number of arguments of f.*
        -- Signature (Computer Science). Encyclopedia of Mathematics


        Returns:
            int: The arity.
        """
        return self._arity

    @property
    def is_constant(self) -> bool:
        """Is Constant?

        *In the case ar(f)=0 for a function symbol f∈F, the symbol f is called a constant symbol.*
        -- Signature (Computer Science). Encyclopedia of Mathematics

        Returns:
            bool: True if the object is a constant, False otherwise.
        """
        return self._arity == 0


