#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BİST Otomatik Tarama - Manuel Teknik Analiz (pandas-ta YOK!)
Her gün seans kapanışında çalışır, güçlü hisseleri filtreler ve Telegram'a gönderir
"""

import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime
import requests
import time

# TELEGRAM BİLGİLERİ
TELEGRAM_TOKEN = "8455173046:AAECKdZcTVnt3naPDzI3udwwfj23nyv4uMs"
TELEGRAM_CHAT_ID = "-1003670397485"

# BİST GÜNCEL HİSSE LİSTESİ (BİST TÜM - 541 HİSSE)
BIST_HISSELER = """
QNBTR,ASELS,KLRHO,GARAN,ENKAI,KCHOL,THYAO,AKBNK,FROTO,TUPRS,BIMAS,VAKBN,HALKB,YKBNK,DSTKF,TCELL,TTKOM,SAHOL,CCOLA,EREGL,KENT,ASTOR,GUBRF,TOASO,TRALT,HEDEF,TERA,SISE,MAGEN,OYAKC,ISDMR,ENJSA,TAVHL,AEFES,TURSG,MGROS,SASA,QNBFK,PGSUS,ZRGYO,BRSAN,KLNMA,DMLKT,MPARK,PASEU,ARCLK,AKSEN,AGHOL,ECILC,TRGYO,KTLEV,ENERY,ISMEN,TABGD,UFUK,BRYAT,CVKMD,AHGAZ,LYDHO,LIDER,GLRMK,PEKGY,RYGYO,RALYH,TBORG,SELEC,OTKAR,DOHOL,TTRAK,ANSGR,TRMET,RGYAS,AYGAZ,ANHYT,ULKER,CIMSA,EFOR,ALARK,PETKM,BSOKE,DOAS,CLEBI,AGESA,ODINE,INVES,AKSA,SOKM,TSKB,AKCNS,MAVI,IEYHO,GRSEL,SARKY,RYSAS,YGGYO,RAYSG,NUHCM,GENIL,ECZYT,CWENE,DAPGM,ADGYO,PAHOL,KRDMA,GRTHO,BASGZ,CMENT,GLYHO,TKFEN,BTCIM,BRISA,HEKTS,TEHOL,TRENJ,EUPWR,KLYPV,ALKLC,SKBNK,BMSTL,LYDYE,GESAN,CEMZY,NTHOL,KUYAS,OBAMS,ALBRK,POLTK,IZENR,AKFYE,OZKGY,EGEEN,KCAER,ARMGD,KONYA,AVPGY,MOGAN,ENTRA,TRHOL,AKSGY,ISGYO,ARASE,MIATK,BFREN,BINBN,SNGYO,FENER,KLKIM,LILAK,BALSU,SUNTK,ISKPL,CANTE,BANVT,AYDEM,VERUS,ZOREN,PSGYO,HLGYO,MEGMT,CRFSA,MRSHL,KZBGY,OYYAT,ASUZU,AHSGY,GSRAY,ENSRI,LMKDC,AKFIS,ALFAS,MOPAS,ALTNY,ULUSE,FZLGY,DEVA,KLSER,SMRTG,YYLGD,LOGO,YEOTK,ARDYZ,EGPRO,KSTUR,GWIND,KAYSE,TCKRC,ISFIN,KONTR,KOTON,JANTS,TRCAS,HTTBT,VESBE,PATEK,TMSN,ECOGR,DOFRB,AKGRT,POLHO,AYCES,ESCAR,BINHO,TUKAS,VAKFA,ICBCT,BULGS,BERA,NETCD,IZMDC,BARMA,OZATD,MEYSU,PRKAB,SONME,SDTTR,EUREN,ZERGY,KBORU,AKFGY,GARFA,TATEN,ALGYO,SRVGY,MOBTL,A1CAP,TNZTP,KORDS,VAKKO,VESTL,DGGYO,OFSYM,VSNMD,GOZDE,VAKFN,VKGYO,BUCIM,GLCVY,GUNDG,BASCM,GEREL,BESLR,BIGTK,INGRM,EBEBK,ADEL,KLGYO,ALCAR,GEDIK,EGGUB,ALKA,BIENY,HRKET,SURGY,INVEO,KARSN,BIOEN,SNPAM,IZFAS,BOSSA,HATSN,QUAGR,KAPLM,PARSN,ODAS,TUREX,TARKM,SEGMN,KOPOL,MAALT,ATAKP,DOKTA,PAGYO,GIPTA,TSPOR,BOBET,AKMGY,AKENR,NTGAZ,AYEN,ASGYO,ARSAN,AGROT,IHAAS,BLUME,KAREL,KMPUR,GMTAS,YIGIT,GOKNR,INTEM,BAHKM,AKHAN,ONCSM,SMRVA,GENTS,ESEN,ISGSY,DITAS,CRDFA,KGYO,MNDTR,BJKAS,ENDAE,TEZOL,NATEN,CATES,GOLTS,YATAS,KRVGD,REEDR,EGEGY,UCAYM,EKOS,KOCMT,KATMR,INDES,DMRGD,CGCAM,CEMTS,ALVES,KONKA,BORSK,FORTE,KARTN,BRKVY,MERIT,TMPOL,YBTAS,ADESE,BIGEN,DESA,ALKIM,PLTUR,AFYON,HOROZ,PENTA,EGEPO,ORGE,ULUUN,DARDL,BURVA,OZYSR,SAFKR,ARFYE,BURCE,ALCTL,TSGYO,LINK,KZGYO,CEMAS,SOKE,SUWEN,GSDHO,TKNSA,SEGYO,BIGCH,ERCB,YUNSA,AZTEK,FMIZP,MHRGY,YAPRK,ONRYT,ORMA,USAK,BVSAN,DYOBY,PKENT,KUTPO,DUNYH,ANELE,KIMMR,GOODY,MNDRS,IMASM,INFO,ELITE,EDATA,NETAS,GATEG,ERBOS,MEKAG,DZGYO,BAGFS,TURGG,GZNMI,BEGYO,PETUN,ATATP,MANAS,PNSUT,PAPIL,HDFGS,AYES,KLSYN,LKMNH,TATGD,MERCN,FORMT,BLCYT,NUGYO,KTSKR,EKSUN,MEDTR,SERNT,RUZYE,CMBTN,SAYAS,BRLSM,KUVVA,HUNER,OSMEN,MAKTK,SANKO,LIDFA,KNFRT,CELHA,IHLAS,ISSEN,HURGZ,DCTTR,EMKEL,PINSU,PNLSN,TRILC,BYDNR,FONET,YYAPI,KRGYO,BEYAZ,LRSHO,MARBL,PRKME,METRO,UNLU,LUKSK,TEKTU,MACKO,SKYLP,MRGYO,BAKAB,CONSE,DURKN,DNISI,MSGYO,FRIGO,PAMEL,ARENA,RUBNS,ARTMS,ESCOM,KRONT,DERHL,VBTYZ,ATEKS,SNICA,GLRYH,PCILT,SANFM,BIZIM,OTTO,DAGI,SELVA,ANGEN,KLMSN,EDIP,OZSUB,TGSAS,EGSER,KRSTL,EYGYO,MTRKS,ULUFA,OZGYO,VERTU,ISBIR,VRGYO,DERIM,TLMAN,INTEK,KFEIN,DGATE,AGYO,IHLGM,EUHOL,RTALB,CUSAN,SKTAS,OSTIM,BRKO,DURDO,BORLS,MERKO,SKYMD,MAKIM,TDGYO,MEPET,TUCLK,ARZUM,OBASE,DMSAS,DENGE,DGNMO,DOFER,VANGD,MARTI,BMSCH,A1YEN,PKART,AVGYO,YKSLN,BNTAS,KRPLS,SUMAS,COSMO,NIBAS,DOGUB,PENGD,GLBMD,ZEDUR,OZRDN,GSDDE,ISYAT,BALAT,AVHOL,AKSUE,MMCAS,PRDGS,RNPOL,GEDZA,SODSN,YAYLA,FADE,HKTM,AVOD,VKING,EPLAS,YESIL,BAYRK,IHGZT,VKFYO,KERVN,EKIZ,ACSEL,IZINV,DESPC,HUBVC,OYAYO,SEYKM,FLAP,ICUGS,EMNIS,CEOEM,SMART,ETILR,SILVR,YONGA,HATEK,SEKFK,PSDTC,KRTEK,SEKUR,ORCAY,IHYAY,BRMEN,PRZMA,BRKSN,MEGAP,IHEVA,AVTUR,ULAS,MARKA,SANEL,MZHLD,AKYHO,OYLUM,SAMAT,IDGYO,GRNYO,ATAGY,ERSU,RODRG,ATLAS,ETYAT,CASA,ATSYH,MTRYO,EUKYO,EUYO,DIRIT,FRMPL,BESTE,ALTIN,ZGYO,MARMR
""".replace('\n', '').strip()

# Listeyi .IS uzantılı hale getir
HISSE_LISTESI = [h.strip() + '.IS' for h in BIST_HISSELER.split(',') if h.strip()]

def telegram_gonder(mesaj):
    """Telegram'a mesaj gönder"""
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        data = {"chat_id": TELEGRAM_CHAT_ID, "text": mesaj, "parse_mode": "HTML"}
        response = requests.post(url, data=data, timeout=10)
        return response.json()
    except Exception as e:
        print(f"Telegram hatası: {e}")
        return None

