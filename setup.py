from os.path import dirname, join
from setuptools import setup, find_packages, Extension
from Cython.Build import cythonize


setup(
    name='python-xlsxio',
    version='0.0.3',
    license='MIT',
    url='https://github.com/Chiorufarewerin/python-xlsxio',
    author='Artur Beltsov',
    author_email='artur1998g@gmail.com',
    description='Wrapper xlsxio library for python',
    long_description=open(join(dirname(__file__), 'README.md'), encoding='utf-8').read(),
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
    install_requires=[
        'Cython',
    ],
    ext_modules=cythonize(
        Extension(
            'xlsxio.xlsxio_read',
            [
                'xlsxio/xlsxio_read.pyx',
            ],
            libraries=['xlsxio_read'],
        ),
    ),
)
