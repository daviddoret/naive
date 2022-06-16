from typing import Final
import inspect  # To manage output verbosity


BASE_STACK_LEVEL: Final[int] = len(inspect.stack())
DEFAULT_PRECISION: Final[int] = 3
OUTPUT_HORIZONTAL_DIRECTION: Final[int] = 3
OUTPUT_VERTICAL_DIRECTION: Final[int] = 4
OUTPUT_LATEX_MATH: Final[int] = 1
OUTPUT_UNICODE: Final[int] = 2

# Verbosity constants
VERBOSITY: Final[int] = 3
INSANE: Final[int] = 4 # Unlimited details
DETAILED: Final[int] = 3 # Human-readable details
BALANCED: Final[int] = 2 # Results and interesting facts
RESULT: Final[int] = 1 # Results
NONE: Final[int] = 0 # No output


