from distutils.core import setup

setup(
    name='reportportal_manager',
    packages=['reportportal_manager'],  # Chose the same as "name"
    version='0.1',
    license='MIT',
    description='A simple abstraction for report portal library, for behave tests.',
    # Give a short description about your library
    author='Maxwell Martins Dalboni',  # Type in your name
    author_email='dalboni.max@hotmail.com',  # Type in your E-Mail
    url='https://github.com/mdalboni',
    download_url='https://github.com/user/reponame/archive/v_01.tar.gz',
    keywords=['report','portal','behave'],
    install_requires=[  # I get to this in a second
        'reportportal_client',
        'behave'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
)
