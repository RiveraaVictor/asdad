#!/usr/bin/env python3
# Teste para debug do erro

from app.services.admixture_processor import AdmixtureProcessor

# Dados de teste simples
test_data = """European: 50.0%
African: 30.0%
Asian: 20.0%"""

try:
    processor = AdmixtureProcessor(test_data)
    result = processor.process()
    print("Sucesso:", result)
except Exception as e:
    print(f"Erro: {type(e).__name__}: {str(e)}")
    import traceback
    traceback.print_exc()