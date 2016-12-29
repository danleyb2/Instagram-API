import os
import setuptools

__version__ = "1.4"
__author__ = "Nyaundi Brian"

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setuptools.setup(
    name='instagram-api',
    version=__version__,
    packages=setuptools.find_packages(),
    include_package_data=True,
    zip_safe=False,
    license='MIT',
    description='Instagram private API PHP',
    long_description=README,
    keywords="Instagram Private API Python",
    platforms='any',
    url='https://github.com/danleyb2/Instagram-API',
    author=__author__,
    author_email='ndieksman@gmail.com',
    install_requires=[
        'pycurl==7.43.0',
        'Pillow==3.4.2',
    ],
    classifiers=[
        # 'Development Status :: 1 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
    ],
)
