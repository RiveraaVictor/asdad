// app/static/js/admixture-map.js

document.addEventListener('alpine:init', () => {
    Alpine.data('admixtureApp', () => ({
        textInput: '',
        fileContent: '',
        map: null,
        popup: new mapboxgl.Popup({
            closeButton: false,
            closeOnClick: false
        }),
        mapboxToken: 'pk.eyJ1IjoiZ2FicmllbGFsbWVpZGFzYW50b3NtZWxvIiwiYSI6ImNtZHI0aHgycDBkbnMybXEzcTFzMjcxZTQifQ.wl33qoKDu0ARCryA6gOsqg', // Seu token Mapbox

        init() {
            this.initializeMap();
        },

        initializeMap() {
            if (!this.mapboxToken) {
                console.error("Token do Mapbox não fornecido.");
                document.getElementById('map').innerHTML = '<p class="p-4 text-red-600">Erro: Token do Mapbox não configurado.</p>';
                return;
            }
            mapboxgl.accessToken = this.mapboxToken;
            this.map = new mapboxgl.Map({
                container: 'map',
                style: 'mapbox://styles/mapbox/light-v11',
                center: [20, 30],
                zoom: 1.5,
                projection: 'globe'
            });
            this.map.on('load', () => {
                this.map.setFog({});
            });
        },

        handleFileSelect(file) {
            if (!file || file.type !== 'text/plain') {
                this.showAlert('Por favor, selecione um arquivo .txt', 'error');
                return;
            }
            const reader = new FileReader();
            reader.onload = (e) => {
                this.fileContent = e.target.result;
                this.textInput = this.fileContent; // Preenche o textarea com o conteúdo do arquivo
            };
            reader.readAsText(file);
        },

        async processData() {
            const dataToProcess = (this.fileContent || this.textInput).trim();
            if (!dataToProcess) {
                this.showAlert('Por favor, forneça os dados de ancestralidade.', 'warning');
                return;
            }

            const mapContainer = document.getElementById('map-container');
            mapContainer.classList.add('loading');

            try {
                const response = await fetch('/api/analyze', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ text_data: dataToProcess })
                });

                const result = await response.json();

                if (!response.ok) {
                    throw new Error(result.error || 'Erro desconhecido no processamento.');
                }

                this.updateMap(result.geojson);
                this.updateLegend(result.components, result.modelName);
                this.showAlert('Análise concluída com sucesso!', 'success');

            } catch (error) {
                console.error('Erro ao processar dados:', error);
                this.showAlert(error.message, 'error');
            } finally {
                mapContainer.classList.remove('loading');
            }
        },

        updateMap(geojson) {
            const source = this.map.getSource('admixture-regions');
            if (source) {
                source.setData(geojson);
            } else {
                this.map.addSource('admixture-regions', {
                    type: 'geojson',
                    data: geojson
                });

                this.map.addLayer({
                    id: 'regions-fill',
                    type: 'fill',
                    source: 'admixture-regions',
                    paint: {
                        'fill-color': ['get', 'color'],
                        'fill-opacity': ['get', 'opacity']
                    }
                }, 'building'); // Adiciona a camada abaixo dos edifícios para melhor visualização

                this.map.addLayer({
                    id: 'regions-outline',
                    type: 'line',
                    source: 'admixture-regions',
                    paint: {
                        'line-color': '#374151', // Um contorno cinza escuro
                        'line-width': 1,
                        'line-opacity': 0.5
                    }
                });

                // Adiciona interatividade de hover (popup)
                this.map.on('mouseenter', 'regions-fill', (e) => {
                    this.map.getCanvas().style.cursor = 'pointer';
                    const props = e.features[0].properties;
                    const percentage = (props.total_proportion * 100).toFixed(2);
                    const popupContent = `<strong>${props.name.replace(/_/g, ' ')}</strong><br>${percentage}%`;
                    this.popup.setLngLat(e.lngLat).setHTML(popupContent).addTo(this.map);
                });

                this.map.on('mouseleave', 'regions-fill', () => {
                    this.map.getCanvas().style.cursor = '';
                    this.popup.remove();
                });
            }
        },

        updateLegend(components, modelName) {
            const legendEl = document.getElementById('legend');
            const modelNameEl = document.getElementById('model-name');

            legendEl.innerHTML = ''; // Limpa a legenda anterior
            modelNameEl.textContent = modelName;

            if (!components || components.length === 0) {
                legendEl.innerHTML = '<p class="text-gray-500 text-sm">Nenhum componente para exibir.</p>';
                return;
            }

            components.forEach(([name, proportion]) => {
                const percentage = (proportion * 100).toFixed(2);
                if (proportion > 0) { // Mostra apenas componentes com valor > 0
                    const item = document.createElement('div');
                    item.className = 'flex justify-between items-center text-sm p-2 rounded-md hover:bg-gray-100';
                    item.innerHTML = `
                        <span class="text-gray-700">${name.replace(/_/g, ' ')}</span>
                        <span class="font-bold text-gray-900">${percentage}%</span>
                    `;
                    legendEl.appendChild(item);
                }
            });
        },

        showAlert(message, type = 'info') {
            // Uma função simples de alerta. Poderia ser substituída por uma biblioteca de notificações.
            alert(`[${type.toUpperCase()}] ${message}`);
        }
    }));
});