def veri_cek(ticker, period="3mo"):
    """Hisse verisini çek"""
    try:
        stock = yf.Ticker(ticker)
        df = stock.history(period=period)
        if df.empty or len(df) < 50:
            return None
        return df
    except:
        return None

# MANUEL TEKNİK ANALİZ FONKSİYONLARI

def calculate_rsi(prices, period=14):
    """RSI hesapla"""
    delta = prices.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

def calculate_adx(df, period=14):
    """ADX hesapla"""
    high = df['High']
    low = df['Low']
    close = df['Close']
    
    plus_dm = high.diff()
    minus_dm = low.diff()
    plus_dm[plus_dm < 0] = 0
    minus_dm[minus_dm > 0] = 0
    
    tr1 = high - low
    tr2 = abs(high - close.shift())
    tr3 = abs(low - close.shift())
    tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
    
    atr = tr.rolling(window=period).mean()
    plus_di = 100 * (plus_dm.rolling(window=period).mean() / atr)
    minus_di = 100 * (abs(minus_dm).rolling(window=period).mean() / atr)
    
    dx = 100 * abs(plus_di - minus_di) / (plus_di + minus_di)
    adx = dx.rolling(window=period).mean()
    
    return adx

def calculate_mfi(df, period=14):
    """MFI hesapla"""
    typical_price = (df['High'] + df['Low'] + df['Close']) / 3
    money_flow = typical_price * df['Volume']
    
    positive_flow = money_flow.where(typical_price > typical_price.shift(1), 0)
    negative_flow = money_flow.where(typical_price < typical_price.shift(1), 0)
    
    positive_mf = positive_flow.rolling(window=period).sum()
    negative_mf = negative_flow.rolling(window=period).sum()
    
    mfi = 100 - (100 / (1 + positive_mf / negative_mf))
    return mfi

