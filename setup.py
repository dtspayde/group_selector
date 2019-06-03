from setuptools import setup

setup(
        name='group_selector',
        version='0.1',
        py_modules=['group_selector'],
        install_requires=[
            'Click>=7.0'
            ],
        entry_points='''
            [console_scripts]
            group_selector=group_selector:cli
        ''',
)
