# Mensagens do sistema

Todas as mensagens exibidas ao usuário ficam centralizadas aqui e são referenciadas nos
casos de uso pelo identificador (`MSG01`), nunca pelo texto. Assim, alterar uma mensagem
usada em oito casos de uso é uma edição só — e a internacionalização já nasce pronta.

| ID | Tipo | Texto (pt-BR) | Usada em |
|---|---|---|---|
| MSG01 | Sucesso | \<texto\> | UC1, UC2 |
| MSG02 | Erro | \<texto\> | UC1 |
| MSG03 | Confirmação | \<texto\> | UC3 |

## Espelhamento no código

Mantenha um arquivo por idioma, com as mesmas constantes:

```python
# lang/pt-br.py
MSG01 = 'Produto cadastrado com sucesso.'
MSG02 = 'Não foi possível cadastrar o produto. Tente novamente mais tarde.'
```

```python
# lang/en-us.py
MSG01 = 'Product successfully registered.'
MSG02 = 'Unable to register the product. Try again later.'
```

Ao adicionar uma mensagem, atualize esta tabela **e** todos os arquivos de idioma. Uma
constante presente em um idioma e ausente em outro quebra a interface silenciosamente.

---
*Última revisão: AAAA-MM-DD | Responsável: \<nome\>*
