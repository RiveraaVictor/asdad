# app/services/geo_converter.py
import json
import copy


class GeoConverter:
    """Converte dados de ancestralidade em um GeoJSON para visualização no mapa."""

    def convert(self, parsed_data: dict, model_config: dict) -> dict:
        """
        Gera um GeoJSON com as proporções ancestrais calculadas para cada região.
        """
        # Carrega a camada GeoJSON base para o modelo
        with open(model_config['geojson_file'], 'r', encoding='utf-8') as f:
            base_geojson = json.load(f)

        result_geojson = copy.deepcopy(base_geojson)
        component_to_region_map = model_config['region_mapping']

        # Itera sobre as regiões definidas no GeoJSON
        for feature in result_geojson['features']:
            region_name = feature['properties']['name']
            total_proportion = 0.0

            # Soma as proporções de todos os componentes que mapeiam para esta região
            for component_name, proportion in parsed_data.items():
                if component_to_region_map.get(component_name) == region_name:
                    total_proportion += proportion

            feature['properties']['total_proportion'] = total_proportion

        self._assign_colors_to_features(result_geojson)
        return result_geojson

    def _assign_colors_to_features(self, geojson_data: dict):
        """
        Atribui uma cor e opacidade a cada região com base na sua proporção.
        """
        proportions = [f['properties']['total_proportion'] for f in geojson_data['features']]
        max_proportion = max(proportions) if proportions else 0

        for feature in geojson_data['features']:
            proportion = feature['properties']['total_proportion']
            intensity = (proportion / max_proportion) if max_proportion > 0 else 0

            # Cor base azul forte
            base_r, base_g, base_b = 60, 130, 246
            # Cor final branca
            final_r, final_g, final_b = 255, 255, 255

            # Interpolação de cor: quanto maior a intensidade, mais perto da cor base
            r = int(final_r - (final_r - base_r) * intensity)
            g = int(final_g - (final_g - base_g) * intensity)
            b = int(final_b - (final_b - base_b) * intensity)

            feature['properties']['color'] = f"rgb({r},{g},{b})"
            # Opacidade mais forte para maiores proporções, garantindo visibilidade
            feature['properties']['opacity'] = 0.6 + (intensity * 0.3)