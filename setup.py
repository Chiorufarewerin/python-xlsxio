import os
from glob import glob
from setuptools import setup, Extension
from setuptools.command.develop import develop as DevelopCommandOriginal


IS_DEVELOPMENT = False


class DevelopCommand(DevelopCommandOriginal):
    def initialize_options(self):
        global IS_DEVELOPMENT
        IS_DEVELOPMENT = True
        super().initialize_options()


class lazy_cythonize(list):
    def __init__(self, callback):
        self._list, self.callback = None, callback

    def c_list(self):
        if self._list is None:
            self._list = self.callback()
        return self._list

    def __iter__(self):
        for e in self.c_list():
            yield e

    def __getitem__(self, ii):
        return self.c_list()[ii]

    def __len__(self):
        return len(self.c_list())


def get_file_data(*paths) -> str:
    file_path = os.path.join(os.path.dirname(__name__), *paths)
    with open(file_path, encoding='utf-8') as f:
        return f.read()


def get_long_description() -> str:
    return get_file_data('README.md')


def get_version() -> str:
    data = get_file_data('xlsxio', '__init__.py')
    for row in data.split('\n'):
        if row.startswith("__version__ = '"):
            return row[15:].strip().strip("'")
    raise ValueError('Version string not found')


def get_compiler_derectives() -> dict:
    if IS_DEVELOPMENT:
        return {
            'profile': True,
            'linetrace': True,
        }
    return {}


def get_extra_extension_kwargs() -> dict:
    if IS_DEVELOPMENT:
        return {
            'extra_compile_args': ['-g'],
            'define_macros': [
                ('CYTHON_TRACE', '1'),
                ('CYTHON_TRACE_NOGIL', '1'),
            ],
        }
    return {}


def get_extensions():
    from Cython.Build import cythonize

    xlsxio_path = './deps/xlsxio'
    return cythonize(
        Extension(
            'xlsxio._xlsxio',
            sources=glob('./xlsxio/*.pyx') + glob(f'{xlsxio_path}/lib/*.c'),
            include_dirs=[
                f'{xlsxio_path}/include',
            ],
            libraries=[
                'expat',
                'zip',
            ],
            **get_extra_extension_kwargs(),

        ),
        compiler_directives=get_compiler_derectives(),
        force=True,
    )


setup(
    name='python-xlsxio',
    version=get_version(),
    license='MIT',
    url='https://github.com/Chiorufarewerin/python-xlsxio',
    author='Artur Beltsov',
    author_email='artur1998g@gmail.com',
    description='Wrapper xlsxio library for python',
    long_description=get_long_description(),
    long_description_content_type='text/markdown',
    packages=[
        'xlsxio',
    ],
    python_requires='>=3.6',
    setup_requires=[
        'cython>=0.29.0',
        'pytest-runner',
    ],
    install_requires=[
        'cython>=0.29.0',
    ],
    tests_require=[
        'pytest',
        'pytest-cov',
    ],
    zip_safe=False,
    keywords=[
        'xlsxio',
        'python',
        'c',
        'excel',
        'read',
    ],
    test_suite="tests",
    project_urls={
        'GitHub': 'https://github.com/Chiorufarewerin/python-xlsxio',
    },
    ext_modules=lazy_cythonize(get_extensions),
    cmdclass={
        'develop': DevelopCommand,
    },
)
