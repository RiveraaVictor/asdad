from flask import Flask, render_template_string

app = Flask(__name__)

@app.route('/')
def index():
    return render_template_string(r'''
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Análise de Ancestralidade Genética</title>
    <meta name="description" content="Visualize dados de ancestralidade genética com qualquer modelo Admixture em mapas interativos usando Mapbox GL JS">
    
    <!-- External Libraries -->
    <script src="https://cdn.tailwindcss.com"></script>
    <script defer src="https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/animate.css/4.1.1/animate.min.css">
    <link href="https://api.mapbox.com/mapbox-gl-js/v2.15.0/mapbox-gl.css" rel="stylesheet">
    <script src="https://api.mapbox.com/mapbox-gl-js/v2.15.0/mapbox-gl.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    
    <style>
        /* Clean UX + Glassmorphism + Cards Layout + Microinterações */
        :root {
            /* Light theme variables */
            --bg-primary: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 50%, #cbd5e1 100%);
            --bg-glass: rgba(255, 255, 255, 0.25);
            --border-glass: rgba(255, 255, 255, 0.3);
            --text-primary: #1e293b;
            --text-secondary: #475569;
            --text-muted: #64748b;
            --shadow-light: rgba(0, 0, 0, 0.1);
            --shadow-medium: rgba(0, 0, 0, 0.15);
            --card-bg: rgba(255, 255, 255, 0.7);
            --input-bg: rgba(255, 255, 255, 0.8);
            --btn-bg: linear-gradient(135deg, #3b82f6, #1d4ed8);
        }
        
        /* Dark theme variables */
         @media (prefers-color-scheme: dark) {
             :root {
                 --bg-primary: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #334155 100%);
                 --bg-glass: rgba(15, 23, 42, 0.4);
                 --border-glass: rgba(71, 85, 105, 0.3);
                 --text-primary: #ffffff;
                 --text-secondary: #f1f5f9;
                 --text-muted: #cbd5e1;
                 --shadow-light: rgba(0, 0, 0, 0.3);
                 --shadow-medium: rgba(0, 0, 0, 0.4);
                 --card-bg: rgba(15, 23, 42, 0.6);
                 --input-bg: rgba(30, 41, 59, 0.8);
                 --btn-bg: linear-gradient(135deg, #3b82f6, #1d4ed8);
             }
         }
        
        /* Manual theme override classes */
        .theme-light {
            --bg-primary: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 50%, #cbd5e1 100%);
            --bg-glass: rgba(255, 255, 255, 0.25);
            --border-glass: rgba(255, 255, 255, 0.3);
            --text-primary: #1e293b;
            --text-secondary: #475569;
            --text-muted: #64748b;
            --shadow-light: rgba(0, 0, 0, 0.1);
            --shadow-medium: rgba(0, 0, 0, 0.15);
            --card-bg: rgba(255, 255, 255, 0.7);
            --input-bg: rgba(255, 255, 255, 0.8);
            --btn-bg: linear-gradient(135deg, #3b82f6, #1d4ed8);
        }
        
        .theme-dark {
             --bg-primary: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #334155 100%);
             --bg-glass: rgba(15, 23, 42, 0.4);
             --border-glass: rgba(71, 85, 105, 0.3);
             --text-primary: #ffffff;
             --text-secondary: #f1f5f9;
             --text-muted: #cbd5e1;
             --shadow-light: rgba(0, 0, 0, 0.3);
             --shadow-medium: rgba(0, 0, 0, 0.4);
             --card-bg: rgba(15, 23, 42, 0.6);
             --input-bg: rgba(30, 41, 59, 0.8);
             --btn-bg: linear-gradient(135deg, #3b82f6, #1d4ed8);
         }
        
        * {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        }
        
        .clean-bg {
            background: var(--bg-primary);
            position: relative;
            min-height: 100vh;
            color: var(--text-primary);
            transition: all 0.3s ease;
        }
        
        .clean-bg::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: 
                radial-gradient(circle at 20% 80%, rgba(59, 130, 246, 0.05) 0%, transparent 50%),
                radial-gradient(circle at 80% 20%, rgba(139, 92, 246, 0.05) 0%, transparent 50%),
                radial-gradient(circle at 40% 40%, rgba(16, 185, 129, 0.05) 0%, transparent 50%);
            animation: gentle-float 15s ease-in-out infinite;
        }
        
        @keyframes gentle-float {
            0%, 100% { transform: translateY(0px) scale(1); }
            50% { transform: translateY(-10px) scale(1.02); }
        }
        
        .glass-card {
            background: var(--bg-glass);
            backdrop-filter: blur(16px) saturate(180%);
            border: 1px solid var(--border-glass);
            border-radius: 20px;
            box-shadow: 
                0 8px 32px var(--shadow-light),
                inset 0 1px 0 var(--border-glass);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative;
            overflow: hidden;
        }
        
        .glass-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
            transition: left 0.6s ease;
        }
        
        .glass-card:hover {
            transform: translateY(-8px);
            box-shadow: 
                0 20px 40px var(--shadow-medium),
                inset 0 1px 0 var(--border-glass);
            border-color: var(--border-glass);
        }
        
        .glass-card:hover::before {
            left: 100%;
        }
        
        .clean-title {
            font-weight: 700;
            letter-spacing: -0.025em;
            color: var(--text-primary);
        }
        
        .clean-subtitle {
            font-weight: 400;
            color: var(--text-muted);
            line-height: 1.6;
        }
        
        .btn-clean {
            background: var(--btn-bg);
            border: none;
            color: white;
            font-weight: 500;
            border-radius: 12px;
            padding: 12px 24px;
            transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
            box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
            position: relative;
            overflow: hidden;
        }
        
        .btn-clean::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
            transition: left 0.4s ease;
        }
        
        .btn-clean:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 20px rgba(59, 130, 246, 0.4);
        }
        
        .btn-clean:hover::before {
            left: 100%;
        }
        
        .btn-clean:active {
            transform: translateY(0px);
            box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
        }
        
        .feature-badge {
            background: var(--input-bg);
            backdrop-filter: blur(8px);
            border: 1px solid var(--border-glass);
            border-radius: 50px;
            padding: 8px 16px;
            font-size: 14px;
            font-weight: 500;
            color: var(--text-secondary);
            transition: all 0.2s ease;
        }
        
        .feature-badge:hover {
            background: var(--card-bg);
            transform: scale(1.05);
        }
        
        .drag-zone {
            border: 2px dashed #cbd5e1;
            border-radius: 16px;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            background: rgba(255, 255, 255, 0.5);
            backdrop-filter: blur(8px);
        }
        
        .drag-zone:hover {
            border-color: #3b82f6;
            background: rgba(59, 130, 246, 0.05);
            transform: scale(1.02);
        }
        
        .drag-zone.drag-over {
            border-color: #10b981;
            background: rgba(16, 185, 129, 0.1);
            transform: scale(1.05);
            box-shadow: 0 0 20px rgba(16, 185, 129, 0.3);
        }
        
        .progress-clean {
            background: rgba(255, 255, 255, 0.3);
            border-radius: 50px;
            overflow: hidden;
            backdrop-filter: blur(8px);
        }
        
        .progress-fill {
            background: linear-gradient(90deg, #3b82f6, #1d4ed8, #10b981);
            border-radius: 50px;
            transition: width 0.4s cubic-bezier(0.4, 0, 0.2, 1);
            box-shadow: 0 0 10px rgba(59, 130, 246, 0.5);
        }
        
        .map-card {
            border-radius: 20px;
            overflow: hidden;
            box-shadow: 0 12px 32px rgba(0, 0, 0, 0.1);
            transition: all 0.3s ease;
        }
        
        .map-card:hover {
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.15);
        }
        
        .control-btn {
            background: var(--card-bg);
            backdrop-filter: blur(8px);
            border: 1px solid var(--border-glass);
            color: var(--text-secondary);
            font-weight: 500;
            border-radius: 10px;
            padding: 8px 16px;
            font-size: 14px;
            transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
            box-shadow: 0 2px 8px var(--shadow-light);
        }
        
        .control-btn:hover {
            background: var(--input-bg);
            transform: translateY(-2px);
            box-shadow: 0 4px 12px var(--shadow-medium);
            color: var(--text-primary);
        }
        
        .control-btn:active {
            transform: translateY(0px);
        }
        
        .legend-item {
            background: var(--bg-glass);
            backdrop-filter: blur(8px);
            border: 1px solid var(--border-glass);
            border-radius: 12px;
            padding: 12px;
            transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
            margin-bottom: 8px;
            color: var(--text-secondary);
        }
        
        .legend-item:hover {
            background: var(--card-bg);
            transform: translateX(4px);
            box-shadow: 0 4px 12px var(--shadow-light);
        }
        
        .stats-card {
            background: var(--card-bg);
            backdrop-filter: blur(12px);
            border: 1px solid var(--border-glass);
            border-radius: 16px;
            padding: 16px;
            transition: all 0.3s ease;
            color: var(--text-primary);
        }
        
        .stats-card:hover {
            background: var(--input-bg);
            transform: translateY(-2px);
            box-shadow: 0 8px 20px var(--shadow-light);
        }
        
        .notification {
            background: var(--input-bg);
            backdrop-filter: blur(16px);
            border: 1px solid var(--border-glass);
            color: var(--text-primary);
        }
        
        /* Dark theme text overrides */
        .theme-dark,
        .theme-dark * {
            color: var(--text-primary) !important;
        }
        
        .theme-dark .clean-subtitle,
        .theme-dark .text-muted {
            color: var(--text-muted) !important;
        }
        
        .theme-dark input,
        .theme-dark textarea,
        .theme-dark select {
            background-color: var(--input-bg) !important;
            color: var(--text-primary) !important;
            border-color: var(--border-glass) !important;
        }
        
        .theme-dark input::placeholder,
        .theme-dark textarea::placeholder {
            color: var(--text-muted) !important;
        }
        
        .theme-dark .feature-badge,
        .theme-dark .control-btn,
        .theme-dark .legend-item {
            color: var(--text-secondary) !important;
        }
        
        .theme-dark .stats-card h3,
        .theme-dark .stats-card p,
        .theme-dark .glass-card h2,
        .theme-dark .glass-card h3,
        .theme-dark .glass-card p,
        .theme-dark .glass-card span {
             color: var(--text-primary) !important;
         }
         
         /* Theme Toggle Button Styles */
         #themeToggle {
             backdrop-filter: blur(20px);
             border-radius: 50px;
             min-width: 120px;
             font-weight: 600;
             letter-spacing: 0.025em;
         }
         
         #themeToggle:hover {
             backdrop-filter: blur(25px);
         }
         
         #themeToggle svg {
             flex-shrink: 0;
         }
         
         #themeToggle:hover svg {
             transform: rotate(15deg);
         }
         
         /* Responsive adjustments */
         @media (max-width: 768px) {
             #themeToggle {
                 min-width: auto;
                 padding: 12px 16px;
             }
             
             #themeToggle span {
                 display: none;
             }
         }
         
         @media (max-width: 480px) {
             #themeToggle {
                 top: 16px;
                 right: 16px;
                 padding: 10px;
             }
         }
         
         /* Popup Styles */
         .mapboxgl-popup {
             z-index: 1000;
         }
         
         .mapboxgl-popup-content {
             border-radius: 12px;
             box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
             border: 1px solid var(--border-glass);
             background: var(--card-bg);
             color: var(--text-primary);
             max-width: none !important;
         }
         
         .hover-popup .mapboxgl-popup-content {
             padding: 0;
             border-radius: 8px;
             box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
             animation: fadeInUp 0.2s ease-out;
         }
         
         .detailed-popup .mapboxgl-popup-content {
             padding: 0;
             border-radius: 12px;
             animation: fadeInScale 0.3s ease-out;
         }
         
         .mapboxgl-popup-tip {
             border-top-color: var(--card-bg) !important;
         }
         
         .mapboxgl-popup-close-button {
             color: var(--text-secondary);
             font-size: 20px;
             padding: 8px;
             border-radius: 50%;
             transition: all 0.2s ease;
         }
         
         .mapboxgl-popup-close-button:hover {
             background: var(--input-bg);
             color: var(--text-primary);
             transform: scale(1.1);
         }
         
         @keyframes fadeInUp {
             from {
                 opacity: 0;
                 transform: translateY(10px);
             }
             to {
                 opacity: 1;
                 transform: translateY(0);
             }
         }
         
         @keyframes fadeInScale {
             from {
                 opacity: 0;
                 transform: scale(0.95);
             }
             to {
                 opacity: 1;
                 transform: scale(1);
             }
         }
         
         /* Dark theme popup adjustments */
         .theme-dark .mapboxgl-popup-content {
             background: var(--card-bg) !important;
             color: var(--text-primary) !important;
             border-color: var(--border-glass) !important;
         }
         
         .theme-dark .mapboxgl-popup-tip {
             border-top-color: var(--card-bg) !important;
         }
         
         @media (prefers-color-scheme: dark) {
              .mapboxgl-popup-content {
                  background: var(--card-bg) !important;
                  color: var(--text-primary) !important;
                  border-color: var(--border-glass) !important;
              }
              
              .mapboxgl-popup-tip {
                  border-top-color: var(--card-bg) !important;
              }
          }
              
              .fixed.top-8.right-8 {
                 top: 1rem;
                 right: 1rem;
             }
         }
         
         @media (max-width: 480px) {
             .fixed.top-8.right-8 {
                 top: 0.75rem;
                 right: 0.75rem;
             }
             
             #themeToggle {
                 padding: 10px 12px;
             }
         }
        
        .input-clean {
            background: rgba(255, 255, 255, 0.8);
            backdrop-filter: blur(8px);
            border: 1px solid rgba(255, 255, 255, 0.3);
            border-radius: 12px;
            color: #1e293b;
            transition: all 0.2s ease;
        }
        
        .input-clean:focus {
            outline: none;
            border-color: #3b82f6;
            background: rgba(255, 255, 255, 0.9);
            box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
        }
        
        .input-clean::placeholder {
            color: #94a3b8;
        }
        
        .section-spacing {
            margin-bottom: 3rem;
        }
        
        .micro-animation {
            animation: gentle-pulse 3s ease-in-out infinite;
        }
        
        @keyframes gentle-pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.8; }
        }
        
        .card-grid {
            display: grid;
            gap: 2rem;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        }
        
        @media (min-width: 1024px) {
            .card-grid {
                grid-template-columns: repeat(2, 1fr);
            }
        }
        
        /* Animações de Background Genético */
        .genetic-background {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
            z-index: -1;
            overflow: hidden;
        }
        
        /* Fluxo Genético - Partículas em movimento */
        .genetic-flow {
            position: absolute;
            width: 100%;
            height: 100%;
        }
        
        .genetic-particle {
            position: absolute;
            width: 4px;
            height: 4px;
            background: linear-gradient(45deg, #3b82f6, #10b981);
            border-radius: 50%;
            opacity: 0.6;
            animation: geneticFlow 15s linear infinite;
        }
        
        .genetic-particle:nth-child(2n) {
            background: linear-gradient(45deg, #8b5cf6, #ec4899);
            animation-duration: 20s;
            animation-delay: -5s;
        }
        
        .genetic-particle:nth-child(3n) {
            background: linear-gradient(45deg, #f59e0b, #ef4444);
            animation-duration: 18s;
            animation-delay: -10s;
        }
        
        @keyframes geneticFlow {
            0% {
                transform: translateX(-100px) translateY(100vh) rotate(0deg);
                opacity: 0;
            }
            10% {
                opacity: 0.6;
            }
            90% {
                opacity: 0.6;
            }
            100% {
                transform: translateX(100vw) translateY(-100px) rotate(360deg);
                opacity: 0;
            }
        }
        
        /* Moléculas Flutuantes */
        .floating-molecules {
            position: absolute;
            width: 100%;
            height: 100%;
        }
        
        .molecule {
            position: absolute;
            width: 20px;
            height: 20px;
            border: 2px solid rgba(59, 130, 246, 0.3);
            border-radius: 50%;
            animation: floatMolecule 12s ease-in-out infinite;
        }
        
        .molecule::before {
            content: '';
            position: absolute;
            top: 50%;
            left: 50%;
            width: 8px;
            height: 8px;
            background: rgba(59, 130, 246, 0.5);
            border-radius: 50%;
            transform: translate(-50%, -50%);
        }
        
        .molecule:nth-child(2n) {
            border-color: rgba(139, 92, 246, 0.3);
            animation-duration: 15s;
            animation-delay: -3s;
        }
        
        .molecule:nth-child(2n)::before {
            background: rgba(139, 92, 246, 0.5);
        }
        
        .molecule:nth-child(3n) {
            border-color: rgba(16, 185, 129, 0.3);
            animation-duration: 18s;
            animation-delay: -6s;
        }
        
        .molecule:nth-child(3n)::before {
            background: rgba(16, 185, 129, 0.5);
        }
        
        @keyframes floatMolecule {
            0%, 100% {
                transform: translateY(0px) translateX(0px) rotate(0deg);
            }
            25% {
                transform: translateY(-30px) translateX(20px) rotate(90deg);
            }
            50% {
                transform: translateY(-10px) translateX(-15px) rotate(180deg);
            }
            75% {
                transform: translateY(-40px) translateX(10px) rotate(270deg);
            }
        }
        
        /* Hélice de DNA 3D - Modelo Pronto da Web */
        .dna-container {
            position: absolute;
            left: 8%;
            top: 15%;
            display: flex;
            justify-content: center;
            align-items: center;
            transform-style: preserve-3d;
            transform: rotateZ(-20deg);
            opacity: 0.15;
        }
        
        @keyframes dnaRotate {
            0% {
                transform: rotateX(0deg);
            }
            100% {
                transform: rotateX(360deg);
            }
        }
        
        .dna-strand {
            position: relative;
            width: 2px;
            height: 120px;
            border: 1px dotted rgba(59, 130, 246, 0.6);
            box-shadow: 0 0 15px rgba(59, 130, 246, 0.4);
            background: transparent;
            margin: 0px 8px;
            animation: dnaRotate 4s linear infinite;
        }
        
        .dna-strand::before {
            content: "";
            position: absolute;
            top: -3px;
            left: -6px;
            width: 12px;
            height: 12px;
            background: #3b82f6;
            border-radius: 50%;
            box-shadow: 0 0 15px #3b82f6;
        }
        
        .dna-strand::after {
            content: '';
            position: absolute;
            bottom: -3px;
            left: -6px;
            width: 12px;
            height: 12px;
            background: #10b981;
            border-radius: 50%;
            box-shadow: 0 0 12px #10b981;
        }
        
        .dna-strand:nth-child(1) { animation-delay: -0.2s; }
        .dna-strand:nth-child(2) { animation-delay: -0.4s; }
        .dna-strand:nth-child(3) { animation-delay: -0.6s; }
        .dna-strand:nth-child(4) { animation-delay: -0.8s; }
        .dna-strand:nth-child(5) { animation-delay: -1.0s; }
        .dna-strand:nth-child(6) { animation-delay: -1.2s; }
        .dna-strand:nth-child(7) { animation-delay: -1.4s; }
        .dna-strand:nth-child(8) { animation-delay: -1.6s; }
        .dna-strand:nth-child(9) { animation-delay: -1.8s; }
        .dna-strand:nth-child(10) { animation-delay: -2.0s; }
        .dna-strand:nth-child(11) { animation-delay: -2.2s; }
        .dna-strand:nth-child(12) { animation-delay: -2.4s; }
        
        /* Ondas Genéticas */
        .genetic-waves {
            position: absolute;
            width: 100%;
            height: 100%;
            background: 
                radial-gradient(ellipse at 20% 30%, rgba(59, 130, 246, 0.1) 0%, transparent 50%),
                radial-gradient(ellipse at 80% 70%, rgba(139, 92, 246, 0.1) 0%, transparent 50%),
                radial-gradient(ellipse at 50% 50%, rgba(16, 185, 129, 0.1) 0%, transparent 50%);
            animation: geneticWaves 25s ease-in-out infinite;
        }
        
        @keyframes geneticWaves {
            0%, 100% {
                background: 
                    radial-gradient(ellipse at 20% 30%, rgba(59, 130, 246, 0.1) 0%, transparent 50%),
                    radial-gradient(ellipse at 80% 70%, rgba(139, 92, 246, 0.1) 0%, transparent 50%),
                    radial-gradient(ellipse at 50% 50%, rgba(16, 185, 129, 0.1) 0%, transparent 50%);
            }
            25% {
                background: 
                    radial-gradient(ellipse at 60% 20%, rgba(59, 130, 246, 0.15) 0%, transparent 60%),
                    radial-gradient(ellipse at 30% 80%, rgba(139, 92, 246, 0.15) 0%, transparent 60%),
                    radial-gradient(ellipse at 70% 40%, rgba(16, 185, 129, 0.15) 0%, transparent 60%);
            }
            50% {
                background: 
                    radial-gradient(ellipse at 80% 60%, rgba(59, 130, 246, 0.2) 0%, transparent 70%),
                    radial-gradient(ellipse at 10% 40%, rgba(139, 92, 246, 0.2) 0%, transparent 70%),
                    radial-gradient(ellipse at 40% 80%, rgba(16, 185, 129, 0.2) 0%, transparent 70%);
            }
            75% {
                background: 
                    radial-gradient(ellipse at 30% 80%, rgba(59, 130, 246, 0.15) 0%, transparent 60%),
                    radial-gradient(ellipse at 70% 20%, rgba(139, 92, 246, 0.15) 0%, transparent 60%),
                    radial-gradient(ellipse at 20% 60%, rgba(16, 185, 129, 0.15) 0%, transparent 60%);
            }
        }
        

    </style>
</head>
<body class="clean-bg">
    <!-- Animações de Background Genético -->
    <div class="genetic-background">
        <!-- Ondas Genéticas -->
        <div class="genetic-waves"></div>
        
        <!-- Fluxo Genético - Partículas -->
        <div class="genetic-flow">
            <div class="genetic-particle" style="left: 10%; animation-delay: 0s;"></div>
            <div class="genetic-particle" style="left: 20%; animation-delay: -2s;"></div>
            <div class="genetic-particle" style="left: 30%; animation-delay: -4s;"></div>
            <div class="genetic-particle" style="left: 40%; animation-delay: -6s;"></div>
            <div class="genetic-particle" style="left: 50%; animation-delay: -8s;"></div>
            <div class="genetic-particle" style="left: 60%; animation-delay: -10s;"></div>
            <div class="genetic-particle" style="left: 70%; animation-delay: -12s;"></div>
            <div class="genetic-particle" style="left: 80%; animation-delay: -14s;"></div>
            <div class="genetic-particle" style="left: 90%; animation-delay: -16s;"></div>
            <div class="genetic-particle" style="left: 15%; animation-delay: -1s;"></div>
            <div class="genetic-particle" style="left: 25%; animation-delay: -3s;"></div>
            <div class="genetic-particle" style="left: 35%; animation-delay: -5s;"></div>
            <div class="genetic-particle" style="left: 45%; animation-delay: -7s;"></div>
            <div class="genetic-particle" style="left: 55%; animation-delay: -9s;"></div>
            <div class="genetic-particle" style="left: 65%; animation-delay: -11s;"></div>
            <div class="genetic-particle" style="left: 75%; animation-delay: -13s;"></div>
            <div class="genetic-particle" style="left: 85%; animation-delay: -15s;"></div>
            <div class="genetic-particle" style="left: 95%; animation-delay: -17s;"></div>
        </div>
        
        <!-- Moléculas Flutuantes -->
        <div class="floating-molecules">
            <div class="molecule" style="left: 5%; top: 10%;"></div>
            <div class="molecule" style="left: 15%; top: 30%;"></div>
            <div class="molecule" style="left: 25%; top: 60%;"></div>
            <div class="molecule" style="left: 35%; top: 20%;"></div>
            <div class="molecule" style="left: 45%; top: 80%;"></div>
            <div class="molecule" style="left: 55%; top: 40%;"></div>
            <div class="molecule" style="left: 65%; top: 70%;"></div>
            <div class="molecule" style="left: 75%; top: 15%;"></div>
            <div class="molecule" style="left: 85%; top: 50%;"></div>
            <div class="molecule" style="left: 95%; top: 85%;"></div>
            <div class="molecule" style="left: 10%; top: 45%;"></div>
            <div class="molecule" style="left: 30%; top: 75%;"></div>
            <div class="molecule" style="left: 50%; top: 25%;"></div>
            <div class="molecule" style="left: 70%; top: 55%;"></div>
            <div class="molecule" style="left: 90%; top: 35%;"></div>
        </div>
        
        <!-- Hélice de DNA 3D - Modelo Pronto Principal -->
        <div class="dna-container">
            <div class="dna-strand"></div>
            <div class="dna-strand"></div>
            <div class="dna-strand"></div>
            <div class="dna-strand"></div>
            <div class="dna-strand"></div>
            <div class="dna-strand"></div>
            <div class="dna-strand"></div>
            <div class="dna-strand"></div>
            <div class="dna-strand"></div>
            <div class="dna-strand"></div>
            <div class="dna-strand"></div>
            <div class="dna-strand"></div>
        </div>
        
        <!-- Hélice de DNA 3D - Modelo Pronto Secundária -->
        <div class="dna-container" style="right: 8%; left: auto; top: 25%; opacity: 0.08; transform: scale(0.8) rotateY(45deg) rotateZ(-20deg);">
            <div class="dna-strand"></div>
            <div class="dna-strand"></div>
            <div class="dna-strand"></div>
            <div class="dna-strand"></div>
            <div class="dna-strand"></div>
            <div class="dna-strand"></div>
            <div class="dna-strand"></div>
            <div class="dna-strand"></div>
            <div class="dna-strand"></div>
            <div class="dna-strand"></div>
            <div class="dna-strand"></div>
            <div class="dna-strand"></div>
        </div>

        <!-- Hélice de DNA 3D - Canto Superior Direito -->
        <div class="dna-container" style="right: 3%; left: auto; top: 5%; opacity: 0.06; transform: scale(0.6) rotateY(120deg) rotateZ(30deg);">
            <div class="dna-strand"></div>
            <div class="dna-strand"></div>
            <div class="dna-strand"></div>
            <div class="dna-strand"></div>
            <div class="dna-strand"></div>
            <div class="dna-strand"></div>
            <div class="dna-strand"></div>
            <div class="dna-strand"></div>
            <div class="dna-strand"></div>
            <div class="dna-strand"></div>
            <div class="dna-strand"></div>
            <div class="dna-strand"></div>
        </div>

        <!-- Hélice de DNA 3D - Canto Inferior Esquerdo -->
        <div class="dna-container" style="left: 3%; top: auto; bottom: 10%; opacity: 0.05; transform: scale(0.7) rotateY(-60deg) rotateZ(45deg);">
            <div class="dna-strand"></div>
            <div class="dna-strand"></div>
            <div class="dna-strand"></div>
            <div class="dna-strand"></div>
            <div class="dna-strand"></div>
            <div class="dna-strand"></div>
            <div class="dna-strand"></div>
            <div class="dna-strand"></div>
            <div class="dna-strand"></div>
            <div class="dna-strand"></div>
            <div class="dna-strand"></div>
            <div class="dna-strand"></div>
        </div>

        <!-- Hélice de DNA 3D - Centro Direito -->
        <div class="dna-container" style="right: 15%; left: auto; top: 50%; opacity: 0.04; transform: scale(0.5) rotateY(180deg) rotateZ(-45deg);">
            <div class="dna-strand"></div>
            <div class="dna-strand"></div>
            <div class="dna-strand"></div>
            <div class="dna-strand"></div>
            <div class="dna-strand"></div>
            <div class="dna-strand"></div>
            <div class="dna-strand"></div>
            <div class="dna-strand"></div>
            <div class="dna-strand"></div>
            <div class="dna-strand"></div>
            <div class="dna-strand"></div>
            <div class="dna-strand"></div>
        </div>

        <!-- Hélice de DNA 3D - Canto Inferior Direito -->
        <div class="dna-container" style="right: 5%; left: auto; bottom: 5%; opacity: 0.07; transform: scale(0.9) rotateY(-90deg) rotateZ(60deg);">
            <div class="dna-strand"></div>
            <div class="dna-strand"></div>
            <div class="dna-strand"></div>
            <div class="dna-strand"></div>
            <div class="dna-strand"></div>
            <div class="dna-strand"></div>
            <div class="dna-strand"></div>
            <div class="dna-strand"></div>
            <div class="dna-strand"></div>
            <div class="dna-strand"></div>
            <div class="dna-strand"></div>
            <div class="dna-strand"></div>
        </div>
    </div>
    
    <div x-data="admixtureApp()" class="min-h-screen relative z-10">
        <!-- Hero Section -->
        <div class="container mx-auto px-6 py-16">
            <div class="text-center animate__animated animate__fadeInDown section-spacing">
                <!-- Theme Toggle Button -->
                <div class="fixed top-8 right-8 z-50">
                    <button id="themeToggle" class="control-btn flex items-center gap-3 px-5 py-3 shadow-lg hover:shadow-xl transition-all duration-300 hover:scale-105" title="Alternar tema">
                        <svg id="sunIcon" class="w-5 h-5 transition-transform duration-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z"></path>
                        </svg>
                        <svg id="moonIcon" class="w-5 h-5 hidden transition-transform duration-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z"></path>
                        </svg>
                        <span id="themeText" class="font-medium text-sm">Escuro</span>
                    </button>
                </div>
                
                <h1 class="clean-title text-5xl md:text-6xl mb-6 micro-animation">
                    Análise de Ancestralidade Genética
                </h1>
                <p class="clean-subtitle text-xl md:text-2xl mb-8 max-w-4xl mx-auto">
                    Visualize seus dados de ancestralidade com qualquer modelo Admixture em um mapa mundial interativo.
                    Uma experiência limpa e intuitiva para explorar sua herança genética.
                </p>
                <div class="flex justify-center gap-4 flex-wrap">
                    <span class="feature-badge">
                        <svg class="w-4 h-4 inline mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3.055 11H5a2 2 0 012 2v1a2 2 0 002 2 2 2 0 012 2v2.945M8 3.935V5.5A2.5 2.5 0 0010.5 8h.5a2 2 0 012 2 2 2 0 104 0 2 2 0 012-2h1.064M15 20.488V18a2 2 0 012-2h3.064M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                        </svg>
                        Suporte Universal
                    </span>
                    <span class="feature-badge">
                        <svg class="w-4 h-4 inline mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"></path>
                        </svg>
                        Detecção Automática
                    </span>
                    <span class="feature-badge">
                        <svg class="w-4 h-4 inline mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 21a4 4 0 01-4-4V5a2 2 0 012-2h4a2 2 0 012 2v12a4 4 0 01-4 4zM21 5a2 2 0 00-2-2h-4a2 2 0 00-2 2v12a4 4 0 004 4h4a2 2 0 002-2V5z"></path>
                        </svg>
                        Cores Dinâmicas
                    </span>
                </div>
            </div>
        </div>

        <!-- Cards Section -->
        <div class="container mx-auto px-6 section-spacing">
            <div class="card-grid">
                <!-- File Upload Card -->
                <div class="glass-card p-8 animate__animated animate__fadeInLeft">
                    <div class="flex items-center mb-6">
                        <div class="w-12 h-12 bg-gradient-to-br from-blue-500 to-blue-600 rounded-xl flex items-center justify-center mr-4">
                            <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"></path>
                            </svg>
                        </div>
                        <h2 class="text-2xl font-semibold text-gray-800">
                            Upload de Arquivo
                        </h2>
                    </div>
                    
                    <div 
                        @dragover.prevent="dragOver = true"
                        @dragleave.prevent="dragOver = false"
                        @drop.prevent="handleFileDrop($event)"
                        :class="{'drag-over': dragOver}"
                        class="drag-zone p-8 text-center cursor-pointer"
                        @click="$refs.fileInput.click()">
                        
                        <div class="text-gray-600">
                            <svg class="w-16 h-16 mx-auto mb-4 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
                            </svg>
                            <p class="text-lg font-medium mb-2">Arraste seu arquivo .txt aqui</p>
                            <p class="text-sm text-gray-500">ou clique para selecionar</p>
                        </div>
                        
                        <input 
                            type="file" 
                            accept=".txt" 
                            x-ref="fileInput"
                            @change="handleFileUpload($event.target.files[0])"
                            class="hidden">
                    </div>
                    
                    <!-- Upload Progress -->
                    <div x-show="uploading" class="mt-6">
                        <div class="progress-clean h-3 mb-2">
                            <div class="progress-fill h-3" :style="`width: ${uploadProgress}%`"></div>
                        </div>
                        <p class="text-gray-600 text-sm font-medium" x-text="uploadStatus"></p>
                    </div>
                </div>

                <!-- Text Input Card -->
                <div class="glass-card p-8 animate__animated animate__fadeInRight">
                    <div class="flex items-center mb-6">
                        <div class="w-12 h-12 bg-gradient-to-br from-green-500 to-green-600 rounded-xl flex items-center justify-center mr-4">
                            <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"></path>
                            </svg>
                        </div>
                        <h2 class="text-2xl font-semibold text-gray-800">
                            Entrada Direta
                        </h2>
                    </div>
                    
                    <textarea 
                        x-model="textInput"
                        placeholder="Cole aqui os dados do seu arquivo Admixture...\n\nExemplo:\nIndividual1 0.25 0.35 0.15 0.25\nIndividual2 0.30 0.20 0.25 0.25"
                        class="input-clean w-full h-40 p-4 resize-none"
                    ></textarea>
                    
                    <button 
                        @click="processTextData()"
                        class="mt-4 w-full btn-clean flex items-center justify-center">
                        <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"></path>
                        </svg>
                        Processar Dados
                    </button>
                </div>
            </div>
        </div>

        <!-- Map Section -->
        <div class="container mx-auto px-6 section-spacing">
            <div class="glass-card p-8 animate__animated animate__fadeInUp">
                <div class="flex flex-col lg:flex-row gap-8">
                    <!-- Map -->
                    <div class="lg:w-3/4">
                        <div class="flex items-center mb-6">
                            <div class="w-12 h-12 bg-gradient-to-br from-purple-500 to-purple-600 rounded-xl flex items-center justify-center mr-4">
                                <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 20l-5.447-2.724A1 1 0 013 16.382V5.618a1 1 0 011.447-.894L9 7m0 13l6-3m-6 3V7m6 10l4.553 2.276A1 1 0 0021 18.382V7.618a1 1 0 00-.553-.894L15 4m0 13V4m0 0L9 7"></path>
                                </svg>
                            </div>
                            <h2 class="text-3xl font-semibold text-gray-800">
                                Mapa de Ancestralidade
                            </h2>
                        </div>
                        <div id="map" class="map-card h-96 lg:h-[500px] bg-gray-100"></div>
                        
                        <!-- Map Controls -->
                        <div class="flex flex-wrap gap-3 mt-6">
                            <button id="resetViewBtn" class="control-btn flex items-center">
                                <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"></path>
                                </svg>
                                Resetar Vista
                            </button>
                            <button id="toggleClustersBtn" class="control-btn flex items-center">
                                <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"></path>
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"></path>
                                </svg>
                                Alternar Clusters
                            </button>
                            <button id="fullscreenBtn" class="control-btn flex items-center">
                                <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 8V4m0 0h4M4 4l5 5m11-1V4m0 0h-4m4 0l-5 5M4 16v4m0 0h4m-4 0l5-5m11 5l-5-5m5 5v-4m0 4h-4"></path>
                                </svg>
                                Tela Cheia
                            </button>
                            <button id="exportBtn" class="control-btn flex items-center">
                                <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"></path>
                                </svg>
                                Exportar
                            </button>
                            <select id="styleSelect" class="control-btn cursor-pointer">
                                <option value="mapbox://styles/mapbox/streets-v12" selected>Streets</option>
                                <option value="mapbox://styles/mapbox/satellite-v9">Satellite</option>
                                <option value="mapbox://styles/mapbox/light-v11">Light</option>
                                <option value="mapbox://styles/mapbox/dark-v11">Dark</option>
                            </select>
                        </div>
                    </div>
                    
                    <!-- Sidebar Cards -->
                    <div class="lg:w-1/4 space-y-6">
                        <!-- Legend Card -->
                        <div class="stats-card">
                            <div class="flex items-center mb-4">
                                <div class="w-8 h-8 bg-gradient-to-br from-pink-500 to-pink-600 rounded-lg flex items-center justify-center mr-3">
                                    <svg class="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 21a4 4 0 01-4-4V5a2 2 0 012-2h4a2 2 0 012 2v12a4 4 0 01-4 4zM21 5a2 2 0 00-2-2h-4a2 2 0 00-2 2v12a4 4 0 004 4h4a2 2 0 002-2V5z"></path>
                                    </svg>
                                </div>
                                <h3 class="text-lg font-semibold text-gray-800">
                                    Legenda
                                </h3>
                            </div>
                            <div id="legend">
                                <p class="text-gray-500 text-sm">Carregue dados para ver a legenda</p>
                            </div>
                        </div>
                        
                        <!-- Statistics Card -->
                        <div class="stats-card">
                            <div class="flex items-center mb-4">
                                <div class="w-8 h-8 bg-gradient-to-br from-indigo-500 to-indigo-600 rounded-lg flex items-center justify-center mr-3">
                                    <svg class="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"></path>
                                    </svg>
                                </div>
                                <h3 class="text-lg font-semibold text-gray-800">
                                    Estatísticas
                                </h3>
                            </div>
                            <div id="statistics">
                                <p class="text-gray-500 text-sm">Carregue dados para ver estatísticas</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script>
        // Alpine.js data
        function admixtureApp() {
            return {
                dragOver: false,
                uploading: false,
                uploadProgress: 0,
                uploadStatus: 'Processando...',
                textInput: '',
                
                handleFileDrop(event) {
                    this.dragOver = false;
                    const files = event.dataTransfer.files;
                    if (files.length > 0) {
                        this.handleFileUpload(files[0]);
                    }
                },
                
                handleFileUpload(file) {
                    if (!file.name.endsWith('.txt')) {
                        this.showNotification('Por favor, selecione um arquivo .txt', 'error');
                        return;
                    }
                    
                    this.uploading = true;
                    this.uploadProgress = 0;
                    
                    const reader = new FileReader();
                    reader.onload = (e) => {
                        this.uploadProgress = 100;
                        this.uploadStatus = 'Arquivo carregado com sucesso!';
                        setTimeout(() => {
                            this.uploading = false;
                            processAdmixtureData(e.target.result);
                        }, 500);
                    };
                    
                    reader.readAsText(file);
                },
                
                processTextData() {
                    if (!this.textInput.trim()) {
                        this.showNotification('Por favor, cole os dados Admixture', 'warning');
                        return;
                    }
                    processAdmixtureData(this.textInput);
                },
                
                showNotification(message, type = 'info') {
                    const notification = document.createElement('div');
                     const iconColor = type === 'error' ? 'text-red-500' :
                                      type === 'warning' ? 'text-yellow-500' :
                                      type === 'success' ? 'text-green-500' :
                                      'text-blue-500';
                     
                     const iconPath = type === 'error' ? 'M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z' :
                                     type === 'warning' ? 'M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.732-.833-2.464 0L3.34 16.5c-.77.833.192 2.5 1.732 2.5z' :
                                     type === 'success' ? 'M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z' :
                                     'M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z';
                     
                     notification.className = `notification fixed top-4 right-4 z-50 p-4 animate__animated animate__fadeInRight`;
                     notification.innerHTML = `
                         <div class="flex items-center">
                             <div class="${iconColor} mr-3">
                                 <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                     <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="${iconPath}"></path>
                                 </svg>
                             </div>
                             <span class="font-medium">${message}</span>
                             <button class="ml-4 text-gray-400 hover:text-gray-600 transition-colors" onclick="this.parentElement.parentElement.remove()">
                                 <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                     <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
                                 </svg>
                             </button>
                         </div>
                     `;
                    
                    document.body.appendChild(notification);
                    
                    setTimeout(() => {
                        if (notification.parentElement) {
                            notification.classList.add('animate__fadeOutRight');
                            setTimeout(() => notification.remove(), 500);
                        }
                    }, 5000);
                }
            }
        }
        
        // Global variables
        let map;
        let admixtureData = null;
        let currentModel = null;
        
        // Token Mapbox configurado
        const MAPBOX_TOKEN = 'pk.eyJ1IjoiZ2FicmllbGFsbWVpZGFzYW50b3NtZWxvIiwiYSI6ImNtZHI0aHgycDBkbnMybXEzcTFzMjcxZTQifQ.wl33qoKDu0ARCryA6gOsqg';
        
        // Base color palette
        const baseColors = [
            '#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6', '#06b6d4',
            '#84cc16', '#f97316', '#ec4899', '#6366f1', '#14b8a6', '#eab308'
        ];
        
        function generateColorPalette(componentCount) {
            const colors = [];
            for (let i = 0; i < componentCount; i++) {
                if (i < baseColors.length) {
                    colors.push(baseColors[i]);
                } else {
                    const hue = (i * 137.508) % 360;
                    const saturation = 65 + (i % 3) * 10;
                    const lightness = 55 + (i % 4) * 8;
                    colors.push(`hsl(${hue}, ${saturation}%, ${lightness}%)`);
                }
            }
            return colors;
        }
        
        // Initialize application
        document.addEventListener('DOMContentLoaded', function() {
            initializeMap();
            setupEventListeners();
        });
        
        function initializeMap() {
            console.log('🗺️ Testando conectividade com Mapbox...');
            console.log('Token:', MAPBOX_TOKEN.substring(0, 20) + '...');
            
            // Test token validity
            fetch(`https://api.mapbox.com/geocoding/v5/mapbox.places/test.json?access_token=${MAPBOX_TOKEN}`)
                .then(response => {
                    console.log('📡 Status da API Mapbox:', response.status);
                    if (response.status === 401) {
                        console.error('❌ Token Mapbox inválido ou expirado');
                        showMapboxError('Token inválido ou expirado');
                        return;
                    }
                    if (response.status !== 200) {
                        console.error('❌ Erro na API Mapbox:', response.status);
                        showMapboxError(`Erro da API: ${response.status}`);
                        return;
                    }
                    
                    console.log('✅ Token Mapbox válido, inicializando mapa...');
                    initializeMapboxMap();
                })
                .catch(error => {
                    console.error('❌ Erro de conectividade:', error);
                    showMapboxError('Erro de conectividade com a internet');
                });
        }
        
        function showMapboxError(errorMessage) {
            const mapContainer = document.getElementById('map');
            mapContainer.innerHTML = `
                <div class="flex items-center justify-center h-full bg-gradient-to-br from-red-50 to-red-100 rounded-xl">
                    <div class="text-center p-8">
                        <div class="bg-red-100 border border-red-400 text-red-700 px-6 py-4 rounded-lg mb-4">
                                <div class="flex items-center justify-center mb-2">
                                    <svg class="w-6 h-6 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                                    </svg>
                                    <strong>Erro de Conexão Mapbox</strong>
                                </div>
                                <p class="text-sm">${errorMessage}</p>
                            </div>
                        <div class="text-sm text-gray-600 space-y-1">
                            <p class="flex items-center">
                                <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
                                </svg>
                                Possíveis soluções:
                            </p>
                            <p>• Verifique sua conexão com a internet</p>
                            <p>• Confirme se o token Mapbox está correto</p>
                            <p>• Verifique se o token não expirou</p>
                            <p>• Tente recarregar a página</p>
                        </div>
                        <button onclick="location.reload()" class="mt-4 bg-red-500 hover:bg-red-600 text-white px-4 py-2 rounded-lg transition-colors flex items-center">
                            <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"></path>
                            </svg>
                            Tentar Novamente
                        </button>
                    </div>
                </div>
            `;
        }
        
        function initializeMapboxMap() {
            mapboxgl.accessToken = MAPBOX_TOKEN;
            
            try {
                map = new mapboxgl.Map({
                    container: 'map',
                    style: 'mapbox://styles/mapbox/streets-v12',
                    center: [0, 20],
                    zoom: 2,
                    projection: 'globe',
                    preserveDrawingBuffer: true
                });
                
                map.on('load', function() {
                    console.log('✅ Mapa Mapbox carregado com sucesso!');
                    
                    map.setFog({
                        'range': [0.8, 8],
                        'color': '#ffffff',
                        'horizon-blend': 0.5
                    });
                    
                    map.addControl(new mapboxgl.NavigationControl());
                    map.addControl(new mapboxgl.FullscreenControl());
                });
                
                map.on('error', function(e) {
                    console.error('❌ Erro no mapa Mapbox:', e);
                    showMapboxError('Erro ao carregar o mapa');
                });
                
            } catch (error) {
                console.error('❌ Erro ao criar mapa Mapbox:', error);
                showMapboxError('Erro ao inicializar o mapa');
            }
        }
        
        function setupEventListeners() {
            console.log('✅ Event listeners configurados via Alpine.js');
            
            // Map controls
            document.getElementById('resetViewBtn').addEventListener('click', resetMapView);
            document.getElementById('toggleClustersBtn').addEventListener('click', toggleClusters);
            document.getElementById('fullscreenBtn').addEventListener('click', toggleFullscreen);
            document.getElementById('exportBtn').addEventListener('click', exportMap);
            document.getElementById('styleSelect').addEventListener('change', changeMapStyle);
        }
        
        function processAdmixtureData(data) {
            console.log('🧬 Processando dados Admixture...');
            
            const lines = data.trim().split('\n').filter(line => line.trim());
            if (lines.length === 0) {
                showAlert('Dados inválidos', 'error');
                return;
            }
            
            const processedData = [];
            let componentCount = 0;
            
            lines.forEach((line, index) => {
                const parts = line.trim().split(/\s+/);
                if (parts.length < 2) return;
                
                const individual = parts[0];
                const proportions = parts.slice(1).map(p => parseFloat(p));
                
                if (index === 0) {
                    componentCount = proportions.length;
                }
                
                processedData.push({
                    individual,
                    proportions
                });
            });
            
            admixtureData = processedData;
            currentModel = `K${componentCount}`;
            
            console.log(`✅ Dados processados: ${processedData.length} indivíduos, ${componentCount} componentes`);
            
            visualizeOnMap(processedData, componentCount);
            updateLegend(componentCount);
            updateStatistics(processedData, componentCount);
        }
        
        function visualizeOnMap(data, componentCount) {
            if (!map) return;
            
            const colors = generateColorPalette(componentCount);
            const features = [];
            
            data.forEach((item, index) => {
                const coords = getRandomCoordinates();
                
                features.push({
                    type: 'Feature',
                    properties: {
                        individual: item.individual,
                        proportions: item.proportions,
                        colors: colors,
                        componentCount: componentCount
                    },
                    geometry: {
                        type: 'Point',
                        coordinates: coords
                    }
                });
            });
            
            const geojson = {
                type: 'FeatureCollection',
                features: features
            };
            
            if (map.getSource('admixture-data')) {
                map.getSource('admixture-data').setData(geojson);
            } else {
                map.addSource('admixture-data', {
                    type: 'geojson',
                    data: geojson,
                    cluster: true,
                    clusterMaxZoom: 14,
                    clusterRadius: 50
                });
                
                // Cluster circles
                map.addLayer({
                    id: 'clusters',
                    type: 'circle',
                    source: 'admixture-data',
                    filter: ['has', 'point_count'],
                    paint: {
                        'circle-color': [
                            'step',
                            ['get', 'point_count'],
                            '#3b82f6',
                            100, '#10b981',
                            750, '#f59e0b'
                        ],
                        'circle-radius': [
                            'step',
                            ['get', 'point_count'],
                            20, 100, 30, 750, 40
                        ]
                    }
                });
                
                // Cluster count
                map.addLayer({
                    id: 'cluster-count',
                    type: 'symbol',
                    source: 'admixture-data',
                    filter: ['has', 'point_count'],
                    layout: {
                        'text-field': '{point_count_abbreviated}',
                        'text-font': ['DIN Offc Pro Medium', 'Arial Unicode MS Bold'],
                        'text-size': 12
                    }
                });
                
                // Individual points
                map.addLayer({
                    id: 'unclustered-point',
                    type: 'circle',
                    source: 'admixture-data',
                    filter: ['!', ['has', 'point_count']],
                    paint: {
                        'circle-color': colors[0],
                        'circle-radius': 8,
                        'circle-stroke-width': 2,
                        'circle-stroke-color': '#fff'
                    }
                });
                
                // Create popup instance for hover tooltips
                let hoverPopup = null;
                
                // Add hover tooltips for quick information
                map.on('mouseenter', 'unclustered-point', (e) => {
                    map.getCanvas().style.cursor = 'pointer';
                    
                    const coordinates = e.features[0].geometry.coordinates.slice();
                    const properties = e.features[0].properties;
                    
                    // Create quick tooltip content
                    const proportions = JSON.parse(properties.proportions || '[]');
                    const colors = JSON.parse(properties.colors || '[]');
                    const individual = properties.individual || 'Amostra';
                    
                    // Find dominant component
                    const maxProportion = Math.max(...proportions);
                    const dominantIndex = proportions.indexOf(maxProportion);
                    const dominantPercentage = (maxProportion * 100).toFixed(1);
                    
                    const tooltipContent = `
                        <div class="p-3 text-sm bg-white rounded-lg shadow-lg border">
                            <div class="font-semibold text-blue-600 mb-1">${individual}</div>
                            <div class="flex items-center text-gray-700">
                                <div class="w-3 h-3 rounded-full mr-2" style="background-color: ${colors[dominantIndex] || '#666'}"></div>
                                <span>Componente ${dominantIndex + 1}: ${dominantPercentage}%</span>
                            </div>
                            <div class="text-xs text-gray-500 mt-2 flex items-center">
                                <svg class="w-3 h-3 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 15l-2 5L9 9l11 4-5 2zm0 0l5 5M7.188 2.239l.777 2.897M5.136 7.965l-2.898-.777M13.95 4.05l-2.122 2.122m-5.657 5.656l-2.12 2.122"></path>
                                </svg>
                                Clique para detalhes completos
                            </div>
                        </div>
                    `;
                    
                    // Remove existing hover popup
                    if (hoverPopup) {
                        hoverPopup.remove();
                    }
                    
                    // Create new hover popup
                    hoverPopup = new mapboxgl.Popup({
                        closeButton: false,
                        closeOnClick: false,
                        className: 'hover-popup',
                        offset: [0, -10]
                    })
                    .setLngLat(coordinates)
                    .setHTML(tooltipContent)
                    .addTo(map);
                });
                
                // Remove hover popup when mouse leaves
                map.on('mouseleave', 'unclustered-point', () => {
                    map.getCanvas().style.cursor = '';
                    if (hoverPopup) {
                        hoverPopup.remove();
                        hoverPopup = null;
                    }
                });
                
                // Add click events for detailed popups
                map.on('click', 'unclustered-point', (e) => {
                    // Remove hover popup when clicking
                    if (hoverPopup) {
                        hoverPopup.remove();
                        hoverPopup = null;
                    }
                    
                    const coordinates = e.features[0].geometry.coordinates.slice();
                    const properties = e.features[0].properties;
                    
                    // Ensure popup appears over the feature
                    while (Math.abs(e.lngLat.lng - coordinates[0]) > 180) {
                        coordinates[0] += e.lngLat.lng > coordinates[0] ? 360 : -360;
                    }
                    
                    // Create detailed popup content
                    const proportions = JSON.parse(properties.proportions || '[]');
                    const colors = JSON.parse(properties.colors || '[]');
                    const individual = properties.individual || 'Amostra';
                    
                    let popupContent = `
                        <div class="p-4 min-w-80 max-w-96">
                            <div class="flex items-center justify-between mb-3">
                                <h3 class="font-bold text-lg text-blue-600">${individual}</h3>
                                <div class="flex items-center text-xs text-gray-500">
                                    <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"></path>
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"></path>
                                    </svg>
                                    ${coordinates[1].toFixed(4)}°, ${coordinates[0].toFixed(4)}°
                                </div>
                            </div>
                            
                            <div class="space-y-3">
                                <div>
                                    <h4 class="font-semibold text-sm mb-3 text-gray-700 flex items-center">
                                        <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"></path>
                                        </svg>
                                        Composição Ancestral Detalhada
                                    </h4>
                                    <div class="space-y-2">
                    `;
                    
                    // Sort components by percentage for better visualization
                    const sortedComponents = proportions.map((prop, index) => ({ prop, index }))
                        .sort((a, b) => b.prop - a.prop);
                    
                    sortedComponents.forEach(({ prop, index }) => {
                        const percentage = (prop * 100).toFixed(1);
                        const color = colors[index] || '#666';
                        const barWidth = Math.max(prop * 100, 1); // Minimum 1% for visibility
                        
                        popupContent += `
                            <div class="space-y-1">
                                <div class="flex items-center justify-between text-sm">
                                    <div class="flex items-center">
                                        <div class="w-4 h-4 rounded-full mr-3 border border-gray-200" style="background-color: ${color}"></div>
                                        <span class="font-medium text-gray-700">Componente ${index + 1}</span>
                                    </div>
                                    <span class="font-bold text-gray-800">${percentage}%</span>
                                </div>
                                <div class="w-full bg-gray-200 rounded-full h-2.5">
                                    <div class="h-2.5 rounded-full transition-all duration-500 ease-out" 
                                         style="background-color: ${color}; width: ${barWidth}%"></div>
                                </div>
                            </div>
                        `;
                    });
                    
                    // Add summary statistics
                    const totalComponents = proportions.length;
                    const maxComponent = Math.max(...proportions);
                    const diversity = 1 - proportions.reduce((sum, p) => sum + p * p, 0); // Simpson's diversity index
                    
                    popupContent += `
                                    </div>
                                </div>
                                
                                <div class="pt-3 border-t border-gray-200">
                                    <h5 class="font-semibold text-sm mb-2 text-gray-700">Estatísticas da Amostra</h5>
                                    <div class="grid grid-cols-2 gap-3 text-xs">
                                        <div class="bg-blue-50 p-2 rounded">
                                            <div class="font-semibold text-blue-800">Componentes</div>
                                            <div class="text-blue-600">${totalComponents}</div>
                                        </div>
                                        <div class="bg-green-50 p-2 rounded">
                                            <div class="font-semibold text-green-800">Máx. Ancestralidade</div>
                                            <div class="text-green-600">${(maxComponent * 100).toFixed(1)}%</div>
                                        </div>
                                        <div class="bg-purple-50 p-2 rounded">
                                            <div class="font-semibold text-purple-800">Diversidade</div>
                                            <div class="text-purple-600">${diversity.toFixed(3)}</div>
                                        </div>
                                        <div class="bg-orange-50 p-2 rounded">
                                            <div class="font-semibold text-orange-800">Modelo</div>
                                            <div class="text-orange-600">K=${totalComponents}</div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    `;
                    
                    new mapboxgl.Popup({
                        maxWidth: '400px',
                        className: 'detailed-popup'
                    })
                        .setLngLat(coordinates)
                        .setHTML(popupContent)
                        .addTo(map);
                });
                
                // Cluster click to zoom
                map.on('click', 'clusters', (e) => {
                    const features = map.queryRenderedFeatures(e.point, {
                        layers: ['clusters']
                    });
                    const clusterId = features[0].properties.cluster_id;
                    map.getSource('admixture-data').getClusterExpansionZoom(
                        clusterId,
                        (err, zoom) => {
                            if (err) return;
                            
                            map.easeTo({
                                center: features[0].geometry.coordinates,
                                zoom: zoom
                            });
                        }
                    );
                });
                
                map.on('mouseenter', 'clusters', () => {
                    map.getCanvas().style.cursor = 'pointer';
                });
                
                map.on('mouseleave', 'clusters', () => {
                    map.getCanvas().style.cursor = '';
                });
            }
        }
        
        function getRandomCoordinates() {
            const lat = (Math.random() - 0.5) * 160; // -80 to 80
            const lng = (Math.random() - 0.5) * 360; // -180 to 180
            return [lng, lat];
        }
        
        function updateLegend(componentCount) {
            const colors = generateColorPalette(componentCount);
            const legendContainer = document.getElementById('legend');
            
            let legendHTML = '';
            for (let i = 0; i < componentCount; i++) {
                legendHTML += `
                    <div class="legend-item flex items-center space-x-3">
                        <div class="w-4 h-4 rounded-lg" style="background-color: ${colors[i]}"></div>
                        <span class="text-gray-700 text-sm font-medium">Componente ${i + 1}</span>
                    </div>
                `;
            }
            
            legendContainer.innerHTML = legendHTML;
        }
        
        function updateStatistics(data, componentCount) {
            const statsContainer = document.getElementById('statistics');
            
            const totalIndividuals = data.length;
            const avgProportions = new Array(componentCount).fill(0);
            
            data.forEach(item => {
                item.proportions.forEach((prop, index) => {
                    avgProportions[index] += prop;
                });
            });
            
            avgProportions.forEach((sum, index) => {
                avgProportions[index] = (sum / totalIndividuals).toFixed(3);
            });
            
            let statsHTML = `
                     <div class="bg-gradient-to-r from-blue-50 to-indigo-50 rounded-lg p-3 mb-4 border border-blue-200">
                         <p class="text-gray-800 text-sm font-semibold mb-2 flex items-center">
                             <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                 <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"></path>
                             </svg>
                             Resumo
                         </p>
                         <div class="space-y-1 text-xs text-gray-600">
                             <p><span class="font-medium">Indivíduos:</span> ${totalIndividuals}</p>
                             <p><span class="font-medium">Componentes:</span> ${componentCount}</p>
                             <p><span class="font-medium">Modelo:</span> ${currentModel}</p>
                         </div>
                     </div>
                 `;
            
            statsHTML += '<div class="space-y-2">';
            avgProportions.forEach((avg, index) => {
                const percentage = (avg * 100).toFixed(1);
                statsHTML += `
                    <div class="flex justify-between items-center text-sm py-1">
                        <span class="text-gray-700 font-medium">C${index + 1}:</span>
                        <span class="text-gray-600">${percentage}%</span>
                    </div>
                `;
            });
            statsHTML += '</div>';
            
            statsContainer.innerHTML = statsHTML;
        }
        
        function resetMapView() {
            if (map) {
                map.flyTo({ 
                    center: [0, 20], 
                    zoom: 2,
                    duration: 2000
                });
                showAlert('Vista do mapa resetada', 'success');
            }
        }
        
        function toggleClusters() {
            if (map && map.getLayer('clusters')) {
                const visibility = map.getLayoutProperty('clusters', 'visibility');
                const newVisibility = visibility === 'visible' ? 'none' : 'visible';
                
                map.setLayoutProperty('clusters', 'visibility', newVisibility);
                map.setLayoutProperty('cluster-count', 'visibility', newVisibility);
                
                const btn = document.getElementById('toggleClustersBtn');
                if (newVisibility === 'visible') {
                    btn.textContent = '📍 Ocultar Clusters';
                    showAlert('Clusters ativados', 'success');
                } else {
                    btn.textContent = '📍 Mostrar Clusters';
                    showAlert('Clusters desativados', 'info');
                }
            } else {
                showAlert('Carregue dados primeiro para usar clusters', 'warning');
            }
        }
        
        function toggleFullscreen() {
            const mapContainer = document.getElementById('map');
            
            if (!document.fullscreenElement) {
                mapContainer.requestFullscreen().then(() => {
                    showAlert('Modo tela cheia ativado', 'success');
                    if (map) map.resize();
                }).catch(err => {
                    showAlert('Erro ao ativar tela cheia', 'error');
                });
            } else {
                document.exitFullscreen().then(() => {
                    showAlert('Modo tela cheia desativado', 'info');
                    if (map) map.resize();
                }).catch(err => {
                    showAlert('Erro ao sair da tela cheia', 'error');
                });
            }
        }
        
        function changeMapStyle(event) {
            if (map) {
                const selectedStyle = event.target.value;
                const styleNames = {
                    'mapbox://styles/mapbox/streets-v12': 'Streets',
                    'mapbox://styles/mapbox/satellite-v9': 'Satellite',
                    'mapbox://styles/mapbox/light-v11': 'Light',
                    'mapbox://styles/mapbox/dark-v11': 'Dark'
                };
                
                map.setStyle(selectedStyle);
                
                // Re-add data layers after style change
                map.once('styledata', () => {
                    if (admixtureData) {
                        console.log('🎨 Recarregando dados após mudança de estilo...');
                        visualizeOnMap(admixtureData, admixtureData[0].proportions.length);
                    }
                });
                
                showAlert(`Estilo alterado para: ${styleNames[selectedStyle]}`, 'success');
            }
        }
        
        function exportMap() {
            if (!map) {
                showAlert('Mapa não está carregado', 'error');
                return;
            }
            
            // Create export modal
            const modal = document.createElement('div');
            modal.className = 'fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50';
            modal.innerHTML = `
                <div class="bg-white rounded-xl p-6 max-w-md w-full mx-4 animate__animated animate__fadeInUp">
                    <div class="flex items-center mb-4">
                        <div class="w-8 h-8 bg-gradient-to-br from-blue-500 to-blue-600 rounded-lg flex items-center justify-center mr-3">
                            <svg class="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
                            </svg>
                        </div>
                        <h3 class="text-lg font-semibold text-gray-800">Exportar Mapa</h3>
                    </div>
                    
                    <p class="text-gray-600 mb-6">Escolha o formato para exportar seu mapa de ancestralidade:</p>
                    
                    <div class="space-y-3 mb-6">
                        <button onclick="downloadMap('png')" class="w-full flex items-center p-3 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors">
                            <div class="w-10 h-10 bg-green-100 rounded-lg flex items-center justify-center mr-3">
                                <svg class="w-5 h-5 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"></path>
                                </svg>
                            </div>
                            <div class="text-left">
                                <div class="font-medium text-gray-800">PNG (Imagem)</div>
                                <div class="text-sm text-gray-500">Formato de imagem de alta qualidade</div>
                            </div>
                        </button>
                        
                        <button onclick="downloadMap('pdf')" class="w-full flex items-center p-3 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors">
                            <div class="w-10 h-10 bg-red-100 rounded-lg flex items-center justify-center mr-3">
                                <svg class="w-5 h-5 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
                                </svg>
                            </div>
                            <div class="text-left">
                                <div class="font-medium text-gray-800">PDF (Documento)</div>
                                <div class="text-sm text-gray-500">Documento para impressão e compartilhamento</div>
                            </div>
                        </button>
                        
                        <button onclick="downloadMap('svg')" class="w-full flex items-center p-3 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors">
                            <div class="w-10 h-10 bg-purple-100 rounded-lg flex items-center justify-center mr-3">
                                <svg class="w-5 h-5 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 21a4 4 0 01-4-4V5a2 2 0 012-2h4a2 2 0 012 2v12a4 4 0 01-4 4zM21 5a2 2 0 00-2-2h-4a2 2 0 00-2 2v12a4 4 0 004 4h4a2 2 0 002-2V5z"></path>
                                </svg>
                            </div>
                            <div class="text-left">
                                <div class="font-medium text-gray-800">SVG (Vetorial)</div>
                                <div class="text-sm text-gray-500">Formato vetorial escalável</div>
                            </div>
                        </button>
                    </div>
                    
                    <div class="flex gap-3">
                        <button onclick="closeExportModal()" class="flex-1 px-4 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors">
                            Cancelar
                        </button>
                    </div>
                </div>
            `;
            
            document.body.appendChild(modal);
            
            // Close modal function
            window.closeExportModal = function() {
                document.body.removeChild(modal);
                delete window.closeExportModal;
                delete window.downloadMap;
            };
            
            // Download function
              window.downloadMap = function(format) {
                  showAlert('Preparando exportação...', 'info');
                  
                  // Use requestAnimationFrame to ensure rendering is complete
                  requestAnimationFrame(() => {
                      try {
                          const canvas = map.getCanvas();
                          const timestamp = new Date().toISOString().slice(0, 10);
                          
                          console.log('Canvas dimensions:', canvas.width, 'x', canvas.height);
                          
                          if (format === 'png') {
                              const dataURL = canvas.toDataURL('image/png', 1.0);
                              console.log('PNG DataURL length:', dataURL.length);
                              downloadFile(dataURL, `mapa-ancestralidade-${timestamp}.png`);
                              showAlert('Mapa PNG exportado com sucesso!', 'success');
                              
                          } else if (format === 'pdf') {
                              // Convert canvas to PDF using jsPDF
                              const imgData = canvas.toDataURL('image/png', 1.0);
                              console.log('PDF Image data length:', imgData.length);
                              
                              if (typeof window.jspdf === 'undefined') {
                                  showAlert('Biblioteca PDF não carregada. Recarregue a página.', 'error');
                                  return;
                              }
                              
                              const { jsPDF } = window.jspdf;
                              const pdf = new jsPDF({
                                  orientation: 'landscape',
                                  unit: 'mm',
                                  format: 'a4'
                              });
                              
                              const pageWidth = 297; // A4 landscape width
                              const pageHeight = 210; // A4 landscape height
                              const imgAspectRatio = canvas.width / canvas.height;
                              
                              let imgWidth = pageWidth;
                              let imgHeight = pageWidth / imgAspectRatio;
                              
                              // If image is too tall, scale by height instead
                              if (imgHeight > pageHeight) {
                                  imgHeight = pageHeight;
                                  imgWidth = pageHeight * imgAspectRatio;
                              }
                              
                              // Center the image
                              const xOffset = (pageWidth - imgWidth) / 2;
                              const yOffset = (pageHeight - imgHeight) / 2;
                              
                              pdf.addImage(imgData, 'PNG', xOffset, yOffset, imgWidth, imgHeight);
                              pdf.save(`mapa-ancestralidade-${timestamp}.pdf`);
                              showAlert('Mapa PDF exportado com sucesso!', 'success');
                              
                          } else if (format === 'svg') {
                              // Convert canvas to SVG
                              const imgData = canvas.toDataURL('image/png', 1.0);
                              const svgData = `<svg xmlns="http://www.w3.org/2000/svg" width="${canvas.width}" height="${canvas.height}">
                                  <image href="${imgData}" width="${canvas.width}" height="${canvas.height}"/>
                              </svg>`;
                              
                              const blob = new Blob([svgData], { type: 'image/svg+xml' });
                              const url = URL.createObjectURL(blob);
                              downloadFile(url, `mapa-ancestralidade-${timestamp}.svg`);
                              showAlert('Mapa SVG exportado com sucesso!', 'success');
                          }
                          
                          closeExportModal();
                          
                      } catch (error) {
                          console.error('Erro ao exportar mapa:', error);
                          showAlert(`Erro ao exportar mapa em ${format.toUpperCase()}: ${error.message}`, 'error');
                      }
                  });
              };
        }
        
        function downloadFile(dataURL, filename) {
            const link = document.createElement('a');
            link.download = filename;
            link.href = dataURL;
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
        }
        
        function canvasToSVG(canvas) {
            const ctx = canvas.getContext('2d');
            const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
            
            let svg = `<svg xmlns="http://www.w3.org/2000/svg" width="${canvas.width}" height="${canvas.height}">`;
            svg += `<image href="${canvas.toDataURL()}" width="${canvas.width}" height="${canvas.height}"/>`;
            svg += '</svg>';
            
            return svg;
        }
        
        function showAlert(message, type = 'info') {
            const alertDiv = document.createElement('div');
             const iconColor = type === 'error' ? 'text-red-500' :
                              type === 'warning' ? 'text-yellow-500' :
                              type === 'success' ? 'text-green-500' :
                              'text-blue-500';
             
             const iconPath = type === 'error' ? 'M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z' :
                             type === 'warning' ? 'M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.732-.833-2.464 0L3.34 16.5c-.77.833.192 2.5 1.732 2.5z' :
                             type === 'success' ? 'M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z' :
                             'M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z';
             
             alertDiv.className = `notification fixed top-4 right-4 z-50 p-4 animate__animated animate__fadeInRight`;
             alertDiv.innerHTML = `
                 <div class="flex items-center">
                     <div class="${iconColor} mr-3">
                         <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                             <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="${iconPath}"></path>
                         </svg>
                     </div>
                     <span class="font-medium">${message}</span>
                     <button class="ml-4 text-gray-400 hover:text-gray-600 transition-colors" onclick="this.parentElement.parentElement.remove()">
                         <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                             <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
                         </svg>
                     </button>
                 </div>
             `;
            
            document.body.appendChild(alertDiv);
            
            setTimeout(() => {
                if (alertDiv.parentElement) {
                    alertDiv.classList.add('animate__fadeOutRight');
                    setTimeout(() => alertDiv.remove(), 500);
                }
            }, 5000);
        }
        
        // Theme Management System
        class ThemeManager {
            constructor() {
                this.currentTheme = this.getStoredTheme() || this.getSystemTheme();
                this.init();
            }
            
            init() {
                this.applyTheme(this.currentTheme);
                this.setupEventListeners();
                this.watchSystemTheme();
                console.log(`Tema inicializado: ${this.currentTheme}`);
            }
            
            getSystemTheme() {
                return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
            }
            
            getStoredTheme() {
                return localStorage.getItem('theme');
            }
            
            setStoredTheme(theme) {
                localStorage.setItem('theme', theme);
            }
            
            applyTheme(theme) {
                const body = document.body;
                
                // Remove existing theme classes
                body.classList.remove('theme-light', 'theme-dark');
                
                // Apply new theme class
                body.classList.add(`theme-${theme}`);
                
                // Update UI elements
                this.updateThemeUI(theme);
                
                this.currentTheme = theme;
                this.setStoredTheme(theme);
            }
            
            updateThemeUI(theme) {
                const sunIcon = document.getElementById('sunIcon');
                const moonIcon = document.getElementById('moonIcon');
                const themeText = document.getElementById('themeText');
                
                if (theme === 'dark') {
                    sunIcon?.classList.add('hidden');
                    moonIcon?.classList.remove('hidden');
                    if (themeText) themeText.textContent = 'Claro';
                } else {
                    sunIcon?.classList.remove('hidden');
                    moonIcon?.classList.add('hidden');
                    if (themeText) themeText.textContent = 'Escuro';
                }
            }
            
            toggleTheme() {
                const newTheme = this.currentTheme === 'light' ? 'dark' : 'light';
                this.applyTheme(newTheme);
                
                // Show notification
                showAlert(`Tema alterado para ${newTheme === 'dark' ? 'escuro' : 'claro'}`, 'success');
            }
            
            setupEventListeners() {
                const themeToggle = document.getElementById('themeToggle');
                if (themeToggle) {
                    themeToggle.addEventListener('click', () => this.toggleTheme());
                }
            }
            
            watchSystemTheme() {
                const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
                
                mediaQuery.addEventListener('change', (e) => {
                    // Only auto-switch if user hasn't manually set a preference
                    if (!this.getStoredTheme()) {
                        const systemTheme = e.matches ? 'dark' : 'light';
                        this.applyTheme(systemTheme);
                        showAlert(`Tema alterado automaticamente para ${systemTheme === 'dark' ? 'escuro' : 'claro'}`, 'info');
                    }
                });
            }
        }
        
        // Initialize theme management when DOM is loaded
        document.addEventListener('DOMContentLoaded', () => {
            window.themeManager = new ThemeManager();
        });
        
        // Keyboard shortcut for theme toggle (Ctrl/Cmd + Shift + T)
        document.addEventListener('keydown', (e) => {
            if ((e.ctrlKey || e.metaKey) && e.shiftKey && e.key === 'T') {
                e.preventDefault();
                if (window.themeManager) {
                    window.themeManager.toggleTheme();
                }
            }
        });
    </script>
</body>
</html>
    ''')

if __name__ == '__main__':
    print('''
🧬 Aplicação de Análise de Ancestralidade Genética
📍 Acesse: http://localhost:5000

📋 Funcionalidades:
   • Upload de arquivos .txt com resultados Admixture
   • Campo para colar dados diretamente
   • Mapa interativo com Mapbox GL JS
   • Suporte universal para qualquer modelo K
   • Detecção automática do número de componentes
   • Visualização de dados GeoJSON

✅ Token Mapbox configurado e pronto para uso!
    ''')
    
    app.run(debug=True, host='0.0.0.0', port=5000)