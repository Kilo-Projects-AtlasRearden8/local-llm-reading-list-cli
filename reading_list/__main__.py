"""Allow ``python -m reading_list``."""

from .cli import main
import sys

sys.exit(main())
