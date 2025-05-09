from setuptools import setup, find_packages

setup(
    name="p2pchat",
    version="0.1",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "p2p-server=p2pchat.server:main",
            "p2p-client=p2pchat.client:main",
        ]
    },
    install_requires=[],
    author="Your Name",
    description="A simple peer-to-peer socket-based chat system.",
)
