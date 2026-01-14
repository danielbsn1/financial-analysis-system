# Guia de Contribuição

Obrigado por considerar contribuir com o Sistema de Análise Financeira! 🎉

## Como Contribuir

### Reportar Bugs

Se você encontrou um bug, por favor abra uma issue incluindo:

- Descrição clara do problema
- Passos para reproduzir
- Comportamento esperado vs atual
- Screenshots (se aplicável)
- Ambiente (OS, Python version, etc.)

### Sugerir Melhorias

Adoramos receber sugestões! Abra uma issue com:

- Descrição detalhada da funcionalidade
- Por que seria útil
- Exemplos de uso

### Pull Requests

1. **Fork** o repositório
2. **Clone** seu fork
3. **Crie uma branch** para sua feature
   ```bash
   git checkout -b feature/MinhaNovaFeature
   ```
4. **Faça suas alterações**
5. **Teste** suas mudanças
6. **Commit** com mensagens claras
   ```bash
   git commit -m "feat: adiciona nova funcionalidade X"
   ```
7. **Push** para sua branch
   ```bash
   git push origin feature/MinhaNovaFeature
   ```
8. **Abra um Pull Request**

## Padrões de Código

### Python
- Siga PEP 8
- Use type hints quando possível
- Docstrings para funções públicas
- Máximo 100 caracteres por linha

### JavaScript
- Use ES6+
- Nomes descritivos de variáveis
- Comentários para lógica complexa

### Commits
Use Conventional Commits:
- `feat:` nova funcionalidade
- `fix:` correção de bug
- `docs:` documentação
- `style:` formatação
- `refactor:` refatoração
- `test:` testes
- `chore:` tarefas gerais

## Testes

Sempre adicione testes para novas funcionalidades:

```bash
python -m pytest tests/
```

## Dúvidas?

Abra uma issue ou entre em contato!