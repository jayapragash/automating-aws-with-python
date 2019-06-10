from setuptools import setup

setup(
    name='Static_Website',
    version='0.1',
    author='Jayapragash Baskar',
    author_email='jayapragash_b@yahoo.com',
    description='Static_Website is a tool to deploy static websites to AWS.',
    license='GPLv3+',
    packages=['webotron'],
    url='https://github.com/jayapragash/automating-aws-with-python/tree/master/01-webotron',
    install_requires=[
        'click',
        'boto3'
    ],
    entry_points='''
        [console_scripts]
        webotron=webotron.webotron:cli
    '''
)
