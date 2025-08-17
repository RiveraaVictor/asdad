# app/services/admixture_config.py

# Configuração dos modelos Admixture
ADMIXTURE_MODELS = {
    'K2': {
        'name': 'K2 - Modelo Básico',
        'components': 2,
        'geojson_file': 'app/static/geojson/generic_world_regions.json',
        'region_mapping': {
            'European': 'Europe',
            'African': 'Africa'
        }
    },
    'K3': {
        'name': 'K3 - Modelo Simples', 
        'components': 3,
        'geojson_file': 'app/static/geojson/generic_world_regions.json',
        'region_mapping': {
            'European': 'Europe',
            'East_Asian': 'Asia',
            'African': 'Africa'
        }
    },
    'K12': {
        'name': 'K12 - Modelo Detalhado',
        'components': 12,
        'geojson_file': 'app/static/geojson/k12b_regions.json',
        'region_mapping': {
            'European': 'Europe',
            'East_Asian': 'Asia',
            'African': 'Africa',
            'Native_American': 'Americas',
            'Oceanian': 'Oceania',
            'Middle_Eastern': 'Middle_East',
            'South_Asian': 'South_Asia',
            'Central_Asian': 'Central_Asia',
            'Siberian': 'Siberia',
            'North_African': 'North_Africa',
            'Mediterranean': 'Mediterranean',
            'Baltic': 'Baltic'
        }
    },
    'K15': {
        'name': 'K15 - Modelo Avançado',
        'components': 15,
        'geojson_file': 'app/static/geojson/k15_regions.json',
        'region_mapping': {
            'European': 'Europe',
            'East_Asian': 'Asia',
            'African': 'Africa',
            'Native_American': 'Americas',
            'Oceanian': 'Oceania',
            'Middle_Eastern': 'Middle_East',
            'South_Asian': 'South_Asia',
            'Central_Asian': 'Central_Asia',
            'Siberian': 'Siberia',
            'North_African': 'North_Africa',
            'Mediterranean': 'Mediterranean',
            'Baltic': 'Baltic',
            'Scandinavian': 'Scandinavia',
            'Caucasian': 'Caucasus',
            'Southeast_Asian': 'Southeast_Asia'
        }
    },
    'K36': {
        'name': 'K36 - Modelo Completo',
        'components': 36,
        'geojson_file': 'app/static/geojson/k36_regions.json',
        'region_mapping': {
            'European': 'Europe',
            'East_Asian': 'Asia',
            'African': 'Africa',
            'Native_American': 'Americas',
            'Oceanian': 'Oceania',
            'Middle_Eastern': 'Middle_East',
            'South_Asian': 'South_Asia',
            'Central_Asian': 'Central_Asia',
            'Siberian': 'Siberia',
            'North_African': 'North_Africa',
            'Mediterranean': 'Mediterranean',
            'Baltic': 'Baltic',
            'Scandinavian': 'Scandinavia',
            'Caucasian': 'Caucasus',
            'Southeast_Asian': 'Southeast_Asia',
            'Amerindian': 'Amerindian',
            'Sub_Saharan': 'Sub_Saharan',
            'West_African': 'West_Africa',
            'East_African': 'East_Africa',
            'Pygmy': 'Central_Africa',
            'San': 'Southern_Africa',
            'Red_Sea': 'Red_Sea',
            'Omotic': 'Horn_Africa',
            'Maghrebi': 'Maghreb',
            'Coptic': 'Egypt',
            'Nubian': 'Nubia',
            'Nilo_Saharan': 'Nilo_Saharan',
            'Hadramaut': 'Arabia',
            'Arabian': 'Arabia',
            'Yemenite_Jewish': 'Yemen',
            'Ethiopian_Jewish': 'Ethiopia',
            'Mizrahi_Jewish': 'Levant',
            'Sephardic_Jewish': 'Iberia',
            'Ashkenazi_Jewish': 'Europe',
            'Caucasus_Jewish': 'Caucasus',
            'Levantine': 'Levant',
            'Arabian_Peninsula': 'Arabia'
        }
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