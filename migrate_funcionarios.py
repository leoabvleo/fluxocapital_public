"""
Script de migração para criar as tabelas do módulo de Funcionários.
Execute: python migrate_funcionarios.py
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app, db
from models import Funcionario, FuncionarioLancamento, FolhaPagamento

with app.app_context():
    db.create_all()
    print("✓ Tabelas criadas (ou já existiam):")
    print("  - funcionarios")
    print("  - funcionario_lancamentos")
    print("  - folha_pagamentos")
    print("Migração concluída com sucesso!")
