## Contribuindo com Diário de Enxaqueca – Backend

Obrigado por seu interesse em contribuir para o backend do Diário de Enxaqueca! Este documento descreve as diretrizes e boas práticas para contribuir de forma eficiente, consistente e alinhada aos padrões de qualidade do projeto.

---

##  Como contribuir
### 1. Clonar o repositório

Clone o repositório localmente:
```bash
git clone https://github.com/diario-enxaqueca/backend.git
cd backend
```

### 2. Criar uma nova branch

Sempre baseie sua branch em `main`:
```bash
git checkout main
git pull
git checkout -b feature/nome-da-feature
```

Use nomes descritivos, por exemplo:
* Funcionalidades: feature/criar-episodio
* Correções de bug: fix/token-invalido
* Documentação: docs/atualiza-readme

##Padrão de commits
Siga o padrão Conventional Commits para manter a consistência no histórico do projeto.

Formato:
```php-template
<tipo>[escopo opcional]: <descrição>
```

Exemplos de tipos aceitos:
Tipo      |  Descrição                              
----------+-----------------------------------------
feat      |  Nova funcionalidade                    
fix       |  Correção de bug                        
docs      |  Alterações na documentação             
style     |  Ajustes de formatação e lint           
refactor  |  Refatoração sem mudança funcional      
test      |  Adição ou modificação de testes        
chore     |  Tarefas de build, CI/CD ou dependências

#### Exemplo de commit:
```bash
git commit -m "feat(episodio): adiciona endpoint para criar episodio"
```

---

## Diretrizes e Boas Práticas
Para garantir a qualidade e manutenibilidade do projeto, siga estas recomendações:
* Arquitetura: mantenha o padrão MVC (Model, View, Controller).
* Clean Code: use nomes claros, evite duplicação e métodos longos.
* SOLID: aplique princípios de baixo acoplamento e alta coesão.
* Documentação: mantenha docstrings claras no estilo Google Docstring.
* Tipagem: utilize type hints e boas práticas PEP 484.
* Lint: o projeto usa Ruff para linting. Verifique o código antes de commitar:

```bash
ruff check .
```

Corrigir automaticamente:

```bash
ruff check . --fix
```
* Tests: sempre escreva testes unitários e de integração com pytest:

```bash
pytest
```

* Docker: valide se o backend e o banco MySQL inicializam corretamente após suas alterações.

---
### Fluxo de Desenvolvimento Local
1. Fork no seu GitHub (se externo ao grupo).
2. Clone e instale dependências.
3. Configure variáveis de ambiente no arquivo .env.
4. Rode a aplicação localmente ou via docker-compose.
5. Adicione e teste sua funcionalidade.
6. Antes do commit, execute lint e testes.
7. Faça push da feature branch.
8. 
---

#### Abrindo um Pull Request

1. Envie sua branch:
```bash
git push origin feature/nome-da-feature
```
2. Acesse o repositório no GitHub.
3. Crie o Pull Request (PR) direcionado para main.
4. Descreva claramente:
* O que foi implementado
* Qual problema ou funcionalidade resolve
* Se há testes e documentação atualizados
5. Aguarde revisão dos colegas ou mantenedores.
6. Responda aos comentários e aplique modificações solicitadas.
7. Após aprovação, o PR será mergeado.

## Padrões de Código e Organização
* Estrutura de pastas:

```text
source/
  ├── episodio/
  │   ├── model_episodio.py
  │   ├── view_episodio.py
  │   ├── controller_episodio.py
  │   └── teste_episodio.py
```
* Cada entidade deve possuir:
  * Model (camada de dados via SQLAlchemy)
  * Controller (regras de negócio)
  * View (rotas FastAPI)
  * Testes relacionados

* O código deve ser modular e documentado.

## Revisão de Código (Code Review)
Durante a revisão:
* Priorize legibilidade e clareza.
* Verifique nomes de variáveis e funções.
* Garanta que funções façam apenas uma tarefa.
* Avalie o impacto na performance e segurança.
* Sempre prefira código explícito, não implícito.

## Ferramentas de Qualidade

Função           |  Ferramenta              
-----------------+--------------------------
Linter           |  Ruff                    
Formatação       |  Prettier (para frontend)
Tipagem          |  Mypy                    
Testes           |  Pytest                  
CI/CD            |  GitHub Actions          
Containerização  |  Docker                  

## Código de Conduta
Este projeto segue o [Contributor Covenant](https://www.contributor-covenant.org/).
Seja respeitoso, colaborativo e evite comportamento tóxico. Todos devem se sentir bem-vindos para contribuir.

## Agradecimento

Sua colaboração é essencial para tornar o Diário de Enxaqueca mais robusto, acessível e útil.
Cada contribuição melhora a experiência de quem sofre com enxaquecas e busca entender seus gatilhos.
Muito obrigado por fazer parte deste projeto!
