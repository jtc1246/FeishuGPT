from setuptools import setup

setup(
    name='FeishuGPT',
    version='0.1.2',
    author='Tiancheng Jiao',
    author_email='jtc1246@outlook.com',
    url='https://github.com/jtc1246/FeishuGPT',
    description='通过飞书机器人使用 ChatGPT',
    packages=['FeishuGPT'],
    install_requires=['myHttp', 'tiktoken', 'openai'],
    python_requires='>=3',
    platforms=["all"],
    license='GPL-2.0 License'
)
