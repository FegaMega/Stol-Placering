#Downloads and installs pygame on your computer so the app can be run
#Also updates pygame when available
import os, sys
os.system("pip3 install pygame")

import app

sys.exit(app.main())