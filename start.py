#!/usr/bin/env python3
"""
Script para iniciar o ENEM Tutor System
"""
import subprocess
import sys
import time
import webbrowser
from pathlib import Path
import os

def run_command(cmd, background=False):
    """Executa um comando"""
    if background:
        return subprocess.Popen(cmd, shell=True)
    else:
        return subprocess.run(cmd, shell=True)

def main():
    print("🚀 Iniciando ENEM Tutor System...")
    
    # Verificar se está no diretório correto
    if not Path("src/api.py").exists():
        print("❌ Execute este script no diretório raiz do projeto")
        sys.exit(1)
    
    # Verificar .env
    if not Path("config/.env").exists():
        print("❌ Arquivo config/.env não encontrado")
        sys.exit(1)
    
    try:
        # Parar processos anteriores
        print("🛑 Parando processos anteriores...")
        run_command("pkill -f 'python.*api.py' 2>/dev/null || true")
        run_command("pkill -f 'streamlit.*frontend' 2>/dev/null || true")
        time.sleep(2)
        
        # Configurar variável de ambiente
        os.environ['PYTHONPATH'] = os.getcwd()
        
        # Iniciar API
        print("🔧 Iniciando API...")
        api_process = run_command("cd src && python api.py", background=True)
        time.sleep(3)
        
        # Iniciar Frontend
        print("🎨 Iniciando interface...")
        frontend_process = run_command("cd src && streamlit run frontend.py --server.port=8501", background=True)
        time.sleep(3)
        
        print("\n✅ Sistema iniciado!")
        print("🌐 Interface: http://localhost:8501")
        print("🔧 API: http://localhost:8000")
        print("\n📖 Abrindo navegador...")
        
        # Abrir navegador
        webbrowser.open("http://localhost:8501")
        
        print("\n⏹️  Para parar: Ctrl+C")
        
        # Aguardar interrupção
        try:
            api_process.wait()
        except KeyboardInterrupt:
            print("\n🛑 Parando...")
            api_process.terminate()
            frontend_process.terminate()
            
    except Exception as e:
        print(f"❌ Erro: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()