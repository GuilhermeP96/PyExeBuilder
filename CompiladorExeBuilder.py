import json
import os
import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
import ast

# Função para ler as configurações do arquivo JSON
def ler_configuracao(caminho_cfg):
    with open(caminho_cfg, 'r', encoding='utf-8') as f:
        return json.load(f)

# Função para selecionar um arquivo
def selecionar_arquivo(titulo, filetypes):
    root = tk.Tk()
    root.withdraw()  # Esconde a janela principal do Tkinter
    arquivo_selecionado = filedialog.askopenfilename(title=titulo, filetypes=filetypes)
    return arquivo_selecionado

# Função para selecionar um diretório
def selecionar_diretorio(titulo):
    root = tk.Tk()
    root.withdraw()  # Esconde a janela principal do Tkinter
    diretorio_selecionado = filedialog.askdirectory(title=titulo)
    return diretorio_selecionado

# Função para detectar imports ocultos (hidden imports) automaticamente
def detectar_hidden_imports(arquivo_py):
    hidden_imports = set()

    # Analisar o script Python para detectar imports dinâmicos
    with open(arquivo_py, 'r', encoding='utf-8') as file:
        tree = ast.parse(file.read(), filename=arquivo_py)
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    hidden_imports.add(alias.name)
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    hidden_imports.add(node.module)

    # Incluir manualmente módulos padrão que possam ser necessários
    hidden_imports.update(['secrets', 'oracledb', 'platform', 'os', 'sys'])

    return list(hidden_imports)

# Função para detectar dependências de pacotes com pip freeze
def detectar_dependencias_requeridas():
    try:
        # Usa pip freeze para listar todos os pacotes instalados no ambiente
        result = subprocess.run(['pip', 'freeze'], stdout=subprocess.PIPE, text=True)
        dependencies = [line.split('==')[0].strip() for line in result.stdout.splitlines()]
        return dependencies
    except Exception as e:
        print(f"Erro ao detectar dependências requeridas: {e}")
        return []

# Função para criar o arquivo .spec personalizado
def criar_arquivo_spec(config, arquivo_py, logo_path=None):
    nome_executavel = config['internal_name']
    icon_line = f"icon='{logo_path}'," if logo_path else ""
    
    # Detectar hidden imports automaticamente
    hiddenimports_auto = detectar_hidden_imports(arquivo_py)
    # Detectar todas as dependências requeridas
    all_dependencies = detectar_dependencias_requeridas()
    
    hiddenimports = list(set(config.get('hiddenimports', []) + hiddenimports_auto + all_dependencies))
    hiddenimports_line = f"hiddenimports={hiddenimports}," if hiddenimports else ""

    # Adicione outros arquivos do projeto ao spec
    datas = config.get('datas', [])
    datas_line = f"datas={datas}," if datas else ""

    spec_content = f"""
# -*- mode: python ; coding: utf-8 -*-

import os

block_cipher = None

a = Analysis(
    ['{arquivo_py}'],
    pathex=[],
    binaries=[],
    {datas_line}
    {hiddenimports_line}
    hookspath=[],
    hooksconfig={{}},
    runtime_hooks=[],
    excludes=[],
    noarchive=False
)
pyz = PYZ(a.pure)
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='{nome_executavel}',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    {icon_line}
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='{nome_executavel}',
    distpath=os.path.dirname(os.path.abspath('{arquivo_py}'))
)
"""
    with open(f'{nome_executavel}.spec', 'w', encoding='utf-8') as f:
        f.write(spec_content)

# Função para executar o PyInstaller com o arquivo .spec gerado
def executar_pyinstaller(nome_spec):
    subprocess.run(['pyinstaller', '--noconfirm', nome_spec])

# Função para assinar o executável com signtool
def assinar_executavel(executavel, config):
    signtool_path = config['sign_tool_path']
    timestamp_url = config['timestamp_url']
    sha_type = config['sha_type']
    subprocess.run([
        signtool_path, 'sign', '/a',
        '/tr', timestamp_url,
        '/td', sha_type, '/fd', sha_type,
        '/v', executavel
    ])

def main():
    # Selecionar o arquivo Python principal
    arquivo_py = selecionar_arquivo("Selecione o arquivo Python principal", [("Python Files", "*.py")])
    if not arquivo_py:
        print("Nenhum arquivo Python selecionado.")
        return

    # Selecionar o arquivo JSON de configuração
    arquivo_cfg = selecionar_arquivo("Selecione o arquivo JSON de configuração", [("JSON Files", "*.json")])
    if not arquivo_cfg:
        print("Nenhum arquivo JSON selecionado.")
        return

    # Ler as configurações do arquivo JSON
    config = ler_configuracao(arquivo_cfg)

    # Perguntar se deseja adicionar um logo personalizado
    add_logo = messagebox.askyesno("Adicionar Logo", "Deseja adicionar um logo personalizado?")
    logo_path = None
    if add_logo:
        logo_path = selecionar_arquivo("Selecione o arquivo de logo", [("Image Files", "*.ico;*.png;*.jpg")])
        if not logo_path:
            print("Nenhum logo selecionado.")
            return

    # Criar o arquivo .spec personalizado
    criar_arquivo_spec(config, arquivo_py, logo_path)

    # Nome do arquivo .spec gerado
    nome_spec = f"{config['internal_name']}.spec"

    # Executar o PyInstaller com o arquivo .spec gerado
    executar_pyinstaller(nome_spec)

    # Perguntar se deseja assinar digitalmente
    sign_exe = messagebox.askyesno("Assinar Digitalmente", "Deseja assinar digitalmente o executável?")
    if sign_exe:
        # Caminho do executável gerado
        executavel_gerado = os.path.join(os.path.dirname(os.path.abspath(arquivo_py)), 'dist', config['internal_name'], config['internal_name'] + '.exe')

        # Assinar o executável
        assinar_executavel(executavel_gerado, config)

    print(f"Processamento concluído. O executável foi gerado com base no arquivo {arquivo_py} e na configuração {arquivo_cfg}.")

if __name__ == '__main__':
    main()
