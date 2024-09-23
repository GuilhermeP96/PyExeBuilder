
# ExeBuilder - Compilador com HiddenImports

Este projeto é um **compilador personalizado em Python** desenvolvido pela **Guilherme Pinheiro Consultoria e Serviços de T.I.**. Ele automatiza o processo de criação de executáveis usando **PyInstaller**, oferecendo funcionalidades como detecção automática de **imports ocultos** (hidden imports), geração de um arquivo **.spec** customizado e opção de **assinatura digital** de executáveis.

## Funcionalidades

- **Detecção Automática de Hidden Imports:** Detecta automaticamente módulos e pacotes utilizados no código.
- **Geração de Arquivo .spec Personalizado:** Cria um arquivo `.spec` adaptado ao seu projeto.
- **Execução do PyInstaller:** Automatiza a criação de executáveis com base no arquivo `.spec`.
- **Assinatura Digital de Executáveis:** Oferece a opção de assinar digitalmente os executáveis utilizando **signtool**.
- **Interface Gráfica Simples:** Utiliza **Tkinter** para facilitar a interação com o usuário para seleção de arquivos e diretórios.

## Estrutura do Projeto

- **Arquivo Principal:** `Compilador - ExeBuilder - HiddenImports.py`
- **Arquivo de Configuração:** Exemplo de arquivo de configuração JSON (detalhado abaixo).

## Exemplo de Arquivo de Configuração (JSON)

O arquivo de configuração JSON é utilizado para definir os detalhes do executável, como nome do produto, versão e caminho para o **signtool** (caso deseje assinar digitalmente o executável).

```json
{
    "company_name": "Guilherme Pinheiro Consultoria e Serviços de T.I.",
    "file_description": "Compilador de scripts e projetos em Python",
    "file_version": "1.0.0.0",
    "internal_name": "Compilador de scripts e projetos em Python",
    "legal_copyright": "©2024 Guilherme Pinheiro Consultoria e Serviços de T.I.",
    "original_filename": "Compilador de scripts e projetos em Python",
    "product_name": "Compilador de scripts e projetos em Python",
    "product_version": "1.0.0.0",
    "sign_tool_path": "C:\\Program Files (x86)\\Windows Kits\\10\\bin\\10.0.19041.0\\x64\\signtool.exe",
    "timestamp_url": "http://timestamp.digicert.com",
    "sha_type": "SHA256"
}
```

## Requisitos

Para rodar o projeto, é necessário ter as seguintes dependências instaladas:

- **Python 3.6+**
- **Tkinter** (para a interface gráfica)
- **PyInstaller**
- **signtool** (opcional, para assinatura digital)

Instale todas as dependências utilizando o arquivo `requirements.txt`:

```bash
pip install -r requirements.txt
```

Conteúdo do `requirements.txt`:

```
tkinter
PyInstaller
```

## Como Usar

1. Clone este repositório:

   ```bash
   git clone https://github.com/seuusuario/ExeBuilder.git
   ```

2. Execute o script principal:

   ```bash
   python CompiladorExeBuilder.py
   ```

3. Na interface gráfica, selecione o arquivo Python principal, o arquivo de configuração JSON e, opcionalmente, um logo para o executável.

4. O executável será gerado na pasta `dist`.

5. Caso deseje assinar o executável, siga as instruções da interface para assinar digitalmente com **signtool**.

## Melhorias Futuras

- Continuo aprimorando a detecção de **hidden imports** e a inclusão de dependências de forma automática. O projeto já está funcional, mas alguns ajustes ainda estão sendo feitos para cobrir mais casos de imports ocultos.
