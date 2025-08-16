# app/routes/admixture.py
from flask import Blueprint, request, jsonify, render_template
from app.services.admixture_processor import AdmixtureProcessor

admixture_bp = Blueprint('admixture', __name__)

@admixture_bp.route('/analysis')
def analysis_page():
    """Renderiza a página principal de análise de ancestralidade."""
    return render_template('admixture/analysis.html')

@admixture_bp.route('/api/analyze', methods=['POST'])
def analyze_admixture_api():
    """Endpoint da API para processar dados Admixture."""
    data = request.json
    if not data or 'text_data' not in data or not data['text_data'].strip():
        return jsonify({'error': 'Nenhum dado enviado.'}), 400

    try:
        processor = AdmixtureProcessor(data['text_data'])
        result = processor.process()
        return jsonify(result)

    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        # Em produção, seria ideal logar o erro.
        print(f"Erro inesperado no processamento: {e}")
        return jsonify({'error': 'Ocorreu um erro interno ao processar sua solicitação.'}), 500