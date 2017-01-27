from setuptools import setup, find_packages


setup(
    name='drs4',
    author='Maximilian Nöthe',
    author_email='maximilian.noethe@tu-dortmund.de',
    packages=find_packages(),
    version='0.0.1',
    install_requires=['numpy'],
    tests_require=['pytest'],
    setup_requires=['pytest-runner'],
)
