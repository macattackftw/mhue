from setuptools import setup, find_packages

setup(name='mhue',
      version='0.0.1',
      description='Intended to interface with Hue lights',
      install_requires=['requests'],
      python_requires='>3.9',
      author='Kyle MacMillan',
      author_email='kyle.w.macmillan@gmail.com',
      license='WTFPL',
      packages=find_packages(exclude=['test']),
      zip_safe=True)
