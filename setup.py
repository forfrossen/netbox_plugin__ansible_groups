from setuptools import find_packages, setup

setup(
    name='netbox-ansible-groups',
    version='0.1.0',
    description='NetBox plugin for managing Ansible groups',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='forfrossen',
    license='Apache 2.0',
    install_requires=[],
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
)