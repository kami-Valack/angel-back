# Como rodar as migrations

1. Abra o terminal na raiz do projeto.
2. Execute o comando abaixo para importar as tabelas no seu banco MySQL:

```sh
mysql -u root -p codefy < app/migrations.sql
```

- Altere o nome do banco (`codefy`) se necessário.
- O script criará as tabelas: users, courses, modules, lessons, resources.
