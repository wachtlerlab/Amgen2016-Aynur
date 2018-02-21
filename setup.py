from setuptools import setup, find_packages
setup(
    name="amgenaynur2016",
    use_scm_version=True,
    setup_requires=['setuptools_scm'],
    packages=find_packages(exclude=["^\."]),
    exclude_package_data={'': ["Readme.md"]},
    install_requires=["numpy==1.11",
                      "matplotlib>=1.5.3",
                      "scipy==0.18.1",
                      "astropy",
                      "seaborn>=0.7.1",
                      "neo==0.4",
                      "nixio>=0.1.3",
                      "sympy",
                      "playdoh",
                      "pycuda",
                      "brian>=1.4.3",
                      ],

    python_requires=">=2.7",
)