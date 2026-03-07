import requests
import logging
from datetime import datetime
from app import app, db, Ativo
from sqlalchemy import text

# Configuração de logging básica para o console
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def get_price(ticker, headers):
    try:
        url = f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}?interval=1d&range=1d"
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        dados = response.json()
        if dados and 'chart' in dados and dados['chart']['result']:
            result = dados['chart']['result'][0]
            if 'meta' in result and 'regularMarketPrice' in result['meta']:
                return float(result['meta']['regularMarketPrice'])
    except Exception as e:
        logging.debug(f"Erro ao buscar preço para {ticker}: {e}")
    return None

def get_pvp(ticker):
    try:
        url = f"https://content.btgpactual.com/api/research/public-router/content-hub-assets/v1/asset-indicators/{ticker}?periodFilter=LAST_12_MONTHS&locale=pt-BR"
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        response = requests.get(url, headers=headers, timeout=15)
        if response.status_code == 200:
            data = response.json()
            for cat in data.get('categories', []):
                for ind in cat.get('indicators', []):
                    if ind.get('indicator', {}).get('indicator') in ['PRICE_TO_BOOK_VALUE', 'PRICE_TO_BOOK_VALUE_REIT']:
                        if ind.get('data') and len(ind['data']) > 0:
                            return float(ind['data'][-1][1])
    except Exception:
        pass
    return None

def atualizar():
    with app.app_context():
        try:
            logging.info(f"--- Início da Atualização: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')} ---")
            
            ativos = Ativo.query.all()
            if not ativos:
                logging.warning("Nenhum ativo encontrado no banco de dados.")
                return

            # Agrupar tickers e categorias, limpando o ticker
            tickers_to_update = {}
            for a in ativos:
                clean_ticker = a.ticker.strip().upper()
                if clean_ticker != a.ticker:
                    logging.info(f"Corrigindo ticker com espaços: '{a.ticker}' -> '{clean_ticker}'")
                    a.ticker = clean_ticker
                
                if clean_ticker not in tickers_to_update:
                    tickers_to_update[clean_ticker] = a.categoria
                elif a.categoria == 'Internacional':
                    tickers_to_update[clean_ticker] = 'Internacional'

            db.session.commit()

            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
            
            # Buscar cotação do Dólar
            usd_brl = get_price("USDBRL=X", headers)
            if usd_brl:
                logging.info(f"[CÂMBIO] USDBRL: R$ {usd_brl:.4f}")
            else:
                logging.warning("[CÂMBIO] Erro ao buscar dólar. Usando 5.00 como fallback.")
                usd_brl = 5.00

            for ticker, categoria in tickers_to_update.items():
                preco_final = None
                pvp_final = None
                
                try:
                    if categoria == 'Internacional':
                        preco_raw = get_price(ticker, headers)
                        if preco_raw:
                            preco_final = preco_raw * usd_brl
                            logging.info(f"[{ticker}] US$ {preco_raw:.2f} -> R$ {preco_final:.2f}")
                    else:
                        ticker_yahoo = f"{ticker}.SA"
                        preco_final = get_price(ticker_yahoo, headers)
                        pvp_final = get_pvp(ticker)
                        
                        if preco_final:
                            msg = f"[{ticker}] R$ {preco_final:.2f}"
                            if pvp_final: msg += f" | P/VP: {pvp_final:.2f}"
                            logging.info(msg)

                    if preco_final is not None:
                        update_values = {"preco_atual": preco_final}
                        if pvp_final is not None:
                            update_values["pvp"] = pvp_final
                        
                        # Update em massa para o ticker
                        db.session.query(Ativo).filter(Ativo.ticker == ticker).update(update_values, synchronize_session=False)

                except Exception as e:
                    logging.error(f"[{ticker}] Erro ao processar: {e}")

            db.session.commit()
            logging.info(f"--- Fim da Atualização: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')} ---")

        except Exception as e:
            logging.error(f"Erro geral durante a atualização: {e}")

if __name__ == "__main__":
    atualizar()

