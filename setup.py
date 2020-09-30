from distutils.core import setup
setup(
    name='flask_neo4j_lite',
    packages=['flask_neo4j_lite'],
    version='0.1',
    license='MIT',
    description='Using Neo4J Easy',
    author='Janis Gösser',
    author_email='janisgoesser92@gmail.com',
    url='https://github.com/JangasCodingplace/flask-neo4j-lite',
    download_url='TODO', #
    keywords=['flask', 'neo4j', 'models', 'osm'],
    install_requires=["py2neo"],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development',
        'License :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)
