from setuptools import setup, find_packages
import os

version = '1.0'

setup(name='wildcard.media',
      version=version,
      description="",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        ],
      keywords='video audio media plone tiny html5 mediaelement',
      author='nathan@vangheem.us',
      author_email='Nathan Van Gheem',
      url='https://github.com/collective/wildcard.media',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['wildcard'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'plone.transformchain',
          'plone.app.dexterity',
          'plone.directives.form',
          'plone.app.textfield'
      ],
      entry_points="""
      # -*- Entry points: -*-

      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
