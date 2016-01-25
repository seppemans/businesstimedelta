from setuptools import setup


def readme():
    with open('README.md') as f:
        return f.read()

setup(
    name='businesstimedelta',
    version='0.1',
    description='Timedelta for business time. Supports exact amounts of time (hours, seconds), custom schedules, holidays, and time zones.',
    long_description=readme(),
    classifiers=[
      'Development Status :: 3 - Alpha',
      'License :: OSI Approved :: MIT License',
      'Programming Language :: Python :: 2.7',
      'Topic :: Office/Business :: Scheduling'
    ],
    keywords='business working time timedelta hours businesstime businesshours',
    url='http://github.com/seppemans/businesstimedelta',
    author='seppemans',
    license='MIT',
    packages=['businesstimedelta'],
    install_requires=[
        'pytz',
    ],
    zip_safe=False,
    test_suite='nose.collector',
    tests_require=['nose'])
