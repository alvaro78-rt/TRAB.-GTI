from http.server import HTTPServer, BaseHTTPRequestHandler
import webbrowser

HTML_CONTENT = """
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Jornada do Século - 100 Anos</title>
    <!-- Fontes do Google e Ícones do FontAwesome -->
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;800&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        :root {
            --primary: #00f2fe;
            --secondary: #4facfe;
            --dark: #0a0a0a;
            --light: #f8f9fa;
            --glass-bg: rgba(255, 255, 255, 0.05);
            --glass-border: rgba(255, 255, 255, 0.1);
        }
        
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Poppins', sans-serif;
        }

        body {
            background: #0f0c29;  /* fallback para navegadores antigos */
            background: -webkit-linear-gradient(to right, #24243e, #302b63, #0f0c29);
            background: linear-gradient(to right, #24243e, #302b63, #0f0c29);
            color: var(--light);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            overflow: hidden;
            position: relative;
        }

        /* Partículas flutuantes no fundo */
        .circles {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            overflow: hidden;
            z-index: 0;
        }

        .circles li {
            position: absolute;
            display: block;
            list-style: none;
            width: 20px;
            height: 20px;
            background: rgba(255, 255, 255, 0.1);
            animation: animate 25s linear infinite;
            bottom: -150px;
            border-radius: 50%;
        }

        .circles li:nth-child(1) { left: 25%; width: 80px; height: 80px; animation-delay: 0s; }
        .circles li:nth-child(2) { left: 10%; width: 20px; height: 20px; animation-delay: 2s; animation-duration: 12s; }
        .circles li:nth-child(3) { left: 70%; width: 20px; height: 20px; animation-delay: 4s; }
        .circles li:nth-child(4) { left: 40%; width: 60px; height: 60px; animation-delay: 0s; animation-duration: 18s; }
        .circles li:nth-child(5) { left: 65%; width: 20px; height: 20px; animation-delay: 0s; }
        .circles li:nth-child(6) { left: 75%; width: 110px; height: 110px; animation-delay: 3s; }
        .circles li:nth-child(7) { left: 35%; width: 150px; height: 150px; animation-delay: 7s; }
        .circles li:nth-child(8) { left: 50%; width: 25px; height: 25px; animation-delay: 15s; animation-duration: 45s; }
        .circles li:nth-child(9) { left: 20%; width: 15px; height: 15px; animation-delay: 2s; animation-duration: 35s; }
        .circles li:nth-child(10) { left: 85%; width: 150px; height: 150px; animation-delay: 0s; animation-duration: 11s; }

        @keyframes animate {
            0% { transform: translateY(0) rotate(0deg); opacity: 1; border-radius: 0; }
            100% { transform: translateY(-1000px) rotate(720deg); opacity: 0; border-radius: 50%; }
        }

        /* Painel Glassmorphism Avançado */
        .glass-panel {
            background: var(--glass-bg);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            border: 1px solid var(--glass-border);
            border-radius: 24px;
            padding: 3rem 2.5rem;
            width: 100%;
            max-width: 480px;
            z-index: 10;
            box-shadow: 0 25px 45px rgba(0, 0, 0, 0.2);
            position: relative;
            transition: transform 0.4s ease, box-shadow 0.4s ease;
        }

        .glass-panel:hover {
            transform: translateY(-5px);
            box-shadow: 0 30px 60px rgba(0, 0, 0, 0.4);
        }

        .header {
            text-align: center;
            margin-bottom: 2.5rem;
        }

        .header i {
            font-size: 3rem;
            background: -webkit-linear-gradient(var(--primary), var(--secondary));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 1rem;
            animation: pulse 2s infinite;
        }

        @keyframes pulse {
            0% { transform: scale(1); }
            50% { transform: scale(1.05); }
            100% { transform: scale(1); }
        }

        h1 {
            font-size: 2rem;
            font-weight: 800;
            letter-spacing: -0.5px;
            background: linear-gradient(to right, #fff, #a5b4fc);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        
        p.subtitle {
            font-size: 0.9rem;
            color: #a5b4fc;
            margin-top: 0.5rem;
        }

        .input-group {
            position: relative;
            margin-bottom: 1.5rem;
        }

        .input-group i {
            position: absolute;
            left: 15px;
            top: 50%;
            transform: translateY(-50%);
            color: #a5b4fc;
            font-size: 1.2rem;
            transition: color 0.3s;
        }

        input {
            width: 100%;
            padding: 16px 16px 16px 45px;
            background: rgba(0, 0, 0, 0.2);
            border: 2px solid transparent;
            border-radius: 12px;
            color: #fff;
            font-size: 1rem;
            transition: all 0.3s ease;
            outline: none;
        }

        input::placeholder {
            color: rgba(255, 255, 255, 0.5);
        }

        input:focus {
            border-color: var(--primary);
            background: rgba(0, 0, 0, 0.4);
            box-shadow: 0 0 15px rgba(0, 242, 254, 0.2);
        }

        input:focus + i, input:focus ~ i {
            color: var(--primary);
        }

        .btn {
            width: 100%;
            padding: 16px;
            border: none;
            border-radius: 12px;
            background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
            color: #fff;
            font-size: 1.1rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            text-transform: uppercase;
            letter-spacing: 1.5px;
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 10px;
            box-shadow: 0 10px 20px rgba(79, 172, 254, 0.3);
            margin-top: 1rem;
        }

        .btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 15px 25px rgba(79, 172, 254, 0.5);
        }

        .btn:active {
            transform: translateY(1px);
        }

        /* Container de Resultados com Animações */
        #result-container {
            margin-top: 2rem;
            padding-top: 2rem;
            border-top: 1px solid rgba(255,255,255,0.1);
            display: none;
            text-align: center;
            animation: slideUp 0.6s cubic-bezier(0.16, 1, 0.3, 1) forwards;
        }

        @keyframes slideUp {
            from { opacity: 0; transform: translateY(30px) scale(0.95); }
            to { opacity: 1; transform: translateY(0) scale(1); }
        }

        .greeting {
            font-size: 1.5rem;
            font-weight: 600;
            margin-bottom: 1rem;
            color: #fff;
        }

        .highlight-name {
            color: var(--primary);
            text-shadow: 0 0 10px rgba(0, 242, 254, 0.5);
            font-weight: 800;
        }

        /* Gráfico Circular de Progresso */
        .progress-circle {
            position: relative;
            width: 160px;
            height: 160px;
            margin: 1.5rem auto;
            border-radius: 50%;
            background: conic-gradient(var(--primary) var(--percentage), rgba(255,255,255,0.1) 0);
            display: flex;
            justify-content: center;
            align-items: center;
            box-shadow: 0 0 25px rgba(0, 0, 0, 0.5), inset 0 0 15px rgba(0, 0, 0, 0.5);
        }

        .progress-circle::after {
            content: '';
            position: absolute;
            width: 136px;
            height: 136px;
            background: #272740; /* Cor central próxima ao fundo do painel */
            border-radius: 50%;
            box-shadow: inset 0 0 10px rgba(0,0,0,0.5);
        }

        .progress-text {
            position: relative;
            z-index: 1;
            font-size: 3rem;
            font-weight: 800;
            color: var(--primary);
            text-shadow: 0 2px 10px rgba(0,0,0,0.5);
            display: flex;
            flex-direction: column;
            line-height: 1;
        }

        .progress-label {
            font-size: 0.9rem;
            color: #a5b4fc;
            font-weight: 600;
            margin-top: 5px;
            text-transform: uppercase;
            letter-spacing: 2px;
        }

        .message {
            font-size: 1.2rem;
            line-height: 1.6;
            color: #e0e7ff;
            background: rgba(0,0,0,0.3);
            padding: 1.2rem;
            border-radius: 12px;
            border-left: 5px solid var(--primary);
            margin-top: 1rem;
        }

        .error {
            color: #ff4757;
            font-size: 0.85rem;
            margin-top: 0.5rem;
            display: none;
            text-align: left;
            padding-left: 10px;
        }

        /* Script de Confete (para quando bater 100/passar de 100) */
        #confetti-canvas {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
            z-index: 9999;
        }
    </style>
</head>
<body>
    <!-- Confetes ocultos até precisar -->
    <canvas id="confetti-canvas"></canvas>

    <!-- Partículas em CSS -->
    <ul class="circles">
        <li></li><li></li><li></li><li></li><li></li>
        <li></li><li></li><li></li><li></li><li></li>
    </ul>

    <div class="glass-panel">
        <div class="header">
            <i class="fa-solid fa-hourglass-half"></i>
            <h1>Jornada do Século</h1>
            <p class="subtitle">Acompanhe seu percurso até os gloriosos 100 anos</p>
        </div>

        <div class="input-group">
            <i class="fa-solid fa-user-astronaut"></i>
            <input type="text" id="nome" placeholder="Digite seu nome incrível" autocomplete="off">
            <div id="error-nome" class="error"><i class="fa-solid fa-circle-exclamation"></i> Por favor, informe seu nome.</div>
        </div>

        <div class="input-group">
            <i class="fa-solid fa-cake-candles"></i>
            <input type="number" id="idade" placeholder="Digite sua idade atual" min="0" max="150" autocomplete="off">
            <div id="error-idade" class="error"><i class="fa-solid fa-circle-exclamation"></i> Informe uma idade válida (0 a 150).</div>
        </div>

        <button class="btn" onclick="calcular()">
            <span>Viajar no Tempo</span>
            <i class="fa-solid fa-rocket"></i>
        </button>

        <div id="result-container">
            <div class="greeting" id="greeting-text"></div>
            
            <div class="progress-circle" id="progress">
                <div class="progress-text">
                    <span id="years-left">0</span>
                    <span class="progress-label" id="years-label">Anos</span>
                </div>
            </div>

            <div class="message" id="message-text"></div>
        </div>
    </div>

    <!-- Biblioteca de Confetes em JavaScript (via CDN) -->
    <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.6.0/dist/confetti.browser.min.js"></script>

    <script>
        function calcular() {
            const nomeStr = document.getElementById('nome').value.trim();
            const idadeStr = document.getElementById('idade').value;
            
            const errNome = document.getElementById('error-nome');
            const errIdade = document.getElementById('error-idade');
            const resultBox = document.getElementById('result-container');
            
            let hasError = false;

            // Validação de Nome
            if (!nomeStr) { 
                errNome.style.display = 'block'; 
                hasError = true; 
            } else { 
                errNome.style.display = 'none'; 
            }

            // Validação de Idade
            const idade = parseInt(idadeStr);
            if (isNaN(idade) || idade < 0 || idade > 150) { 
                errIdade.style.display = 'block'; 
                hasError = true; 
            } else { 
                errIdade.style.display = 'none'; 
            }

            if (hasError) {
                resultBox.style.display = 'none';
                return;
            }

            // Cálculos
            const anosFaltantes = 100 - idade;
            // Cálculo da porcentagem para preencher o círculo de progresso
            const porcentagem = Math.min((idade / 100) * 100, 100);
            
            // Inserção no DOM
            document.getElementById('greeting-text').innerHTML = `Olá, <span class="highlight-name">${nomeStr}</span>!`;
            
            const progressCircle = document.getElementById('progress');
            // Mostra o valor absoluto para não mostrar número negativo
            document.getElementById('years-left').innerText = Math.abs(anosFaltantes); 
            
            const messageText = document.getElementById('message-text');

            // Resetar a Animação do Box
            resultBox.style.display = 'none';
            // Trigger reflow
            void resultBox.offsetWidth;
            
            setTimeout(() => {
                resultBox.style.display = 'block';
                
                // Animar o Círculo de Progresso Customizado
                let currentPercent = 0;
                let targetPercent = porcentagem;
                
                // Se a pessoa passou de 100, mantemos a barra 100% cheia
                if(anosFaltantes <= 0) targetPercent = 100;

                const interval = setInterval(() => {
                    currentPercent += 2;
                    if(currentPercent >= targetPercent) {
                        currentPercent = targetPercent;
                        clearInterval(interval);
                    }
                    progressCircle.style.setProperty('--percentage', `${currentPercent}%`);
                }, 20);

                // Regras e Estilos dependendo da idade
                if (anosFaltantes > 0) {
                    document.getElementById('years-label').innerText = 'Faltam';
                    messageText.innerHTML = `Que jornada maravilhosa pela frente! Faltam exatamente <strong>${anosFaltantes} anos</strong> para você celebrar 1 século de vida. Foco no futuro!`;
                    progressCircle.style.background = `conic-gradient(var(--primary) var(--percentage), rgba(255,255,255,0.1) 0)`;
                    document.querySelector('.progress-text').style.color = 'var(--primary)';
                    messageText.style.borderLeftColor = 'var(--primary)';
                } else if (anosFaltantes === 0) {
                    document.getElementById('years-label').innerText = 'EXATOS';
                    messageText.innerHTML = `INACREDITÁVEL! Você está completando exatamente <strong>100 anos</strong> de existência! Um marco histórico! Parabéns!`;
                    // Dourado para representar o centenário
                    progressCircle.style.background = `conic-gradient(#ffd700 var(--percentage), rgba(255,255,255,0.1) 0)`;
                    document.querySelector('.progress-text').style.color = '#ffd700';
                    messageText.style.borderLeftColor = '#ffd700';
                    dispararConfetes();
                } else {
                    document.getElementById('years-label').innerText = 'Excedidos';
                    messageText.innerHTML = `Uau! Você é uma verdadeira lenda viva! Já se passaram <strong>${Math.abs(anosFaltantes)} anos</strong> desde o seu centenário histórico!`;
                    // Rosa/Magenta para idade superior a 100
                    progressCircle.style.background = `conic-gradient(#ff007f var(--percentage), rgba(255,255,255,0.1) 0)`;
                    document.querySelector('.progress-text').style.color = '#ff007f';
                    messageText.style.borderLeftColor = '#ff007f';
                    dispararConfetes();
                }

            }, 50);
        }

        // Função para lançar poeira de confetes
        function dispararConfetes() {
            var myCanvas = document.getElementById('confetti-canvas');
            var myConfetti = confetti.create(myCanvas, { resize: true, useWorker: true });
            
            var duration = 4 * 1000;
            var animationEnd = Date.now() + duration;
            var defaults = { startVelocity: 30, spread: 360, ticks: 60, zIndex: 9999 };

            function randomInRange(min, max) { return Math.random() * (max - min) + min; }

            var interval = setInterval(function() {
                var timeLeft = animationEnd - Date.now();
                if (timeLeft <= 0) { return clearInterval(interval); }
                var particleCount = 50 * (timeLeft / duration);
                // Canhões de confete pela esquerda e direita
                myConfetti(Object.assign({}, defaults, { particleCount, origin: { x: randomInRange(0.1, 0.3), y: Math.random() - 0.2 } }));
                myConfetti(Object.assign({}, defaults, { particleCount, origin: { x: randomInRange(0.7, 0.9), y: Math.random() - 0.2 } }));
            }, 250);
        }
    </script>
</body>
</html>
"""

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(HTML_CONTENT.encode('utf-8'))
        
    def log_message(self, format, *args):
        # Desabilita o log automático a cada requisição para manter o terminal limpo
        pass

def run(server_class=HTTPServer, handler_class=SimpleHTTPRequestHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    
    print("\\n" + "="*55)
    print("  [>] SERVIDOR WEB - JORNADA DO SECULO INICIADO!")
    print(f"  [>] Acesse o site em: http://localhost:{port}")
    print("  [!] Para desligar o servidor, pressione CTRL+C")
    print("="*55 + "\\n")
    
    try:
        # Tenta abrir no Google Chrome explicitamente
        url = f'http://localhost:{port}'
        try:
            # Caminhos comuns do Chrome no Windows
            chrome_path = 'C:/Program Files/Google/Chrome/Application/chrome.exe %s'
            webbrowser.get(chrome_path).open(url)
        except webbrowser.Error:
            try:
                # Tenta pelo nome 'chrome' registrado no sistema
                webbrowser.get('chrome').open(url)
            except webbrowser.Error:
                # Fallback: abre no navegador padrão do Windows
                webbrowser.open(url)
                
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\\nServidor desligado com sucesso.")
        httpd.server_close()

if __name__ == '__main__':
    run()
