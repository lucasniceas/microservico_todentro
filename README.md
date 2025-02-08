# 🎵 Microserviço de Geração de Áudio Personalizado

Este microserviço foi desenvolvido para gerar um áudio personalizado para convites de eventos. O sistema combina efeitos sonoros, trechos de músicas, base neutra e locução gerada via TTS (Text-to-Speech) intercalados de forma dinâmica.

## 📌 **Funcionalidades Implementadas**

✅ Geração de convites de áudio com locução automatizada (TTS em português do Brasil).  
✅ Uso de efeitos sonoros no início, meio e final do áudio.  
✅ Seleção automática de trechos das músicas (pegando o refrão em 1:20 minutos, quando possível).  
✅ Aplicação de fade-in na música para transição suave.  
✅ Sobreposição de uma base neutra de fundo para o gênero musical.  
✅ Processamento local de músicas baixadas previamente.  

## 📂 **Estrutura de Pastas**

```
📁 microservico_todentro/
├── 📁 app/
│   ├── 📁 assets/
│   │   ├── 📁 sertanejo/
│   │   │   ├── base_neutra.mp3
│   │   │   ├── Jorge & Mateus.mp3
│   │   │   ├── Henrique e Juliano.mp3
│   │   │   ├── Matheus & Kauan.mp3
│   │   │   ├── 📁 entrada/
│   │   │   │   ├── big-fone-atencao.mp3
│   │   │   │   ├── woosh-effect.mp3
│   │   │   ├── 📁 meio/
│   │   │   │   ├── irra-ratinho.mp3
│   │   │   │   ├── quick-double-swish.mp3
│   ├── 📁 services/
│   │   ├── audio_processor.py
│   │   ├── youtube_downloader.py
├── 📁 output/
│   ├── <Nome_do_cliente>_final.mp3
├── main.py
├── requirements.txt
└── README.md
```

## 🚀 **Instalação e Configuração**

### **1️⃣ Clonar o Repositório**
```sh
git clone <URL_DO_REPOSITORIO>
cd microservico_todentro
```

### **2️⃣ Criar e Ativar o Ambiente Virtual**
```sh
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate  # Windows
```

### **3️⃣ Instalar as Dependências**
```sh
pip install -r requirements.txt
```

### **4️⃣ Executar o Servidor Flask**
```sh
FLASK_APP=main.py flask run --host=0.0.0.0 --port=5000
```

## 🛠 **Como Usar**

A API recebe uma requisição POST contendo os dados do evento e gera um áudio personalizado. Para testar via **cURL** ou **Postman**, envie uma requisição para:

```
POST http://127.0.0.1:5000/process_audio
Content-Type: application/json
```

### **Exemplo de JSON de Entrada:**
```json
{
  "generoMusical": "sertanejo",
  "textoConvite": "Olá, João! Esperamos você para um evento inesquecível! No dia 15 de março, na Fazenda Boa Vista, teremos muita música e diversão.",
  "dadosEvento": {"nomePessoa": "João"},
  "linksMusicas": [
    "Jorge & Mateus.mp3",
    "Henrique e Juliano.mp3",
    "Matheus & Kauan.mp3"
  ]
}
```

### **Resposta Esperada:**
```json
{
  "genero": "sertanejo",
  "texto_convite": "Olá, João! Esperamos você para um evento inesquecível!...",
  "dados_evento": {"nomePessoa": "João"},
  "links_musicas": ["Jorge & Mateus.mp3", "Henrique e Juliano.mp3", "Matheus & Kauan.mp3"],
  "output_path": "output/Joao_final.mp3",
  "status": "Áudio processado e exportado com sucesso."
}
```

## 🎼 **Lógica da Montagem do Áudio**
1️⃣ **Efeito inicial** (Exemplo: "big-fone-atencao.mp3")  
2️⃣ **Trecho de TTS** (Parte 1 do texto do convite)  
3️⃣ **Trecho do refrão da música 1** (Corte de 10s a partir de 1:20min)  
4️⃣ **Efeito sonoro** (Exemplo: "irra-ratinho.mp3")  
5️⃣ **Trecho de TTS** (Parte 2 do texto do convite)  
6️⃣ **Trecho do refrão da música 2** (Corte de 10s a partir de 1:20min)  
7️⃣ **Efeito sonoro** (Exemplo: "quick-double-swish.mp3")  
8️⃣ **Trecho de TTS** (Parte 3 do texto do convite)  
9️⃣ **Trecho do refrão da música 3** (Corte de 10s a partir de 1:20min)  
🔟 **Efeito final** (2 segundos de silêncio)  
🎶 **Base neutra** tocando suavemente no fundo  

## 📌 **Ajustes Realizados na Versão Final**

✔️ **Correção do idioma do TTS** para **português do Brasil (pt-br)**.  
✔️ **Correção do tempo de corte da música**, pegando trechos do refrão em vez do início.  
✔️ **Aprimoramento da mixagem** com **fade-in** nas músicas para transições suaves.  
✔️ **Correção de diretórios** para garantir que os arquivos de música sejam lidos corretamente.  

## 📢 **Feedback e Melhorias**
Se houver necessidade de ajustes, como **alterar a posição dos cortes, incluir novas músicas ou efeitos**, basta modificar os arquivos dentro de `app/assets/sertanejo/` e executar novamente o processamento.

---

📌 **Projeto concluído!** Agora basta testar e enviar ao cliente. 🚀🎧

