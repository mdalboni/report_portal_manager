from distutils.core import setup

setup(
    name='reportportal_manager',
    packages=['reportportal_manager'],
    version='1.1',
    license='MIT',
    description='A simple abstraction for report portal library, for behave tests.',
    author='Maxwell Martins Dalboni',
    author_email='dalboni.max@hotmail.com',
    url='https://github.com/mdalboni',
    download_url='https://github.com/user/reponame/archive/v_05.tar.gz',
    keywords=['report', 'portal', 'behave'],
    install_requires=[
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
