# Personal LLM Agent Framework

Um framework de agente autônomo de IA construído com Python que permite ao modelo de linguagem (Google Gemini) agir como um agente capaz de executar tarefas complexas de forma independente.

## Visão Geral

Este projeto implementa um **Agente de IA Autônomo** que pode:
- Navegar pelo sistema de arquivos
- Ler e escrever arquivos
- Executar scripts Python
- Tomar decisões baseadas nos resultados de suas ações
- Completar tarefas complexas através de múltiplas iterações

O agente opera em um loop contínuo onde analisa a tarefa, executa ações, avalia os resultados e continua até completar o objetivo.

## Técnicas Implementadas

### Function Calling (Tool Use)

Técnica avançada que permite ao LLM invocar funções Python de forma estruturada. Cada função possui um schema definido que o modelo utiliza para fazer chamadas corretas, permitindo que o agente interaja com o sistema de forma controlada.

### Agentic Loop

Loop autônomo que permite ao LLM operar de forma independente. O agente mantém histórico completo da conversa, possui limite de iterações para prevenir loops infinitos, e encerra automaticamente quando decide que a tarefa está completa.

### Sandboxing de Segurança

Todas as operações de arquivo são validadas para prevenir ataques de **Directory Traversal**. O agente só pode operar dentro do diretório de trabalho designado, garantindo isolamento e segurança.

### Dynamic Function Dispatch

Padrão de dispatch dinâmico que mapeia chamadas do LLM para funções Python através de um dicionário de funções, permitindo extensibilidade e manutenção simplificada.

### Process Execution

Execução segura de scripts Python com timeout e captura de output (stdout/stderr), permitindo que o agente execute e teste código de forma controlada.

### Message History Management

Gerenciamento do histórico de mensagens para manter contexto multi-turn, permitindo que o agente mantenha consciência de todas as ações anteriores durante a execução de uma tarefa.

## Ferramentas do Agente

| Ferramenta | Descrição |
|------------|-----------|
| `get_files_info` | Lista arquivos em um diretório com metadados |
| `get_file_content` | Lê o conteúdo de um arquivo |
| `write_file` | Cria ou sobrescreve arquivos |
| `run_python_file` | Executa scripts Python e captura o output |

## Estrutura do Projeto

```
personal-llm/
├── main.py                 # Entry point e loop principal do agente
├── call_function.py        # Dispatcher de funções e definições de tools
├── prompt.py               # System prompt para o LLM
├── config.py               # Constantes de configuração
├── functions/              # Implementação das ferramentas
│   ├── get_files_info.py
│   ├── get_file_content.py
│   ├── write_file.py
│   └── run_python_file.py
└── calculator/             # Projeto de exemplo para testes
```

## Tecnologias

- **Python 3.13+**
- **Google Gemini 2.5-Flash** - Modelo de linguagem
- **google-genai** - SDK do Google para Generative AI
- **python-dotenv** - Gerenciamento de variáveis de ambiente

## Instalação

1. Clone o repositório
2. Crie um ambiente virtual e instale as dependências:
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

3. Configure a API key do Google em um arquivo `.env`:
```
GEMINI_API_KEY=sua_api_key
```

## Uso

```bash
python main.py "Sua tarefa aqui"
python main.py --verbose "Sua tarefa aqui"  # modo debug
```

## Fluxo de Execução

```
Usuário fornece tarefa
        │
        ▼
   LLM analisa e responde
        │
        ▼
   Tem function calls? ──SIM──▶ Executa funções
        │                              │
       NÃO                             │
        │                              │
        ▼                              │
   Resposta final ◀────────────────────┘
```

## Aprendizados

Projeto desenvolvido na plataforma [Boot.dev](https://boot.dev), demonstrando:

- Integração com APIs de LLM
- Padrões de Agentes de IA autônomos
- Segurança em aplicações de IA (sandboxing)
- Arquitetura modular e extensível
- Function Calling para estender capacidades de LLMs

---

Desenvolvido como projeto educacional na plataforma [Boot.dev](https://boot.dev)
