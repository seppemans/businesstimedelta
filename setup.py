from setuptools import setup

setup(
    name='businesstimedelta',
    version='0.2',
    description="Timedelta for business time. Supports exact amounts of time " +
                "(hours, seconds), custom schedules, holidays, and time zones.",
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Office/Business :: Scheduling'
    ],
    keywords='business working time timedelta hours businesstime businesshours',
    url='http://github.com/seppemans/businesstimedelta',
    author='seppemans',
    license='MIT',
    packages=['businesstimedelta', 'businesstimedelta.rules'],
    install_requires=[
        'pytz',
        'holidays'
    ],
    zip_safe=False,
    test_suite='nose.collector',
    tests_require=['nose'])
