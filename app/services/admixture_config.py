# app/services/admixture_config.py

# Mapeamento de nomes de componentes conhecidos para as regiões do nosso mapa genérico.
# Isso nos ajuda a automatizar a criação do region_mapping para cada modelo.
# A chave é uma parte do nome do componente (em minúsculas), o valor é a região do GeoJSON.
COMPONENT_KEYWORD_TO_REGION = {
    'north': 'Northern_Europe', 'nordic': 'Northern_Europe', 'scandinavian': 'Northern_Europe',
    'atlantic': 'Northern_Europe', 'baltic': 'Eastern_Europe', 'east_european': 'Eastern_Europe',
    'mediterranean': 'Southern_Europe', 'south_european': 'Southern_Europe', 'west_med': 'Southern_Europe',
    'east_med': 'Southern_Europe', 'italian': 'Southern_Europe', 'iberian': 'Southern_Europe',
    'caucasus': 'West_Asia_Caucasus', 'gedrosia': 'West_Asia_Caucasus', 'west_asian': 'West_Asia_Caucasus',
    'near_east': 'West_Asia_Caucasus', 'middle_east': 'West_Asia_Caucasus',
    'south_asian': 'South_Asia', 'harappan': 'South_Asia', 'indian': 'South_Asia',
    'siberian': 'Siberia_Central_Asia', 'central_asian': 'Siberia_Central_Asia',
    'east_asian': 'East_Asia', 'northeast_asian': 'East_Asia',
    'southeast_asian': 'Southeast_Asia',
    'north_african': 'North_Africa', 'maghreb': 'North_Africa',
    'sub_saharan': 'Sub_Saharan_Africa', 'west_african': 'Sub_Saharan_Africa', 'east_african': 'Sub_Saharan_Africa',
    'amerindian': 'Americas', 'native_american': 'Americas',
    'oceanian': 'Oceania', 'papuan': 'Oceania'
}


def get_region_for_component(component_name):
    """Encontra a melhor região genérica para um nome de componente."""
    c_lower = component_name.lower()
    for keyword, region in COMPONENT_KEYWORD_TO_REGION.items():
        if keyword in c_lower:
            return region
    return None  # Retorna None se nenhuma palavra-chave for encontrada


def generate_model_config(name, components, component_names):
    """Gera a configuração completa para um modelo."""
    region_mapping = {}
    for c_name in component_names:
        region = get_region_for_component(c_name)
        if region:
            region_mapping[c_name] = region
        # Se a região não for encontrada, o componente será ignorado no mapa, mas ainda aparecerá na legenda.

    return {
        'name': name,
        'components': components,
        'geojson_file': 'app/static/geojson/generic_world_regions.json',
        'region_mapping': region_mapping,
        'color_palette': []  # A ser preenchido dinamicamente se necessário
    }


# Nomes dos componentes para cada modelo (essencial para o mapeamento)
# Esta informação foi pesquisada com base nos nomes dos modelos.
MODEL_COMPONENT_NAMES = {
    'K7b': ['African', 'Atlantic_Baltic', 'East_Asian', 'Siberian', 'South_Asian', 'Southeast_Asian', 'West_Asian'],
    'K12b': ['Gedrosia', 'Siberian', 'Northwest_African', 'Southeast_Asian', 'Atlantic_Med', 'North_European',
             'South_Asian', 'East_African', 'Southwest_Asian', 'East_Asian', 'Caucasus', 'Sub_Saharan'],
    'globe13': ['Siberian', 'Amerindian', 'West_African', 'Palaeo_African', 'Southwest_Asian', 'East_Asian',
                'Mediterranean', 'Australasian', 'Arctic', 'West_European', 'South_Asian', 'Northeast_European',
                'Southeast_Asian'],
    'world9': ['Amerindian', 'East_Asian', 'African', 'Atlantic_Baltic', 'Australasian', 'Siberian', 'South_Asian',
               'Southern', 'West_Asian'],
    'K13': ['North_Atlantic', 'Baltic', 'West_Med', 'West_Asian', 'East_Med', 'Red_Sea', 'South_Asian', 'East_Asian',
            'Siberian', 'Amerindian', 'Oceanian', 'Northeast_African', 'Sub-Saharan'],
    'K36': ['Amerindian', 'Arabian', 'Armenian', 'Basque', 'Central_African', 'Central_Euro', 'East_African',
            'East_Asian', 'East_Balkan', 'East_Central_Euro', 'East_Med', 'Eastern_Euro', 'Fennoscandian', 'French',
            'Iberian', 'Indo-Chinese', 'Italian', 'Malayan', 'Near_Eastern', 'North_African', 'North_Atlantic',
            'North_Caucasian', 'North_Sea', 'Northeast_African', 'Oceanian', 'Omotic', 'Pygmy', 'Siberian',
            'South_Asian', 'South_Central_Asian', 'South_Chinese', 'South_West_Asian', 'Southeast_Asian', 'Tibetan',
            'Volga-Ural', 'West_African'],
    'HarappaWorld': ['S-Indian', 'Baloch', 'Caucasian', 'NE-Euro', 'SE-Asian', 'Siberian', 'NE-Asian', 'Papuan',
                     'American', 'Beringian', 'Mediterranean', 'SW-Asian', 'San', 'E-African', 'Pygmy', 'W-African']
    # Adicionar outras listas de componentes aqui...
}

# Dicionário final que será usado pela aplicação
ADMIXTURE_MODELS = {}

# Preenche o dicionário ADMIXTURE_MODELS dinamicamente
for model_key, component_list in MODEL_COMPONENT_NAMES.items():
    model_name_full = f"Model {model_key}"  # Placeholder, idealmente viria de uma config mais detalhada
    if model_key == 'K12b': model_name_full = "Dodecad K12b"
    if model_key == 'K13': model_name_full = "Eurogenes K13"

    ADMIXTURE_MODELS[model_key] = generate_model_config(
        name=model_name_full,
        components=len(component_list),
        component_names=component_list
    )

# Adiciona manualmente modelos que não têm uma lista de componentes definida acima
# (Este é um fallback caso a lista `MODEL_COMPONENT_NAMES` esteja incompleta)
if 'K15' not in ADMIXTURE_MODELS:
    ADMIXTURE_MODELS['K15'] = {
        'name': 'Eurogenes K15', 'components': 15,
        'geojson_file': 'app/static/geojson/generic_world_regions.json',
        'region_mapping': {},  # TODO: Preencher com os 15 nomes de componentes e mapear
        'color_palette': []
    }