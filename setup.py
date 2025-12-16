from setuptools import setup, find_packages

setup(
    name="flood-warning-system",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        'streamlit>=1.28.0',
        'pandas>=2.1.3',
        'numpy>=1.25.0',
        'Pillow>=10.1.0',
        'gspread>=5.11.3',
        'oauth2client>=4.1.3',
    ],
    python_requires='>=3.8',
)