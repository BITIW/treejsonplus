from setuptools import setup, find_packages

with open('treejson/version.py') as f:
    exec(f.read())

setup(
    name='treejson',
    version=__version__,
    description='Этот пакет помогает вам обнаружить структуру JSON-строки.',
    author='Richard Tuin',
    author_email='richard@newnative.nl',
    url='https://github.com/rtuin/treejson',
    license='MIT',
    packages=find_packages(),
    install_requires=[],
    entry_points={
        'console_scripts': [
            'treejson=treejson:main'
        ]
    },
)
