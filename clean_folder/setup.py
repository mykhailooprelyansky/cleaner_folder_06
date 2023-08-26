from setuptools import setup

setup(name='clean_folder',
      version='0.0.1',
      description='Cleaning and sorting files in folder',
      url='http://github.com/mykhailooprelyansky/cleaner_folder_06',
      author='Mykhailo Oprelyanskiy',
      author_email='mykhailooprelianskiy@example.com',
      license='MIT',
      packages=['clean_folder'],
      entry_points={'console_scripts': ['clean-folder = clean_folder.clean:scan']})
