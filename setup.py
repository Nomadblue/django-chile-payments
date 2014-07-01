from setuptools import find_packages, setup

with open('README.md') as f:
    long_description = f.read()

setup(
    name='django-chile-payments',
    description='Chilean payment brokers for Django',
    long_description=long_description,
    version='0.1.1',
    packages=find_packages(),
    url='https://github.com/Nomadblue/django-chile-payments',
    license='MIT',
    author='José Sazo',
    author_email='jose.sazo@gmail.com',
    include_package_data=True,
)
