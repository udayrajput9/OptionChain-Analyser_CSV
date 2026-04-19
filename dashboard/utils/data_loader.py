import os
import re
import pandas as pd
from pathlib import Path
from datetime import datetime
import shutil

# Compute stocks dir relative to this file:
# data_loader.py is at: dashboard/utils/data_loader.py
# manage.py is at:       optionchain_project/manage.py
# stocks/ is at:         optionchain_project/stocks/
_THIS_FILE = Path(__file__).resolve()
_PROJECT_ROOT = _THIS_FILE.parent.parent.parent  # goes up: utils -> dashboard -> optionchain_project

def get_stocks_dir() -> Path:
    """stocks/ folder ka path — always relative to manage.py location"""
    stocks = _PROJECT_ROOT / "stocks"
    return stocks


def get_stock_dir(stock_symbol: str) -> Path:
    return get_stocks_dir() / stock_symbol.strip().upper()

def get_available_stocks() -> list[str]:
    """stocks/ folder mein jo bhi subfolders hain unke naam return karo"""
    stocks_dir = get_stocks_dir()
    if not stocks_dir.exists():
        return []
    return sorted([
        d.name for d in stocks_dir.iterdir()
        if d.is_dir() and not d.name.startswith('.')
    ])

def extract_date_from_csv(filepath: Path) -> str | None:
    """CSV ke header se download date extract karo"""
    try:
        with open(filepath, 'r', encoding='utf-8-sig') as f:
            for line in f:
                line = line.strip()
                # "# Downloaded: 18/4/2026, 12:45:04 pm"
                if line.startswith('# Downloaded:'):
                    date_part = line.replace('# Downloaded:', '').strip()
                    return date_part.split(',')[0].strip()  # sirf date, time nahi
                if not line.startswith('#'):
                    break  # headers khatam
    except Exception:
        pass
    return None


def parse_date_label(date_label: str | None):
    if not date_label:
        return None
    for fmt in ('%d/%m/%Y', '%d/%m/%y'):
        try:
            return datetime.strptime(date_label.strip(), fmt).date()
        except ValueError:
            continue
    return None

def get_available_files(stock_symbol: str) -> list[dict]:
    """
    Ek stock ke folder mein jo bhi CSV files hain — dynamically detect karo.
    Returns: sorted list of dicts — [{number, filename, path, date_label}]
    Jo bhi files hain, sirf wohi — koi assumption nahi count ke baare mein.
    """
    stock_dir = get_stock_dir(stock_symbol)
    
    if not stock_dir.exists():
        raise FileNotFoundError(
            f"'{stock_symbol}' ka folder nahi mila. "
            f"Banao: stocks/{stock_symbol.upper()}/ "
            f"aur CSV files daalo format mein: 1_{stock_symbol}.csv"
        )
    
    files = []
    for f in stock_dir.iterdir():
        if f.suffix.lower() != '.csv':
            continue
        
        # Number extract karo filename se
        match = re.match(r'^(\d+)', f.name)
        if not match:
            # Try end mein number
            match = re.search(r'(\d+)\.csv$', f.name, re.IGNORECASE)
        
        if match:
            number = int(match.group(1))
        else:
            # Number nahi mila — skip karo with warning
            print(f"Warning: '{f.name}' mein number nahi mila, skip ho raha hai.")
            continue
        
        # Metadata extract karo (download date)
        date_label = extract_date_from_csv(f)
        
        files.append({
            'number': number,
            'filename': f.name,
            'path': str(f),
            'date_label': date_label or f"File #{number}",
            'is_latest': False  # baad mein set hongi
        })
    
    if not files:
        return []  # Empty list return karo — crash nahi hoga
    
    # Number ke hisaab se sort karo (1 = oldest, N = latest)
    files.sort(key=lambda x: x['number'])
    
    # Latest file mark karo
    if files:
        files[-1]['is_latest'] = True
    
    return files

def get_latest_file(stock_symbol: str) -> dict:
    """Sabse latest (highest numbered) file return karo"""
    files = get_available_files(stock_symbol)
    return files[-1]  # Already sorted, last = latest

def get_file_by_number(stock_symbol: str, number: int) -> dict:
    """Specific number ki file return karo"""
    files = get_available_files(stock_symbol)
    for f in files:
        if f['number'] == number:
            return f
    available = [f['number'] for f in files]
    raise FileNotFoundError(
        f"File #{number} nahi mili {stock_symbol} ke liye. "
        f"Available files: {available}"
    )

def get_file_count(stock_symbol: str) -> int:
    """Kitni files hain — dynamic"""
    return len(get_available_files(stock_symbol))

def load_historical_data(stock_symbol: str, last_n: int = None) -> list[pd.DataFrame]:
    """
    last_n: kitni latest files chahiye. None = saari files.
    Return: List of DataFrames (oldest → newest)
    """
    from dashboard.utils.data_cleaner import parse_option_chain_csv
    
    files = get_available_files(stock_symbol)
    
    if last_n is not None:
        files = files[-last_n:]  # last N files lo
    
    dataframes = []
    for file_info in files:
        try:
            df, meta = parse_option_chain_csv(file_info['path'])
            df['_file_number'] = file_info['number']
            df['_date_label'] = file_info['date_label']
            df['_is_latest'] = file_info['is_latest']
            dataframes.append({'data': df, 'meta': meta})
        except Exception as e:
            print(f"Warning: {file_info['filename']} load nahi hua — {e}")
            continue
    
    return dataframes


def load_historical_data_until(stock_symbol: str, upto_number: int, last_n: int = None):
    files = [f for f in get_available_files(stock_symbol) if f['number'] <= upto_number]
    if last_n is not None:
        files = files[-last_n:]

    from dashboard.utils.data_cleaner import parse_option_chain_csv

    dataframes = []
    for file_info in files:
        try:
            df, meta = parse_option_chain_csv(file_info['path'])
            df['_file_number'] = file_info['number']
            df['_date_label'] = file_info['date_label']
            df['_is_latest'] = file_info['is_latest']
            dataframes.append({'data': df, 'meta': meta, 'file_info': file_info})
        except Exception as e:
            print(f"Warning: {file_info['filename']} load nahi hua — {e}")
            continue
    return dataframes


def save_uploaded_option_chain(stock_symbol: str, uploaded_file) -> dict:
    stock_symbol = stock_symbol.strip().upper()
    stock_dir = get_stock_dir(stock_symbol)
    stock_dir.mkdir(parents=True, exist_ok=True)

    existing = get_available_files(stock_symbol) if stock_dir.exists() else []
    next_number = (existing[-1]['number'] + 1) if existing else 1
    safe_name = f"{next_number}_{stock_symbol}_OptionChain.csv"
    target_path = stock_dir / safe_name

    with open(target_path, 'wb+') as destination:
        for chunk in uploaded_file.chunks():
            destination.write(chunk)

    date_label = extract_date_from_csv(target_path)
    return {
        'number': next_number,
        'filename': safe_name,
        'path': str(target_path),
        'date_label': date_label or f"File #{next_number}",
        'is_latest': True,
    }


def reset_stock_files(stock_symbol: str):
    stock_dir = get_stock_dir(stock_symbol)
    stock_dir.mkdir(parents=True, exist_ok=True)
    removed = 0
    for item in stock_dir.iterdir():
        if item.is_file():
            item.unlink()
            removed += 1
    return removed


def delete_stock_card_files(stock_symbol: str):
    stock_dir = get_stock_dir(stock_symbol)
    if not stock_dir.exists():
        return False
    shutil.rmtree(stock_dir)
    return True
