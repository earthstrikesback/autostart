'''
Installation script
'''

from setuptools import setup



if __name__ == '__main__':
    setup(
        name = 'Autostart',
        version = '0.0.1',
        description = 'Form to create startup programs scripts',
        author = 'earthstrikesback',
        author_email = 'earthstrikesback@gmail.com',
        python_requires = '>=3.5',
        install_requires = ['pyforms-gui'],
        keywords = ['gui', 'gnome', 'start', 'autostart']
    )

