from setuptools import setup

setup(
    name="Brownfield resource generator",
    version="0.0.2",
    description="Generates HTML resource pages from result json input",
    url="https://github.com/digital-land/brownfield-resources",
    license="MIT",
    install_requires=["click",
                      "jinja2"
                      ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        'console_scripts': [
            'brownfield-resource-gen = resource_generator.cli:generate',
        ]
    },
    python_requires=">=3.6",
)