def calculate_stochastic(df, k_period=14, d_period=3):
    """Stochastic hesapla"""
    low_min = df['Low'].rolling(window=k_period).min()
    high_max = df['High'].rolling(window=k_period).max()
    
    k = 100 * (df['Close'] - low_min) / (high_max - low_min)
    d = k.rolling(window=d_period).mean()
    
    return k, d

def calculate_vwap(df):
    """VWAP hesapla"""
    typical_price = (df['High'] + df['Low'] + df['Close']) / 3
    return (typical_price * df['Volume']).cumsum() / df['Volume'].cumsum()

def hisse_analiz(ticker):
    """Tek bir hisseyi analiz et"""
    try:
        df = veri_cek(ticker)
        if df is None or len(df) < 50:
            return None
        
        # Teknik analiz hesapla
        df['RSI'] = calculate_rsi(df['Close'], 14)
        df['ADX'] = calculate_adx(df, 14)
        df['MFI'] = calculate_mfi(df, 14)
        df['STOCH_K'], df['STOCH_D'] = calculate_stochastic(df, 14, 3)
        df['VWAP'] = calculate_vwap(df)
        
        # Son değerler
        son = df.iloc[-1]
        fiyat = son['Close']
        
        # Kontroller
        if pd.isna(son['ADX']) or pd.isna(son['MFI']) or pd.isna(son['RSI']):
            return None
        
        adx = son['ADX']
        mfi = son['MFI']
        rsi = son['RSI']
        stoch_k = son['STOCH_K']
        stoch_d = son['STOCH_D']
        vwap_val = son['VWAP']
        
        # Destek/Direnç
        destek = df['Low'].tail(20).min()
        direnc = df['High'].tail(20).max()
        
        # VWAP Breakout
        vwap_breakout = ((fiyat - vwap_val) / vwap_val) * 100
        
        # MTF Uyum (basit)
        haftalik = df['Close'].tail(5).mean() > df['Close'].tail(10).head(5).mean()
        aylik = df['Close'].tail(20).mean() > df['Close'].tail(40).head(20).mean()
        mtf_uyumlu = haftalik and aylik
        
        # Risk/Ödül (Sadece raporda göstermek için hesaplıyoruz, filtrede eleme yapmayacak)
        stop = destek
        hedef = fiyat + (fiyat - stop) * 1.5
        risk = fiyat - stop
        odul = hedef - fiyat
        risk_odul = risk / odul if odul > 0 else 999
        
        # FİLTRE (DENGELİ - Hem trendi yakalar hem çok sıkmaz)
        filtre_gecti = (
            adx > 20 and                  # Trend oluşumu başlasın yeter
            mfi > 35 and                  # Para girişi var
            vwap_breakout > 0.5 and       # VWAP'ın üstünde
            vwap_breakout < 12.0 and      # Ama %12'den fazla kopmamış
            mtf_uyumlu and                # Çoklu zaman dilimi onayı
            rsi > 40 and rsi < 80 and     # RSI makul aralıkta
            stoch_k > stoch_d and         # Stoch AL konumunda
            stoch_k < 90                  # Stoch tavana (100) vurmamış
        )
        
        if not filtre_gecti:
            return None
        
        # Skor
        skor = min(adx, 40) + min(mfi / 2, 30) + min(vwap_breakout * 2, 20) + (10 if mtf_uyumlu else 0)
        
        return {
            'ticker': ticker.replace('.IS', ''),
            'fiyat': fiyat,
            'adx': adx,
            'mfi': mfi,
            'rsi': rsi,
            'stoch_k': stoch_k,
            'stoch_d': stoch_d,
            'vwap': vwap_val,
            'vwap_breakout': vwap_breakout,
            'destek': destek,
            'hedef': hedef,
            'risk_odul': risk_odul,
            'mtf_uyum': mtf_uyumlu,
            'skor': skor
        }
        
    except Exception as e:
        print(f"{ticker} analiz hatası: {e}")
        return None

