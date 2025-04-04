#/setup.py

from setuptools import setup, find_packages

setup(
    name='animotion',
    version='0.1.2',
    description='A library to create keyframe-based animations for hardware devices like servos and LEDs',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author="Pena",
    author_email="penadoxo@gmail.com",
    url='https://github.com/peninha/animotion',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    python_requires='>=3.7',
    install_requires=[
        'matplotlib',
    ],
    keywords='animation hardware servo LED keyframe',
    license='MIT',
)
