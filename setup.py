from setuptools import setup
import os


lib_dir = os.path.dirname(os.path.realpath(__file__))
requirements_path = lib_dir + "/requirements.txt"
install_requires = []
if os.path.isfile(requirements_path):
    with open(requirements_path) as f:
        install_requires = f.read().splitlines()

setup(
    name='evaltools',
    version='0.0',
    packages=['evaltools'],
    url='',
    license='MIT License',
    author='Lukas Ewecker',
    author_email='lukasewecker@web.de',
    description='Simple library to evaluate the performance of python functions.',
    install_requires=install_requires
)