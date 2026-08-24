# NexVigil — Security Rules

Estas regras são obrigatórias.

1. Nenhum segredo real em código, logs, exemplos ou commits.
2. `.env`, credenciais e Terraform state nunca entram no Git.
3. Attack Range nunca deve ficar exposto publicamente por padrão.
4. Scripts ofensivos devem operar apenas contra ambiente próprio/autorizado.
5. Dados usados em demonstrações devem ser sintéticos.
6. Containers não devem usar privilégios desnecessários.
7. Evitar host mounts desnecessários.
8. Serviços administrativos devem fazer bind em localhost quando possível.
9. Toda entrada externa deve ser validada.
10. Logs devem remover tokens, senhas e headers sensíveis.
11. Dependências devem ser verificadas por SCA.
12. Pipeline deve executar secret scanning e SAST.
13. IA não recebe shell arbitrário.
14. IA não recebe credenciais administrativas.
15. IA recomenda; policy engine valida; humano aprova ações críticas.
16. Toda automação de resposta deve possuir rollback.
17. Falso positivo deve ser considerado no desenho de detecções.
18. Cloud deve seguir least privilege e ser destruída quando não necessária.
19. Nenhum cenário ofensivo deve atingir terceiros.
20. Falhas conhecidas devem ser registradas e tratadas, não escondidas.
