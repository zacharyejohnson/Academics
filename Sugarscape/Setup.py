import distutils.core
import Cython.StringIOTree as s 
import Cython.Build
distutils.core.setup(
    ext_modules = Cython.Build.cythonize("DataCollector.pyx"))
