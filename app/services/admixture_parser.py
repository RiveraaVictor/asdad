# app/services/admixture_parser.py
import re
from .admixture_config import ADMIXTURE_MODELS

class AdmixtureParser:
    """Detecta o modelo e extrai os dados do texto de entrada."""

    def detect_model(self, data: str) -> str:
        """
        Detecta o modelo Admixture com base no número de linhas/componentes.
        """
        lines = [line for line in data.strip().split('\n') if line.strip()]
        num_components = len(lines)

        for model_key, config in ADMIXTURE_MODELS.items():
            if config['components'] == num_components:
                return model_key

        raise ValueError(f"Não foi possível detectar um modelo com {num_components} componentes. Verifique os dados ou a configuração.")

    def parse(self, data: str) -> dict:
        """
        Analisa os dados de entrada no formato 'Componente: XX.XX%' e retorna
        um dicionário com { 'Componente': proporcao_decimal }.
        """
        parsed_data = {}
        lines = [line for line in data.strip().split('\n') if line.strip()]
        pattern = re.compile(r'^(.*?):\s*(\d+(\.\d+)?)%?$')

        for line in lines:
            match = pattern.match(line.strip())
            if match:
                component_name = match.group(1).strip()
                # Converte a porcentagem para um valor decimal (ex: 33.43% -> 0.3343)
                percentage_value = float(match.group(2)) / 100.0
                parsed_data[component_name] = percentage_value

        return parsed_data