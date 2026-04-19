import pandas as pd
import numpy as np
import re


def _safe_numeric(val, default=0.0):
    return float(val) if pd.notna(val) else default


def _safe_mean(series):
    cleaned = series.dropna()
    return float(cleaned.mean()) if not cleaned.empty else 0.0

def _to_float(val):
    """Convert a messy string value to float — handles commas, dashes, unicode minus."""
    if pd.isna(val) or val is None:
        return np.nan
    s = str(val).strip()
    if s in ('', '—', '-', 'N/A', 'n/a'):
        return np.nan
    # Remove surrounding quotes
    s = s.strip('"')
    # Replace unicode minus '−' with regular minus
    s = s.replace('\u2212', '-')
    # Remove commas (thousands separator)
    s = s.replace(',', '')
    # Remove % signs
    s = s.replace('%', '')
    try:
        return float(s)
    except (ValueError, TypeError):
        return np.nan


def parse_option_chain_csv(filepath: str):
    """
    Parses the WYSIWYG Option Chain CSV format exported from NSE/TradingView.
    Handles:
    - Metadata comment lines starting with #
    - Embedded stock price line like 'TCS 2,581.50 INR +4.60 +0.18%'
    - Expiry section headers like 'April 28 10 DTE'
    - Numbers with commas (e.g., "2,400" -> 2400)
    - Unicode minus signs in negative values
    - Quoted fields with commas
    Returns: (df, metadata)
    """
    metadata = {
        'symbol': 'UNKNOWN',
        'expiry': '',
        'underlying_price': 0.0,
        'download_time': '',
        'atm_strike': 0.0
    }

    raw_lines = []
    with open(filepath, 'r', encoding='utf-8-sig') as f:
        raw_lines = f.readlines()

    headers = []
    data_rows = []
    found_header = False

    for line in raw_lines:
        stripped = line.strip()

        # Skip blank lines
        if not stripped:
            continue

        # Metadata lines
        if stripped.startswith('#'):
            if 'Symbol:' in stripped:
                metadata['symbol'] = stripped.split(':', 1)[1].strip()
            elif 'Expiry:' in stripped:
                metadata['expiry'] = stripped.split(':', 1)[1].strip()
            elif 'Downloaded:' in stripped:
                metadata['download_time'] = stripped.split(':', 1)[1].strip()
            continue

        # Calls/Puts header line - skip it
        if stripped.lower().startswith('calls,') or stripped.lower().startswith('"calls"'):
            continue

        # Detect column header line - it starts with Rho,Vega,...
        if stripped.startswith('Rho,Vega'):
            # Build column names: before Strike = C_ prefix, Strike = Strike, after = P_ prefix
            raw_cols = _parse_csv_row(stripped)
            new_cols = []
            found_strike = False
            for col in raw_cols:
                c = col.strip().strip('"')
                if c.lower() == 'strike':
                    new_cols.append('Strike')
                    found_strike = True
                elif c.lower() == 'iv' and not found_strike:
                    new_cols.append('C_IV')
                elif c.lower() == 'iv' and found_strike:
                    new_cols.append('IV')  # center IV
                elif not found_strike:
                    new_cols.append(f'C_{c}')
                else:
                    new_cols.append(f'P_{c}')
            headers = new_cols
            found_header = True
            continue

        # Skip section headers like 'April 28 10 DTE,...'
        if not found_header:
            continue

        # Skip expiry section label rows (has 'DTE' text)
        if 'DTE' in stripped and stripped.count(',') < 10:
            continue

        # Detect embedded stock price line (e.g., "TCS 2,581.50 INR +4.60 +0.18%,,,...")
        # These start with a stock ticker word + space + numbers
        first_cell = _parse_csv_row(stripped)[0].strip().strip('"')
        if re.match(r'^[A-Z]+\s+[\d,]+\.\d+\s+INR', first_cell):
            # Extract underlying price from this line
            m = re.search(r'([\d,]+\.\d+)', first_cell.split('INR')[0])
            if m:
                price_str = m.group(1).replace(',', '')
                try:
                    metadata['underlying_price'] = float(price_str)
                except ValueError:
                    pass
            continue

        # It's a data row
        if found_header and headers:
            cols = _parse_csv_row(stripped)
            # Pad or trim to match header count
            while len(cols) < len(headers):
                cols.append('')
            cols = cols[:len(headers)]
            data_rows.append(cols)

    if not headers or not data_rows:
        raise ValueError(
            f"CSV parse failed: headers={bool(headers)}, rows={len(data_rows)}. "
            f"Check file format — expects 'Rho,Vega,Gamma,...' header row."
        )

    df = pd.DataFrame(data_rows, columns=headers)

    # Convert ALL numeric columns
    for col in df.columns:
        df[col] = df[col].apply(_to_float)

    # Drop rows where Strike is NaN (blank trailing rows)
    df = df.dropna(subset=['Strike'])
    df = df.reset_index(drop=True)

    # ATM Strike identification
    if metadata['underlying_price'] > 0 and len(df) > 0:
        diffs = (df['Strike'] - metadata['underlying_price']).abs()
        atm_idx = diffs.idxmin()
        metadata['atm_strike'] = df.loc[atm_idx, 'Strike']
    elif len(df) > 0:
        metadata['atm_strike'] = df['Strike'].median()

    return df, metadata


