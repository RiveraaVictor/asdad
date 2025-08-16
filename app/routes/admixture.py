# app/routes/admixture.py

from flask import Blueprint, render_template, request, jsonify
from app.services.admixture_parser import parse_input
from app.services.admixture_processor import find_closest_populations
from app.services.data_validator import validate_data

admixture_bp = Blueprint('admixture', __name__)


@admixture_bp.route('/analysis', methods=['POST'])
def analysis():
    # List of country codes to display based on the image provided.
    countries_to_show = [
        'PT', 'ES', 'FR', 'IT', 'DE', 'GB', 'IE',
        'SE', 'NO', 'FI', 'PL', 'UA', 'RU', 'GR', 'TR'
    ]

    raw_data = request.form.get('data')
    calculator = request.form.get('calculator')

    if not raw_data or not calculator:
        return render_template('admixture/analysis.html', error="No data or calculator selected.")

    try:
        parsed_data = parse_input(raw_data)
        validate_data(parsed_data, calculator)
        results = find_closest_populations(parsed_data, calculator)

        # Filter the results to include only the specified countries.
        filtered_results = [result for result in results if result['code'] in countries_to_show]

        return render_template(
            'admixture/analysis.html',
            results=filtered_results,
            user_components=parsed_data
        )
    except ValueError as e:
        return render_template('admixture/analysis.html', error=str(e))