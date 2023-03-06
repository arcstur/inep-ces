# inep-analise-ces
Análise dos microdados do Censo da Educação Superior do INEP

Por padrão a análise é feita para o curso de Arquitetura e Urbanismo, no estado do Rio Grande do Sul. Isso pode ser configurado com variáveis de ambiente.

## Cálculo de concluintes por ano

Baixe o arquivo dos microdados em um csv, configure as variáveis de ambiente, e rode o script `concluintes.py`

## Configuração

As seguintes variáveis de ambiente definem o programa.
- `NO_CURSO` (default `ARQUITETURA E URBANISMO`): nome do curso, em caixa alta.
- `SG_UF` (default `RS`): sigla da UF
- `PLOT_ACTION` (default `EXPORT`): ação a realizar com os gráficos: `EXPORT` os salva e `SHOW` os mostra.
- `PYTHON_LOG` (default `INFO`): define o [nível do log](https://docs.python.org/3/howto/logging.html#when-to-use-logging) do `logging` do python