def _parse_csv_row(line: str) -> list:
    """
    Parse one CSV row respecting quoted fields that may contain commas.
    e.g: 0.67,0.72,"2,589.40",—,— -> ['0.67', '0.72', '2,589.40', '—', '—']
    """
    import csv
    import io
    reader = csv.reader(io.StringIO(line))
    for row in reader:
        return row
    return []


def get_option_chain_summary(df: pd.DataFrame, metadata: dict) -> dict:
    """
    Computes summary statistics from the parsed option chain DataFrame.
    """
    summary = {
        'underlying_price': metadata.get('underlying_price', 0.0),
        'atm_strike': metadata.get('atm_strike', 0.0),
        'atm_iv': 0.0,
        'pcr_volume': 1.0,
        'pcr_oi': 1.0,
        'max_pain': 0.0,
        'highest_call_oi_strike': 0.0,
        'highest_call_oi': 0.0,
        'highest_put_oi_strike': 0.0,
        'highest_put_oi': 0.0,
        'net_delta': 0.0,
        'iv_skew': 0.0,
        'near_atm_call_volume': 0.0,
        'near_atm_put_volume': 0.0,
        'near_atm_pcr_volume': 1.0,
        'near_atm_delta_flow': 0.0,
        'near_atm_gamma_imbalance': 0.0,
        'support_strength': 0.0,
        'resistance_strength': 0.0,
        'put_wall_distance_pct': 0.0,
        'call_wall_distance_pct': 0.0,
        'time_value_skew': 0.0,
        'liquidity_score': 50.0,
        'downside_iv_premium': 0.0,
    }

    try:
        # Volume columns
        vol_c = 'C_Volume' if 'C_Volume' in df.columns else None
        vol_p = 'P_Volume' if 'P_Volume' in df.columns else None

        if vol_c and vol_p:
            tot_c = df[vol_c].fillna(0).sum()
            tot_p = df[vol_p].fillna(0).sum()
            summary['pcr_volume'] = round(tot_p / tot_c, 3) if tot_c > 0 else 1.0
            summary['pcr_oi'] = summary['pcr_volume']

            # Highest OI (using Volume as proxy since OI not in this CSV format)
            summary['highest_call_oi'] = df[vol_c].max()
            summary['highest_put_oi'] = df[vol_p].max()
            if df[vol_c].idxmax() is not None:
                summary['highest_call_oi_strike'] = df.loc[df[vol_c].idxmax(), 'Strike']
            if df[vol_p].idxmax() is not None:
                summary['highest_put_oi_strike'] = df.loc[df[vol_p].idxmax(), 'Strike']

            # Max Pain calculation
            strikes = df['Strike'].dropna().values
            pains = []
            for S in strikes:
                call_pain = df[df['Strike'] < S].apply(
                    lambda row: (S - row['Strike']) * (row[vol_c] if pd.notna(row[vol_c]) else 0), axis=1
                ).sum()
                put_pain = df[df['Strike'] > S].apply(
                    lambda row: (row['Strike'] - S) * (row[vol_p] if pd.notna(row[vol_p]) else 0), axis=1
                ).sum()
                pains.append(call_pain + put_pain)
            if pains:
                min_idx = np.argmin(pains)
                summary['max_pain'] = float(strikes[min_idx])

        # ATM IV (center column 'IV' if present, else C_Ask IV %)
        atm_row = df[df['Strike'] == summary['atm_strike']]
        atm_idx = None
        if not atm_row.empty:
            atm_idx = atm_row.index[0]
        if not atm_row.empty:
            if 'IV' in df.columns:
                iv_val = atm_row['IV'].values[0]
                summary['atm_iv'] = round(float(iv_val), 2) if pd.notna(iv_val) else 0.0
            elif 'C_Ask IV %' in df.columns:
                iv_val = atm_row['C_Ask IV %'].values[0]
                summary['atm_iv'] = round(float(iv_val), 2) if pd.notna(iv_val) else 0.0

        if atm_idx is None and len(df) > 0:
            atm_idx = int((df['Strike'] - summary['atm_strike']).abs().idxmin())

        if atm_idx is not None:
            window = df.iloc[max(0, atm_idx - 2):min(len(df), atm_idx + 3)].copy()

            if vol_c and vol_p:
                near_call = window[vol_c].fillna(0).sum()
                near_put = window[vol_p].fillna(0).sum()
                summary['near_atm_call_volume'] = float(near_call)
                summary['near_atm_put_volume'] = float(near_put)
                summary['near_atm_pcr_volume'] = round(near_put / near_call, 3) if near_call > 0 else 1.0

                put_median = window[vol_p].replace(0, np.nan).median()
                call_median = window[vol_c].replace(0, np.nan).median()
                summary['support_strength'] = round(summary['highest_put_oi'] / put_median, 3) if pd.notna(put_median) and put_median else 0.0
                summary['resistance_strength'] = round(summary['highest_call_oi'] / call_median, 3) if pd.notna(call_median) and call_median else 0.0

            if summary['underlying_price']:
                summary['put_wall_distance_pct'] = round(
                    ((summary['underlying_price'] - summary['highest_put_oi_strike']) / summary['underlying_price']) * 100,
                    3,
                ) if summary['highest_put_oi_strike'] else 0.0
                summary['call_wall_distance_pct'] = round(
                    ((summary['highest_call_oi_strike'] - summary['underlying_price']) / summary['underlying_price']) * 100,
                    3,
                ) if summary['highest_call_oi_strike'] else 0.0

            if 'C_Delta' in window.columns and 'P_Delta' in window.columns and vol_c and vol_p:
                total_near_volume = window[vol_c].fillna(0).sum() + window[vol_p].fillna(0).sum()
                if total_near_volume > 0:
                    delta_flow = (
                        (window['C_Delta'].fillna(0) * window[vol_c].fillna(0)).sum()
                        + (window['P_Delta'].fillna(0) * window[vol_p].fillna(0)).sum()
                    ) / total_near_volume
                    summary['near_atm_delta_flow'] = round(float(delta_flow), 5)

            if 'C_Gamma' in window.columns and 'P_Gamma' in window.columns and vol_c and vol_p:
                total_near_volume = window[vol_c].fillna(0).sum() + window[vol_p].fillna(0).sum()
                if total_near_volume > 0:
                    gamma_imbalance = (
                        (window['C_Gamma'].fillna(0) * window[vol_c].fillna(0)).sum()
                        - (window['P_Gamma'].fillna(0) * window[vol_p].fillna(0)).sum()
                    ) / total_near_volume
                    summary['near_atm_gamma_imbalance'] = round(float(gamma_imbalance * 1000), 5)

            if 'C_Time value' in window.columns and 'P_Time value' in window.columns:
                time_value_skew = _safe_mean(window['P_Time value']) - _safe_mean(window['C_Time value'])
                summary['time_value_skew'] = round(time_value_skew, 3)

            if 'P_Ask IV %' in window.columns and 'C_Ask IV %' in window.columns:
                iv_premium = _safe_mean(window['P_Ask IV %']) - _safe_mean(window['C_Ask IV %'])
                summary['downside_iv_premium'] = round(iv_premium, 3)

            if 'C_Spread' in window.columns and 'P_Spread' in window.columns:
                call_spread_pct = _safe_mean(window['C_Spread'] / window['Strike'].replace(0, np.nan))
                put_spread_pct = _safe_mean(window['P_Spread'] / window['Strike'].replace(0, np.nan))
                normalized_cost = max(0.0, (call_spread_pct + put_spread_pct) * 10000)
                summary['liquidity_score'] = round(max(0.0, min(100.0, 100.0 - normalized_cost)), 2)

        # Net Delta
        if 'C_Delta' in df.columns and 'P_Delta' in df.columns:
            c_delta_sum = df['C_Delta'].fillna(0).sum()
            p_delta_sum = df['P_Delta'].fillna(0).sum()
            summary['net_delta'] = round(c_delta_sum + p_delta_sum, 4)

        # IV Skew (OTM Put IV - OTM Call IV)
        if 'C_Ask IV %' in df.columns and 'P_Ask IV %' in df.columns:
            atm = summary['atm_strike']
            k_down = atm * 0.95
            k_up = atm * 1.05
            put_row = df.iloc[(df['Strike'] - k_down).abs().argsort()[:1]]
            call_row = df.iloc[(df['Strike'] - k_up).abs().argsort()[:1]]
            p_iv = put_row['P_Ask IV %'].values[0] if len(put_row) else 0
            c_iv = call_row['C_Ask IV %'].values[0] if len(call_row) else 0
            summary['iv_skew'] = round(float(p_iv if pd.notna(p_iv) else 0) - float(c_iv if pd.notna(c_iv) else 0), 3)

    except Exception as e:
        print(f"Warning: Summary computation partial failure — {e}")

    return summary
