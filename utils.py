from flask import request, session
from flask_login import current_user
from auth import is_superadmin, is_admin_or_superadmin
from extensions import db
from models import Carteira

def get_current_wallet():
    """Helper para obter a carteira ativa (ou lista delas) priorizando a URL e depois a Sessão."""
    c_list = request.args.getlist('carteira')
    if c_list:
        if len(c_list) == 1 and c_list[0] == 'Consolidada':
            c_ativa = 'Consolidada'
        else:
            if 'Consolidada' in c_list:
                c_ativa = 'Consolidada'
            else:
                c_ativa = c_list if len(c_list) > 1 else c_list[0]
        # Persiste na sessão para que links sem parâmetros mantenham a seleção
        session['carteira_ativa'] = c_ativa
        return c_ativa
    return session.get('carteira_ativa', 'Consolidada')

def get_authorized_query(model, c_ativa):
    """Retorna uma query filtrada pelas permissões do usuário e carteira ativa.
    
    SuperAdmin: acesso irrestrito a todos os dados.
    Admin: acesso às suas carteiras atribuídas (com escrita).
    Usuário: acesso somente leitura às suas carteiras atribuídas.
    """
    query = model.query
    
    # Se c_ativa for uma lista, tratamos a consolidação dessas carteiras
    if isinstance(c_ativa, list):
        if is_superadmin():
            if 'Consolidada' in c_ativa:
                return query
            
            c_objs = Carteira.query.filter(Carteira.nome.in_(c_ativa)).all()
            c_ids = [c.id for c in c_objs]
            if hasattr(model, 'carteira_id'):
                return query.filter(model.carteira_id.in_(c_ids))
            else:
                return query.filter(model.carteira.in_(c_ativa))
        else:
            # Filtra apenas pelas carteiras que o usuário tem acesso
            acessivel = [c.nome for c in current_user.carteiras]
            permitidas = [nome for nome in c_ativa if nome in acessivel]
            
            if not permitidas:
                return query.filter(False)
            
            c_objs = Carteira.query.filter(Carteira.nome.in_(permitidas)).all()
            c_ids = [c.id for c in c_objs]
            
            if hasattr(model, 'carteira_id'):
                return query.filter(model.carteira_id.in_(c_ids))
            else:
                return query.filter(model.carteira.in_(permitidas))

    # SuperAdmin tem acesso total — sem filtro de carteira
    if is_superadmin():
        if c_ativa != 'Consolidada':
            c_obj = Carteira.query.filter_by(nome=c_ativa).first()
            if c_obj:
                if hasattr(model, 'carteira_id'):
                    return query.filter_by(carteira_id=c_obj.id)
                else:
                    return query.filter_by(carteira=c_ativa)
            return query.filter(False)
        return query  # 'Consolidada' = todos os dados para SuperAdmin
    
    if c_ativa == 'Consolidada':
        # Admin e Usuário: filtrar pelas carteiras atribuídas
        wallet_ids = [c.id for c in current_user.carteiras]
        if wallet_ids:
            if hasattr(model, 'carteira_id'):
                return query.filter(model.carteira_id.in_(wallet_ids))
            else:
                wallet_nomes = [c.nome for c in current_user.carteiras]
                return query.filter(model.carteira.in_(wallet_nomes))
        return query.filter(False)
    else:
        # Carteira específica
        c_obj = Carteira.query.filter_by(nome=c_ativa).first()
        if c_obj:
            # Verifica se o usuário tem acesso a essa carteira
            if not is_admin_or_superadmin() or (current_user.perfil and current_user.perfil.nome == 'Admin'):
                if c_obj not in current_user.carteiras:
                    return query.filter(False)
            
            if hasattr(model, 'carteira_id'):
                return query.filter_by(carteira_id=c_obj.id)
            else:
                return query.filter_by(carteira=c_ativa)
        else:
            return query.filter(False)
    return query
