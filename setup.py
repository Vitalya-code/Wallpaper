from io import open
from setuptools import setup
from auto_py_to_exe import __version__ as version

setup(
    name='Wallpaper-gui',
    version='0.7',
    url='https://github.com/Vitalya-code/Wallpaper',
    license='MIT',
    author='Vitalya',
    author_email='vitalikkmita@gmail.com',
    description='This program can download background image for your desktop.',
    keywords=['gui', 'executable'],
    packages=['Wallpaper-gui'],
    include_package_data=True,
    install_requires=[        
          'PyQt6',
          'requests',
          'beautifulsoup4',
          'lxml',
          'screeninfo',
          'pywin32',
          'pyqtdarktheme'],
    
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX :: Linux']
)


