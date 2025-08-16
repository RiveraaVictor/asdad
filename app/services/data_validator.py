# app/services/data_validator.py
import re

class AdmixtureDataValidator:
    """Valida o formato e a consistência dos dados de entrada."""

    def validate_format(self, data: str) -> bool:
        """
        Valida se os dados de entrada estão no formato 'Componente: XX.XX%'.
        Permite múltiplas linhas e ignora linhas em branco.
        """
        lines = [line for line in data.strip().split('\n') if line.strip()]
        if not lines:
            return False

        # Padrão: Nome do componente, seguido por ':', espaços e um número com '%'.
        pattern = re.compile(r'^[a-zA-Z\s\(\)-]+:\s*\d+(\.\d+)?%?$')

        for line in lines:
            if not pattern.match(line.strip()):
                return False
        return True

    def validate_consistency(self, parsed_data: dict, model_config: dict):
        """
        Valida se os componentes encontrados correspondem ao modelo detectado.
        """
        expected_components = len(model_config['region_mapping'].keys())
        found_components = len(parsed_data.keys())

        # Verifica se o número de componentes é o esperado pelo modelo
        if found_components != model_config['components']:
             raise ValueError(f"Dados inválidos para o modelo {model_config['name']}. Esperava {model_config['components']} componentes, mas encontrou {found_components}.")

        # Verifica se os nomes dos componentes nos dados correspondem aos do modelo
        for component_name in parsed_data.keys():
            if component_name not in model_config['region_mapping']:
                raise ValueError(f"Componente desconhecido '{component_name}' para o modelo {model_config['name']}.")

def validate_data(parsed_data: dict, calculator: str):
    """
    Função de conveniência para validar dados.
    """
    validator = AdmixtureDataValidator()
    # Validação básica por enquanto
    if not parsed_data:
        raise ValueError("Dados não podem estar vazios")
    
    # Verificar se as porcentagens somam aproximadamente 100%
    total = sum(parsed_data.values())
    if abs(total - 1.0) > 0.1:  # Permite 10% de tolerância
        raise ValueError(f"As porcentagens devem somar 100%. Total atual: {total * 100:.1f}%")