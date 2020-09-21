import os

env = os.getenv(r"C:\Users\Lisa\Anaconda3\envs\LercheGUI")

os.environ["HDF5_DISABLE_VERSION_CHECK"] = "1"

print(os.environ["'LD_LIBRARY_PATH'"])