from setuptools import setup

setup(name='clean_folder',
      python_requires='>3.4.0',
      version='1',
      description='homework module7',
      url='https://github.com/kkkingqz/goit-homework/tree/main/module-7-setup/clean_folder',
      author='Bodya',
      author_email='kkingqz@gmail.com',
      license='MIT',
      packages=['clean_folder'],
      entry_points={'console_scripts': ['clean-folder = clean_folder.clean:main']})