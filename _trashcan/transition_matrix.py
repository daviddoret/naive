from _trashcan import binary_vector, binary_matrix


class TransitionMatrix(binary_matrix.BinaryMatrix):

    def __init__(self, source_object: object):
        super().__init__(source_object)
        self.check_consistency()  # TODO: DESIGN FLAW: The check_consistency() method is called twice, once from super().__init__() and second in __init__().

    def check_consistency(self) -> bool:
        return super().check_consistency()

    def copy(self):
        """Return a copy of itself"""
        return TransitionMatrix(self._bool_numpy_array)

    def get_immediate_successors_iv(self, index) -> binary_vector.BinaryVector:
        """Return the incidence vector of immediate successors of a state by index position"""
        return super().get_row(index)

    def get_s_path_set_iv(self, s_index: int) -> binary_vector.BinaryVector:
        """Return the incidence vector of the set of states in Path(s), i.e. IV(S, {Path(s)})

        Path(s) is infinite.
        By definition, the set of states in Path(s), noted {Path(s)}, is finite and is a subset of S.

        :param s_index: The index position of state s
        :return: IV(S, {Path(s)})
        """
        s_path_set_iv = self._get_s_path_set_iv(s_index)
        return s_path_set_iv

    def _get_s_path_set_iv(self, s_index: int, iv: binary_vector.BinaryVector = None) -> binary_vector.BinaryVector:
        """The internal method that return the incidence vector of the set of states in Path(s)

        This method is identical to the public method except that it implements the internal parameter subset to recursively build the finite set.

        Path(s) is infinite.
        By definition, the set of states in Path(s) is finite and is a subset of S.

        :param s_index: The index position of state s
        :param iv: The incidence vector, used recursively to reduce the infinite Path(s) to a finite set
        :return: IV(S, {Path(s)})
        """
        if iv is None:
            iv = binary_vector.BinaryVector(size=self.get_dimension_1_length())

        # Add s
        if not iv[s_index]:
            iv[s_index] = 1

        # Retrieve the incidence vector of the immediate successors of s
        iv_successors = self.get_immediate_successors_iv(s_index)
        for s_prime_index in range(0, self.get_dimension_1_length()):
            # Check if s' is not already present in the incidence vector
            if not iv[s_prime_index]:
                # Check if s' is a successor of s from the incidence vector
                if iv_successors[s_prime_index]:
                    # Then add s' to the incidence vector
                    iv[s_prime_index] = 1
                    # Recursively retrieve the set of states from Path(s').
                    # Because we pass 'subset' to the recursive function,
                    # we avoid infinite loops.
                    iv = self._get_s_path_set_iv(s_prime_index, iv)

        return iv
