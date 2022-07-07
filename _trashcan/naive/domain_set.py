


class DomainSet:
    """A set of mathematical domains.

    Design choice:
        In order to avoid key string manipulations, set elements are accessible as attributes, e.g. domains.n0.
    """
    def append(self, key, domain):
        # TODO: Prevent the usage of underscores and common names.
        setattr(self, key, domain)

