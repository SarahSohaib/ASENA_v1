from setuptools import setup, find_packages

setup(
    name='Asena',
    version='0.1.0',
    author='Your Name',
    author_email='your.email@example.com',
    description='Asena is an intelligent virtual assistant that adapts to user needs and preferences.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/asena',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        'speechrecognition',
        'pyaudio',
        'numpy',
        'scikit-learn',
        'requests',
        'flask',  # or any other web framework you might use
        # Add other dependencies as needed
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)