from setuptools import setup, find_packages

setup(
    packages=find_packages('src'),
    name='vkinder',
    package_dir={'': 'src'},
    py_modules=['main'],
    install_requires = [
        'pymongo',
        'vk-api',
        'pymystem3',
        'nltk',
    ]
)