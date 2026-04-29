from setuptools import setup, find_packages

with open('README.md', 'r') as f:
    long_description = f.read()

setup(
    name='orbit-sim',
    version='0.1.0',
    description='A professional-grade orbital mechanics simulation framework',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Rosso Sgroi',
    author_email='sgroirosso00@gmail.com',
    url='https://github.com/rossosgroi/orbit-sim',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'numpy',
        'scipy',
        'matplotlib',
        'pytest',
        'tqdm',
        'plotly',
        'numba',
        'PyQt5'
    ],
    extras_require={
        'dev': [
            'pytest-cov',
            'sphinx',
            'sphinx-rtd-theme'
        ]
    },
    entry_points={
        'console_scripts': [
            'orbit-sim=main:main'
        ]
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Astronomy',
        'Topic :: Scientific/Engineering :: Physics',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12'
    ],
    python_requires='>=3.8'
)