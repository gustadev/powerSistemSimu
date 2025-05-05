from pathlib import Path
import sys
desktop = Path(__file__).absolute().parent.parent.parent.parent.parent
sys.path.append(str(desktop))