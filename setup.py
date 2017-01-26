from setuptools import setup


setup(
    name='drs',
    author='Maximilian Nöthe',
    author_email='maximilian.noethe@tu-dortmund.de',
    version='0.0.1',
    install_requires=['numpy'],
    tests_require=['pytest'],
    setup_requires=['pytest-runner'],
)