def rapor_olustur(hisse_data):
    """Pavyon formatında neon rapor :)"""
    ticker = hisse_data['ticker']
    skor = hisse_data['skor']
    
    yildiz = "🌟🌟🌟🌟🌟" if skor >= 90 else "⭐⭐⭐⭐" if skor >= 75 else "⭐⭐⭐"
    mtf_emoji = "✅ ONAYLI" if hisse_data['mtf_uyum'] else "⚠️ DİKKAT"
    
    rapor = f"""
🔥 <b>[ {ticker} ] - VIP SİNYAL DETAYI</b> 🔥
━━━━━━━━━━━━━━━━━━━━━
💰 <b>Anlık Fiyat:</b> {hisse_data['fiyat']:.2f} TL
🎯 <b>Potansiyel Hedef:</b> {hisse_data['hedef']:.2f} TL
🛡️ <b>Ana Destek (Stop):</b> {hisse_data['destek']:.2f} TL
━━━━━━━━━━━━━━━━━━━━━
<b>--- ⚙️ TEKNİK GÖSTERGELER ---</b>
📈 <b>Trend (ADX):</b> {hisse_data['adx']:.1f} <i>(Güçlü Kalkış!)</i>
💵 <b>Para Girişi (MFI):</b> {hisse_data['mfi']:.1f} <i>(Hacim Destekli)</i>
🚀 <b>VWAP Kopuşu:</b> %{hisse_data['vwap_breakout']:.1f}
⏳ <b>Zaman Uyum (MTF):</b> {mtf_emoji}

<b>--- 📊 OSİLATÖR DURUMU ---</b>
⚡ <b>RSI:</b> {hisse_data['rsi']:.1f} <i>(Şişme Yok)</i>
🎯 <b>Stoch K/D:</b> {hisse_data['stoch_k']:.1f} / {hisse_data['stoch_d']:.1f} <i>(AL Konumunda)</i>
⚖️ <b>Risk/Ödül Oranı:</b> {hisse_data['risk_odul']:.2f}
━━━━━━━━━━━━━━━━━━━━━
🏆 <b>SİSTEM SKORU: {skor:.0f}/100</b> {yildiz}
"""
    return rapor

