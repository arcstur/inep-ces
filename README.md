# inep-analise-ces
Análise dos microdados do Censo da Educação Superior do INEP

Por padrão a análise é feita para o curso de Arquitetura e Urbanismo, no estado do Rio Grande do Sul. Isso pode ser configurado com variáveis de ambiente.

## Cálculo de concluintes em um dado ano

Baixe o arquivo dos microdados em um csv, configure as variáveis de ambiente, e rode o script `concluintes.py`

## Configuração

As seguintes variáveis de ambiente definem o programa.
- `CSV_FILENAME` (default `2021.csv`): nome do arquivo (deve ser um microdado do CES do INEP)
- `SG_UF` (default `RS`): sigla da UF
- `NO_CURSO` (default `Arquitetura E Urbanismo`): nome do curso
