from setuptools import setup

with open('README.md') as f:
    readme = f.read()

setup(
    version='0.0.1',
    name='FuelSDK-Wrapper',
    description='Simplify and improve the FuelSDK for Salesforce Marketing Cloud (ExactTarget)',
    long_description=readme,
    author='Sebastien D\'Angelo',
    author_email='seb131286@msn.com',
    py_modules=['FuelSDK-Wrapper'],
    packages=[],
    url='https://github.com/seb-angel/FuelSDK-Python-Wrapper',
    license='MIT',
    install_requires=[
        'FuelSDK>=0.9.3',
        'suds-jurko>=0.6',
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries',
        'Programming Language :: Python :: 2.7',
    ],
)