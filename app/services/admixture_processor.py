# app/services/admixture_processor.py
from .data_validator import AdmixtureDataValidator
from .admixture_parser import AdmixtureParser
from .geo_converter import GeoConverter
from .admixture_config import ADMIXTURE_MODELS

class AdmixtureProcessor:
    """Orquestra o processo completo de análise de dados Admixture."""

    def __init__(self, raw_data: str):
        self.raw_data = raw_data
        self.validator = AdmixtureDataValidator()
        self.parser = AdmixtureParser()
        self.converter = GeoConverter()

    def process(self):
        # 1. Validação de formato básico
        if not self.validator.validate_format(self.raw_data):
            raise ValueError("Formato de dados inválido. Use o formato 'Componente: Porcentagem%'.")

        # 2. Detecção do Modelo
        model_key = self.parser.detect_model(self.raw_data)
        model_config = ADMIXTURE_MODELS[model_key]

        # 3. Parsing dos Dados
        parsed_data = self.parser.parse(self.raw_data)

        # 4. Validação de consistência com o modelo
        self.validator.validate_consistency(parsed_data, model_config)

        # 5. Conversão para GeoJSON
        geojson_result = self.converter.convert(parsed_data, model_config)

        return {
            'modelName': model_config['name'],
            'geojson': geojson_result,
            'components': sorted(parsed_data.items(), key=lambda item: item[1], reverse=True)
        }