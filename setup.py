from setuptools import setup

setup(name="ArdentScan",
      version="0.1",
      description="A fully automated, dynamic, highly extendable, command line enumeration tool",
      url="https://github.com/onsecurity/ardentscanner",
      author="Calum Boal",
      author_email="Calum.Boal@onsecurity.co.uk",
      license="MIT",
      packages=["Ardent", "Ardent.lib", "Ardent.modules"],
      package_data={"Ardent": ["resources/*"]},
      entry_points={
          "console_scripts": [
              "ardent = Ardent.__main__:main"
          ]
      },
      install_requires=[
          "python-libnmap",
          "colorama",
          "tabulate",
      ],
      )
