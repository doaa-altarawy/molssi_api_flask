import setuptools

if __name__ == "__main__":
    setuptools.setup(
        name='molssi_api_flask',
        version="0.3.0",
        description='MolSSI code database',
        author='Doaa Altarawy',
        author_email='daltarawy@vt.edu',
        url="https://github.com/doaa-altarawy/molssi_api_flask",
        license='BSD-3C',
        packages=setuptools.find_packages(),
        install_requires=[
            'Flask==0.12.2',
            'Flask_Cors==3.0.3',
            'Flask-Jsonpify==1.5.0',
            'pymongo',
            'mongoengine',
        ],
        extras_require={
            'docs': [
                'sphinx', 
                'sphinxcontrib-napoleon',
                'sphinx_rtd_theme',
                'numpydoc',
            ],
            'tests': [
                'pytest>=3.0',
                'codecov',
                'pytest-cov',
                'pytest-pep8',
            ],
        },

        # tests_require=[
        #     'pytest',
        #     'pytest-cov',
        #     'pytest-pep8',
        # ],

        classifiers=[
            'Development Status :: 4 - Beta',
            'Intended Audience :: Science/Research',
            'Programming Language :: Python :: 2.7',
            'Programming Language :: Python :: 3.5',
        ],
        zip_safe=True,
    )