def main():
    """Ana fonksiyon"""
    print(f"🚀 Tarama başlatılıyor... Toplam hisse: {len(HISSE_LISTESI)}")
    telegram_gonder(f"🔍 BİST Tarama Başladı\n\nToplam {len(HISSE_LISTESI)} hisse taranıyor...")
    
    basarili_hisseler = []
    hata_sayisi = 0
    
    for i, ticker in enumerate(HISSE_LISTESI):
        try:
            print(f"[{i+1}/{len(HISSE_LISTESI)}] {ticker} analiz ediliyor...")
            
            sonuc = hisse_analiz(ticker)
            if sonuc:
                basarili_hisseler.append(sonuc)
                print(f"  ✅ {ticker} - GÜÇLÜ! Skor: {sonuc['skor']:.0f}")
            
            if (i + 1) % 50 == 0:
                print(f"  📊 İlerleme: {i+1}/{len(HISSE_LISTESI)} ({len(basarili_hisseler)} güçlü)")
            
            time.sleep(0.3)
            
        except Exception as e:
            hata_sayisi += 1
            print(f"  ❌ {ticker} hatası: {e}")
            continue
    
    print(f"\n✅ Tarama tamamlandı!")
    print(f"   Toplam: {len(HISSE_LISTESI)}")
    print(f"   Güçlü: {len(basarili_hisseler)}")
    print(f"   Hata: {hata_sayisi}")
    
    basarili_hisseler.sort(key=lambda x: x['skor'], reverse=True)
    
    if len(basarili_hisseler) == 0:
        telegram_gonder("⚠️ Bugün filtre kriterlerini geçen hisse bulunamadı.")
    else:
        tarih = datetime.now().strftime("%d/%m/%Y %H:%M")
        baslik = f"""
🔥 <b>BİST GÜNLÜK RAPOR</b>
📅 {tarih}

✅ Toplam <b>{len(basarili_hisseler)}</b> güçlü hisse bulundu!

━━━━━━━━━━━━━━━━━━━━━
"""
        telegram_gonder(baslik)
        
        for i, hisse in enumerate(basarili_hisseler[:15], 1):
            rapor = rapor_olustur(hisse)
            telegram_gonder(rapor)
            time.sleep(2)
        
        if len(basarili_hisseler) > 15:
            telegram_gonder(f"\n⚠️ Toplam {len(basarili_hisseler)} hisse bulundu, en yüksek skorlu ilk 15'i gösterildi.")
    
    print("✅ Raporlar Telegram'a gönderildi!")

if __name__ == "__main__":
    main()
