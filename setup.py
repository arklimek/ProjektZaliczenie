from setuptools import setup, find_packages

setup(
    name="main",
    version="1.0.0",
    author="Arkadiusz Klimek, Antoni Knapczyk",
    packages=find_packages(),
    install_requires=[
        "panda3d",
        "panda3d-simplepbr",
        "panda3d-gltf",
    ],
    package_data={
        "": ["Assets/**/*", "myConfig.prc"],
    },
    entry_points={
        "console_scripts": [
            "panda3d_demo = main:main_entry",
        ],
    },
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires=">=3.8",
)
