# Política de Segurança — NexVigil

**Versão aplicável:** NexVigil v1.0.0

## Escopo

O NexVigil é um laboratório educacional de cibersegurança desenvolvido para execução em ambientes locais e controlados.

## Uso autorizado

As funcionalidades ofensivas devem ser utilizadas exclusivamente em:

- localhost;
- interfaces de loopback;
- ambientes pertencentes ao operador;
- sistemas com autorização explícita para testes.

Os scripts de simulação possuem restrições para impedir o uso arbitrário contra alvos externos.

## Dados

O projeto utiliza dados sintéticos.

Credenciais reais, tokens, chaves de API e outros segredos não devem ser armazenados no repositório.

Configurações sensíveis devem permanecer em arquivos locais como `.env`.

O arquivo `.env` é excluído do versionamento.

## Telemetria

Os eventos de segurança podem conter:

- identificadores de evento;
- timestamps;
- usernames sintéticos;
- endereço de origem;
- resultado da autenticação;
- serviço.

Senhas não são gravadas nos logs.

## Desenvolvimento seguro

O projeto utiliza:

- testes automatizados com Pytest;
- Bandit para SAST;
- pip-audit para auditoria de dependências;
- GitHub Actions para CI;
- princípio de menor privilégio;
- Secure by Default;
- Defense in Depth.

## Vulnerabilidades

Caso uma vulnerabilidade seja identificada, ela deve ser analisada e tratada antes da inclusão de novos recursos relacionados.

Problemas de segurança não devem ser explorados contra sistemas de terceiros.

## Disclaimer

NexVigil foi desenvolvido para aprendizado, pesquisa defensiva e validação de segurança em ambientes autorizados.

O responsável pela execução deve garantir que possui autorização para testar qualquer sistema fora do laboratório local.