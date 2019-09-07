from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='businesstimedelta',
    version='1.0.1',
    description="Timedelta for business time. Supports exact amounts of time " +
                "(hours, seconds), custom schedules, holidays, and time zones.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
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
