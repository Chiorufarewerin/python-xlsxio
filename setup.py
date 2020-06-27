from os.path import dirname, join
from glob import glob
from setuptools import setup, find_packages, Extension
from Cython.Build import cythonize


VERSION = '0.0.4'

EXTENSIONS = cythonize(
    Extension(
        'xlsxio._xlsxio',
        sources=glob('./xlsxio/*.pyx') + glob('./deps/xlsxio-0.2.26/lib/*.c'),
        include_dirs=[
            './deps/xlsxio-0.2.26/include',
        ],
        libraries=[
            'expat',
            'zip',
        ],
    ),
)

with open(join(dirname(__file__), 'README.md'), encoding='utf-8') as f:
    LONG_DESCRIPTION = f.read()


setup(
    name='python-xlsxio',
    version=VERSION,
    license='MIT',
    url='https://github.com/Chiorufarewerin/python-xlsxio',
    author='Artur Beltsov',
    author_email='artur1998g@gmail.com',
    description='Wrapper xlsxio library for python',
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    packages=find_packages(exclude=['tests']),
    python_requires='>=3.6',
    zip_safe=False,
    keywords=[
        'xlsxio',
        'python',
        'c',
    ],
    project_urls={
        'GitHub': 'https://github.com/Chiorufarewerin/python-xlsxio',
    },
    ext_modules=EXTENSIONS,
)
