from setuptools import find_packages,setup

setup(
    name='mcgenerator',
    version='0.0.1',
    author='Osama Rizk',
    author_email='info@cairosynth-ai.com',
    install_requires=["openai","langchain","streamlit","python-dotenv","pyPDF2"],
    packages=find_packages()
)