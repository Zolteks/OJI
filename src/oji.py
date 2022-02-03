# nuitka-project: --windows-product-name="Orange Juice Invasion"
# nuitka-project: --windows-company-name="Arthus MEURET"
# nuitka-project: --windows-file-description="Orange Juice Invasion - A game by Arthus MEURET"
# nuitka-project: --windows-product-version=1.6.2.0
# nuitka-project: --windows-icon-from-ico=./assets/icon128.png
# nuitka-project: --windows-icon-from-ico=./assets/icon256.png
# nuitka-project: --include-data-file=editor_220x160.png=pyxel\editor\assets\editor_220x160.png
# nuitka-project: --include-data-file=oji.pyxres=
# nuitka-project: --include-data-file=ships.png=
# nuitka-project: --include-data-file=tiles_packed.png=
# nuitka-project: --onefile
# nuitka-project: --windows-disable-console
from jeu import Jeu
import time
import os
import tempfile

time.sleep(1)

if "NUITKA_ONEFILE_PARENT" in os.environ:
   splash_filename = os.path.join(
      tempfile.gettempdir(),
      "onefile_%d_splash_feedback.tmp" % int(os.environ["NUITKA_ONEFILE_PARENT"]),
   )

   if os.path.exists(splash_filename):
      os.unlink(splash_filename)
Jeu()