import src
import os
import setuptools

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setuptools.setup(
    name='instagram-python',
    version=src.__version__,
    packages=setuptools.find_packages(),
    include_package_data=True,
    zip_safe=False,
    license='MIT',
    description='Instagram PYTHON',
    long_description=README,
    keywords="Instagram Private API Python",
    platforms='any',
    url='https://github.com/danleyb2/Instagram-API',
    author=src.__author__,
    author_email='ndieksman@gmail.com',
    classifiers=[
        #'Development Status :: 1 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
    ],
)
