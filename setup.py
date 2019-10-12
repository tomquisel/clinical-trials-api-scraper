from distutils.core import setup

setup(
    name='clinical_trials_api_scraper',
    version='0.1.0',
    author='David Stuck',
    packages=['clinical_trials_api_scraper'],
    scripts=['clinical_trials_api_scraper/scripts/update_trials_store.py'],
    url='https://github.com/dstuck/clinical-trials-api-scraper',
    description='Scraper to pull trial reporting data from clinicaltrials.gov.',
    long_description=open('README.md').read(),
    install_requires=[
        "requests",
        "python-dateutil"
    ],
)
