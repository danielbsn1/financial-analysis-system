#  Sistema de Análise Financeira

> Dashboard interativo para análise técnica de ações com indicadores avançados e previsões de preço usando Machine Learning.

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-2.3.3-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

##  Sobre o Projeto

Sistema web completo para análise de ações do mercado financeiro, desenvolvido com Python e Flask. Permite visualizar dados históricos, calcular indicadores técnicos em tempo real e fazer previsões de preço usando algoritmos de Machine Learning.

###  Funcionalidades

-  **Gráficos Interativos** - Candlestick, volume e indicadores técnicos
-  **10+ Indicadores Técnicos** - SMA, EMA, RSI, MACD, Bollinger Bands, Stochastic, Williams %R, CCI, ATR, OBV
-  **Previsões com ML** - Regressão polinomial para previsão de preços
-  **Interface Moderna** - Design responsivo e tema dark/light
-  **Mobile Friendly** - Funciona perfeitamente em dispositivos móveis

##  Tecnologias Utilizadas

### Backend
- **Python 3.11+** - Linguagem principal
- **Flask** - Framework web
- **Pandas** - Manipulação de dados
- **NumPy** - Computação numérica
- **Scikit-learn** - Machine Learning
- **TwelveData API** - Dados de mercado em tempo real

### Frontend
- **HTML5/CSS3** - Estrutura e estilo
- **JavaScript ES6+** - Interatividade
- **Plotly.js** - Visualização de dados
- **Responsive Design** - Mobile-first

##  Pré-requisitos

- Python 3.11 ou superior
- pip (gerenciador de pacotes Python)
- Conta gratuita na [TwelveData](https://twelvedata.com/) para API key

##  Como Executar

### 1. Clone o repositório
```bash
git clone https://github.com/seu-usuario/sistema-analise-financeira.git
cd sistema-analise-financeira/Sistema-Analise-Financeira
```

### 2. Crie um ambiente virtual
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 3. Instale as dependências
```bash
pip install -r requirements.txt
```

## 📖 Como Usar

1. **Selecione uma ação** - Digite o ticker (ex: AAPL, TSLA, MSFT)
2. **Escolha o período** - Defina data de início e fim
3. **Selecione indicadores** - Escolha quais indicadores deseja visualizar
4. **Clique em "Buscar Dados"** - Aguarde o carregamento dos gráficos
5. **Analise os resultados** - Explore os gráficos interativos
6. **Baixe o relatório** - Exporte os dados em Excel

## 📊 Indicadores Técnicos Disponíveis

| Indicador | Descrição | Uso |
|-----------|-----------|-----|
| **SMA** | Média Móvel Simples | Identificar tendências |
| **EMA** | Média Móvel Exponencial | Sinais mais rápidos |
| **RSI** | Índice de Força Relativa | Sobrecompra/sobrevenda |
| **MACD** | Convergência/Divergência | Momentum |
| **Bollinger Bands** | Bandas de Volatilidade | Volatilidade do preço |
| **Stochastic** | Oscilador Estocástico | Momentum |
| **Williams %R** | Indicador de Momentum | Reversões |
| **CCI** | Commodity Channel Index | Tendências |
| **ATR** | Average True Range | Volatilidade |
| **OBV** | On Balance Volume | Volume acumulado |

##  Testes

```bash
# Executar testes unitários
python -m pytest tests/

# Com cobertura
python -m pytest --cov=. tests/
```

##  Estrutura do Projeto

```
Sistema-Analise-Financeira/
├── static/
│   ├── app.js           # Lógica do frontend
│   └── styles.css       # Estilos
├── templates/
│   └── index.html       # Interface principal
├── tests/
│   └── test_sistema.py  # Testes unitários
├── app_simples.py       # Aplicação Flask
├── requirements.txt     # Dependências
├── .env                 # Variáveis de ambiente
└── README.md           # Este arquivo
```

##  Aprendizados

Este projeto foi desenvolvido para demonstrar conhecimentos em:

-  Desenvolvimento web com Flask
-  Manipulação de dados com Pandas
-  Machine Learning com Scikit-learn
-  Integração com APIs REST
-  Visualização de dados
- Design responsivo
-  Boas práticas de código

##  Contribuindo

Contribuições são bem-vindas! Sinta-se à vontade para:

1. Fazer um Fork do projeto
2. Criar uma branch para sua feature (`git checkout -b feature/NovaFuncionalidade`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/NovaFuncionalidade`)
5. Abrir um Pull Request

##  Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

##  Autor

**Daniel batista **


##  Agradecimentos

- [TwelveData](https://twelvedata.com/) - API de dados financeiros
- [Plotly](https://plotly.com/) - Biblioteca de gráficos
- [Flask](https://flask.palletsprojects.com/) - Framework web

---

 Se este projeto te ajudou, considere dar uma estrela!
