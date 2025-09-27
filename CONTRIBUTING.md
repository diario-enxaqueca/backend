## Contributing to Diário de Enxaqueca – Backend

Obrigado por seu interesse em contribuir para o backend do Diário de Enxaqueca! Este documento descreve as diretrizes para contribuir com o projeto de forma organizada e consistente.

---

##  Como contribuir
#### Clonar o repositório

Clone o repositório localmente:
```bash
git clone https://github.com/sua-org/diario-enxaqueca-backend.git
cd diario-enxaqueca-backend
```

#### Criar branch

Crie uma nova branch a partir da branch principal (main):
```bash
git checkout main
git pull
git checkout -b feature/nome-da-feature
```

Use nomes de branch descritivos, por exemplo: `feature/criar-registro` ou `bugfix/fix-login`.

#### Fazer commits

Siga o padrão de Conventional Commits para manter consistência:
```php-template
<tipo>[escopo opcional]: <descrição>
```

Exemplos de tipos:

* `feat` – Nova funcionalidade
* `fix` – Correção de bug
* `docs` – Atualização de documentação
* `style` – Ajustes de formatação, sem mudança de lógica
* `refactor` – Refatoração de código
* `test` – Adição ou correção de testes

#### Exemplo de commit:
```bash
git commit -m "feat(registro): adiciona endpoint para criar registro"
```

#### Abrir Pull Request

1. Faça push da branch:
```bash
git push origin feature/nome-da-feature
```
2. Acesse o repositório no GitHub e abra um Pull Request da sua branch para a main.
3. Forneça uma descrição clara e detalhada do que foi feito.
4. Aguarde revisão e comentários antes de merge.

---

## Boas práticas

* Siga o padrão MVC já definido no projeto.
* Mantenha código limpo, organizado e consistente com Clean Code e SOLID.
* Escreva testes unitários sempre que adicionar funcionalidades.
* Atualize a documentação se necessário.
* Certifique-se de que o projeto builda e roda corretamente com Docker após suas alterações.

## Agradecimento

Agradecemos suas contribuições! Cada melhoria ajuda a tornar o Diário de Enxaqueca mais funcional, seguro e fácil de manter.