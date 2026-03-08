import sys
import os

# allow importing backend modules
sys.path.append(os.path.join(os.path.dirname(__file__), "../backend"))

from app.main import app