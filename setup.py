from setuptools import setup

setup(name='kimg4',
      version='0.1.1',
      description='pure-python library for parsing/decrypting Apple\'s proprietary IMG4 format.',
      long_description='file: README.md',
      long_description_content_type='text/markdown',
      author='kritanta',
      url='https://github.com/kritantadev/kimg4',
      install_requires=['pyaes'],
      packages=['kimg4'],
      package_dir={
            'kimg4': 'src/kimg4',
      },
      classifiers=[
            'Programming Language :: Python :: 3',
            'License :: OSI Approved :: MIT License',
            'Operating System :: OS Independent'
      ]
      )
