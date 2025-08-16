# app/services/admixture_config.py

# Configuração dos modelos Admixture
ADMIXTURE_MODELS = {
    'K36': {
        'components': 36,
        'data_path': 'app/static/data/k36_data.json',
        'populations_path': 'app/static/data/k36_populations.json'
    },
    'JTest14': {
        'components': 14,
        'data_path': 'app/static/data/jtest14_data.json',
        'populations_path': 'app/static/data/jtest14_populations.json'
    }
}

def get_calculator_config():
    """
    Returns the configuration for the available admixture calculators.
    Each key is a calculator name, and the value is a dictionary
    containing the path to the data file and the population data file.
    """
    # Modified to only include K36 and JTest14 as requested.
    return {
        'K36': {
            'data_path': 'app/static/data/k36_data.json',
            'populations_path': 'app/static/data/k36_populations.json'
        },
        'JTest14': {
            'data_path': 'app/static/data/jtest14_data.json',
            'populations_path': 'app/static/data/jtest14_populations.json'
        }
    }

def get_available_calculators():
    """Returns a list of available calculator names."""
    return list(get_calculator_config().keys())