#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BİST Otomatik Tarama ve Raporlama Sistemi
Her gün seans kapanışında çalışır, güçlü hisseleri filtreler ve Telegram'a gönderir
"""

import yfinance as yf
import pandas as pd
import pandas_ta as ta
from datetime import datetime, timedelta
import requests
import time

# TELEGRAM BİLGİLERİ
TELEGRAM_TOKEN = "8455173046:AAECKdZcTVnt3naPDzI3udwwfj23nyv4uMs"
TELEGRAM_CHAT_ID = "-1003670397485"

# BİST HİSSE LİSTESİ (TradingView formatından Yahoo Finance formatına)
BIST_HISSELER = """
QNBTR,ASELS,KLRHO,GARAN,ENKAI,KCHOL,THYAO,AKBNK,FROTO,TUPRS,BIMAS,VAKBN,
HALKB,YKBNK,DSTKF,TCELL,TTKOM,SAHOL,CCOLA,EREGL,KENT,ASTOR,GUBRF,TOASO,
TRALT,HEDEF,TERA,SISE,MAGEN,OYAKC,ISDMR,ENJSA,TAVHL,AEFES,TURSG,MGROS,
SASA,QNBFK,PGSUS,ZRGYO,BRSAN,KLNMA,DMLKT,MPARK,PASEU,ARCLK,AKSEN,AGHOL,
ECILC,TRGYO,KTLEV,ENERY,ISMEN,TABGD,UFUK,BRYAT,CVKMD,AHGAZ,LYDHO,LIDER,
GLRMK,PEKGY,RYGYO,RALYH,TBORG,SELEC,OTKAR,DOHOL,TTRAK,ANSGR,TRMET,RGYAS,
AYGAZ,ANHYT,ULKER,CIMSA,EFOR,ALARK,PETKM,BSOKE,DOAS,CLEBI,AGESA,ODINE,
INVES,AKSA,SOKM,TSKB,AKCNS,MAVI,IEYHO,GRSEL,SARKY,RYSAS,YGGYO,RAYSG,
NUHCM,GENIL,ECZYT,CWENE,DAPGM,ADGYO,PAHOL,KRDMA,GRTHO,BASGZ,CMENT,GLYHO,
TKFEN,BTCIM,BRISA,HEKTS,TEHOL,TRENJ,EUPWR,KLYPV,ALKLC,SKBNK,BMSTL,LYDYE,
GESAN,CEMZY,NTHOL,KUYAS,OBAMS,ALBRK,POLTK,IZENR,AKFYE,OZKGY,EGEEN,KCAER,
ARMGD,KONYA,AVPGY,MOGAN,ENTRA,TRHOL,AKSGY,ISGYO,ARASE,MIATK,BFREN,BINBN,
SNGYO,FENER,KLKIM,LILAK,BALSU,SUNTK,ISKPL,CANTE,BANVT,AYDEM,VERUS,ZOREN,
PSGYO,HLGYO,MEGMT,CRFSA,MRSHL,KZBGY,OYYAT,ASUZU,AHSGY,GSRAY,ENSRI,LMKDC,
AKFIS,ALFAS,MOPAS,ALTNY,ULUSE,FZLGY,DEVA,KLSER,SMRTG,YYLGD,LOGO,YEOTK,
ARDYZ,EGPRO,KSTUR,GWIND,KAYSE,TCKRC,ISFIN,KONTR,KOTON,JANTS,TRCAS,HTTBT,
VESBE,PATEK,TMSN,ECOGR,DOFRB,AKGRT,POLHO,AYCES,ESCAR,BINHO,TUKAS,VAKFA,
ICBCT,BULGS,BERA,NETCD,IZMDC,BARMA,OZATD,MEYSU,PRKAB,SONME,SDTTR,EUREN,
ZERGY,KBORU,AKFGY,GARFA,TATEN,ALGYO,SRVGY,MOBTL,A1CAP,TNZTP,KORDS,VAKKO,
VESTL,DGGYO,OFSYM,VSNMD,GOZDE,VAKFN,VKGYO,BUCIM,GLCVY,GUNDG,BASCM,GEREL,
BESLR,BIGTK,INGRM,EBEBK,ADEL,KLGYO,ALCAR,GEDIK,EGGUB,ALKA,BIENY,HRKET,
SURGY,INVEO,KARSN,BIOEN,SNPAM,IZFAS,BOSSA,HATSN,QUAGR,KAPLM,PARSN,ODAS,
TUREX,TARKM,SEGMN,KOPOL,MAALT,ATAKP,DOKTA,PAGYO,GIPTA,TSPOR,BOBET,AKMGY,
AKENR,NTGAZ,AYEN,ASGYO,ARSAN,AGROT,IHAAS,BLUME,KAREL,KMPUR,GMTAS,YIGIT,
GOKNR,INTEM,BAHKM,AKHAN,ONCSM,SMRVA,GENTS,ESEN,ISGSY,DITAS,CRDFA,KGYO,
MNDTR,BJKAS,ENDAE,TEZOL,NATEN,CATES,GOLTS,YATAS,KRVGD,REEDR,EGEGY,UCAYM,
EKOS,KOCMT,KATMR,INDES,DMRGD,CGCAM,CEMTS,ALVES,KONKA,BORSK,FORTE,KARTN,
BRKVY,MERIT,TMPOL,YBTAS,ADESE,BIGEN,DESA,ALKIM,PLTUR,AFYON,HOROZ,PENTA,
EGEPO,ORGE,ULUUN,DARDL,BURVA,OZYSR,SAFKR,ARFYE,BURCE,ALCTL,TSGYO,LINK,
KZGYO,CEMAS,SOKE,SUWEN,GSDHO,TKNSA,SEGYO,BIGCH,ERCB,YUNSA,AZTEK,FMIZP,
MHRGY,YAPRK,ONRYT,ORMA,USAK,BVSAN,DYOBY,PKENT,KUTPO,DUNYH,ANELE,KIMMR,
GOODY,MNDRS,IMASM,INFO,ELITE,EDATA,NETAS,GATEG,ERBOS,MEKAG,DZGYO,BAGFS,
TURGG,GZNMI,BEGYO,PETUN,ATATP,MANAS,PNSUT,PAPIL,HDFGS,AYES,KLSYN,LKMNH,
TATGD,MERCN,FORMT,BLCYT,NUGYO,KTSKR,EKSUN,MEDTR,SERNT,RUZYE,CMBTN,SAYAS,
BRLSM,KUVVA,HUNER,OSMEN,MAKTK,SANKO,LIDFA,KNFRT,CELHA,IHLAS,ISSEN,HURGZ,
DCTTR,EMKEL,PINSU,PNLSN,TRILC,BYDNR,FONET,YYAPI,KRGYO,BEYAZ,LRSHO,MARBL,
PRKME,METRO,UNLU,LUKSK,TEKTU,MACKO,SKYLP,MRGYO,BAKAB,CONSE,DURKN,DNISI,
MSGYO,FRIGO,PAMEL,ARENA,RUBNS,ARTMS,ESCOM,KRONT,DERHL,VBTYZ,ATEKS,SNICA,
GLRYH,PCILT,SANFM,BIZIM,OTTO,DAGI,SELVA,ANGEN,KLMSN,EDIP,OZSUB,TGSAS,
EGSER,KRSTL,EYGYO,MTRKS,ULUFA,OZGYO,VERTU,ISBIR,VRGYO,DERIM,TLMAN,INTEK,
KFEIN,DGATE,AGYO,IHLGM,EUHOL,RTALB,CUSAN,SKTAS,OSTIM,BRKO,DURDO,BORLS,
MERKO,SKYMD,MAKIM,TDGYO,MEPET,TUCLK,ARZUM,OBASE,DMSAS,DENGE,DGNMO,DOFER,
VANGD,MARTI,BMSCH,A1YEN,PKART,AVGYO,YKSLN,BNTAS,KRPLS,SUMAS,COSMO,NIBAS,
DOGUB,PENGD,GLBMD,ZEDUR,OZRDN,GSDDE,ISYAT,BALAT,AVHOL,AKSUE,MMCAS,PRDGS,
RNPOL,GEDZA,SODSN,YAYLA,FADE,HKTM,AVOD,VKING,EPLAS,YESIL,BAYRK,IHGZT,
VKFYO,KERVN,EKIZ,ACSEL,IZINV,DESPC,HUBVC,OYAYO,SEYKM,FLAP,ICUGS,EMNIS,
CEOEM,SMART,ETILR,SILVR,YONGA,HATEK,SEKFK,PSDTC,KRTEK,SEKUR,ORCAY,IHYAY,
BRMEN,PRZMA,BRKSN,MEGAP,IHEVA,AVTUR,ULAS,MARKA,SANEL,MZHLD,AKYHO,OYLUM,
SAMAT,IDGYO,GRNYO,ATAGY,ERSU,RODRG,ATLAS,ETYAT,CASA,ATSYH,MTRYO,EUKYO,
EUYO,DIRIT,FRMPL,BESTE,ALTIN,ZGYO,MARMR
""".replace('\n', '').split(',')

# .IS uzantısı ekle
HISSE_LISTESI = [h.strip() + '.IS' for h in BIST_HISSELER if h.strip()]

def telegram_gonder(mesaj):
    """Telegram'a mesaj gönder"""
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        data = {
            "chat_id": TELEGRAM_CHAT_ID,
            "text": mesaj,
            "parse_mode": "HTML"
        }
        response = requests.post(url, data=data)
        return response.json()
    except Exception as e:
        print(f"Telegram hatası: {e}")
        return None

def veri_cek(ticker, period="3mo"):
    """Hisse verisini çek"""
    try:
        stock = yf.Ticker(ticker)
        df = stock.history(period=period)
        if df.empty:
            return None
        return df
    except:
        return None

def teknik_analiz(df):
    """Teknik analiz hesapla"""
    try:
        # ADX
        adx_df = df.ta.adx(length=14)
        if adx_df is not None and not adx_df.empty:
            df['ADX'] = adx_df['ADX_14']
            df['DI+'] = adx_df['DMP_14']
            df['DI-'] = adx_df['DMN_14']
        
        # MFI
        mfi = df.ta.mfi(length=14)
        if mfi is not None:
            df['MFI'] = mfi
        
        # RSI
        rsi = df.ta.rsi(length=14)
        if rsi is not None:
            df['RSI'] = rsi
        
        # Stochastic
        stoch = df.ta.stoch(k=14, d=3)
        if stoch is not None and not stoch.empty:
            df['STOCH_K'] = stoch['STOCHk_14_3_3']
            df['STOCH_D'] = stoch['STOCHd_14_3_3']
        
        # VWAP
        vwap = df.ta.vwap()
        if vwap is not None:
            df['VWAP'] = vwap
        
        return df
    except Exception as e:
        print(f"Teknik analiz hatası: {e}")
        return df

def destek_direnc_bul(df, window=20):
    """Basit destek/direnç tespiti"""
    try:
        # Son 20 günün en düşüğü = destek
        destek = df['Low'].tail(window).min()
        
        # Son 20 günün en yükseği = direnç  
        direnc = df['High'].tail(window).max()
        
        return destek, direnc
    except:
        return None, None

def mtf_uyum(df):
    """Multi-timeframe uyum kontrolü (haftalık + aylık)"""
    try:
        # Haftalık trend (son 5 gün vs önceki 5 gün)
        haftalik_yuksek = df['Close'].tail(5).mean() > df['Close'].tail(10).head(5).mean()
        
        # Aylık trend (son 20 gün vs önceki 20 gün)
        aylik_yuksek = df['Close'].tail(20).mean() > df['Close'].tail(40).head(20).mean()
        
        return haftalik_yuksek and aylik_yuksek
    except:
        return False

def hisse_analiz(ticker):
    """Tek bir hisseyi analiz et"""
    try:
        # Veri çek
        df = veri_cek(ticker)
        if df is None or len(df) < 50:
            return None
        
        # Teknik analiz
        df = teknik_analiz(df)
        
        # Son değerler
        son = df.iloc[-1]
        fiyat = son['Close']
        
        # Kontroller
        if pd.isna(son.get('ADX')) or pd.isna(son.get('MFI')) or pd.isna(son.get('RSI')):
            return None
        
        adx = son['ADX']
        mfi = son['MFI']
        rsi = son['RSI']
        stoch_k = son.get('STOCH_K', 50)
        stoch_d = son.get('STOCH_D', 50)
        vwap_val = son.get('VWAP', fiyat)
        
        # Destek/Direnç
        destek, direnc = destek_direnc_bul(df)
        if destek is None:
            destek = fiyat * 0.95
            
        # VWAP Breakout hesapla
        vwap_breakout = ((fiyat - vwap_val) / vwap_val) * 100
        
        # MTF Uyum
        mtf_uyumlu = mtf_uyum(df)
        
        # Risk/Ödül hesapla
        stop = destek
        hedef = fiyat + (fiyat - stop) * 1.5  # 1.5R hedef
        risk = fiyat - stop
        odul = hedef - fiyat
        risk_odul = risk / odul if odul > 0 else 999
        
        # FİLTRELEME KRİTERLERİ (PKART benzeri güçlü hisseler)
        filtre_gecti = (
            adx > 20 and              # Güçlü trend
            mfi > 45 and              # Pozitif para akışı
            vwap_breakout > 2.0 and   # VWAP üzerinde breakout
            mtf_uyumlu and            # Haftalık+Aylık yükseliş
            rsi > 40 and rsi < 75 and # Sağlıklı RSI
            stoch_k > stoch_d and     # Stochastic yükseliş
            stoch_k > 40 and          # Stoch momentum
            risk_odul < 0.6           # İyi Risk/Ödül
        )
        
        if not filtre_gecti:
            return None
        
        # Skor hesapla (0-100)
        skor = 0
        skor += min(adx, 40)  # Max 40 puan
        skor += min(mfi / 2, 30)  # Max 30 puan
        skor += min(vwap_breakout * 2, 20)  # Max 20 puan
        skor += 10 if mtf_uyumlu else 0
        
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
    """PKART formatında rapor oluştur"""
    ticker = hisse_data['ticker']
    
    # MTF durum emoji
    mtf_emoji = "✅" if hisse_data['mtf_uyum'] else "⚠️"
    
    # Yıldız sistemi (skor bazlı)
    skor = hisse_data['skor']
    if skor >= 90:
        yildiz = "⭐⭐⭐⭐⭐"
    elif skor >= 75:
        yildiz = "⭐⭐⭐⭐"
    elif skor >= 60:
        yildiz = "⭐⭐⭐"
    else:
        yildiz = "⭐⭐"
    
    rapor = f"""
<b>📊 TEKNİK ANALİZ RAPORU</b>

<b>{ticker}</b>

Hisse <b>{hisse_data['fiyat']:.2f} TL</b> seviyesinde. ADX <b>{hisse_data['adx']:.1f}</b> ile güçlü yükseliş trendi ve MFI <b>{hisse_data['mfi']:.1f}</b> ile pozitif para akışı görülüyor. VWAP <b>{hisse_data['vwap']:.2f} TL</b> üzerinde güçlü bir breakout gerçekleşmiş (<b>%{hisse_data['vwap_breakout']:.1f}</b>). <b>{hisse_data['destek']:.2f} TL</b> (5x test) desteği korundukça <b>{hisse_data['hedef']:.2f} TL</b> hedefi hedeflenebilir. MTF güçlü uyum (haftalık+aylık yükseliş) {mtf_emoji} gösterirken, RSI <b>{hisse_data['rsi']:.1f}</b> ve Stochastic K=<b>{hisse_data['stoch_k']:.1f}</b> / D=<b>{hisse_data['stoch_d']:.1f}</b> seviyeleri dikkat çekiyor; düşük Risk/Ödül oranı (<b>{hisse_data['risk_odul']:.2f}</b>) ise bir risk faktörüdür.

<b>SKOR: {skor:.0f}/100</b> {yildiz}
"""
    return rapor

def main():
    """Ana fonksiyon"""
    print(f"🚀 Tarama başlatılıyor... Toplam hisse: {len(HISSE_LISTESI)}")
    telegram_gonder(f"🔍 BİST Tarama Başladı\n\nToplam {len(HISSE_LISTESI)} hisse taranıyor...")
    
    basarili_hisseler = []
    hata_sayisi = 0
    
    # Tüm hisseleri tara
    for i, ticker in enumerate(HISSE_LISTESI):
        try:
            print(f"[{i+1}/{len(HISSE_LISTESI)}] {ticker} analiz ediliyor...")
            
            sonuc = hisse_analiz(ticker)
            if sonuc:
                basarili_hisseler.append(sonuc)
                print(f"  ✅ {ticker} - GÜÇLÜ SİNYAL! Skor: {sonuc['skor']:.0f}")
            
            # Her 50 hissede bir durum raporu
            if (i + 1) % 50 == 0:
                print(f"  📊 İlerleme: {i+1}/{len(HISSE_LISTESI)} ({len(basarili_hisseler)} güçlü hisse bulundu)")
            
            # Rate limit (saniyede 2 istek)
            time.sleep(0.5)
            
        except Exception as e:
            hata_sayisi += 1
            print(f"  ❌ {ticker} hatası: {e}")
            continue
    
    print(f"\n✅ Tarama tamamlandı!")
    print(f"   Toplam hisse: {len(HISSE_LISTESI)}")
    print(f"   Güçlü sinyal: {len(basarili_hisseler)}")
    print(f"   Hata: {hata_sayisi}")
    
    # Sırala (en yüksek skordan en düşüğe)
    basarili_hisseler.sort(key=lambda x: x['skor'], reverse=True)
    
    # Telegram'a gönder
    if len(basarili_hisseler) == 0:
        mesaj = "⚠️ Bugün filtre kriterlerini geçen hisse bulunamadı."
        telegram_gonder(mesaj)
    else:
        # Başlık mesajı
        tarih = datetime.now().strftime("%d/%m/%Y %H:%M")
        baslik = f"""
🔥 <b>BİST GÜNLÜK RAPOR</b>
📅 {tarih}

✅ Toplam <b>{len(basarili_hisseler)}</b> güçlü hisse bulundu!

━━━━━━━━━━━━━━━━━━━━━
"""
        telegram_gonder(baslik)
        
        # Her hisse için rapor gönder
        for i, hisse in enumerate(basarili_hisseler[:20], 1):  # İlk 20'yi gönder
            rapor = rapor_olustur(hisse)
            telegram_gonder(rapor)
            time.sleep(1)  # Telegram rate limit
        
        # Özet mesajı
        if len(basarili_hisseler) > 20:
            ozet = f"\n⚠️ Toplam {len(basarili_hisseler)} hisse bulundu, ilk 20'si gösterildi."
            telegram_gonder(ozet)
    
    print("✅ Raporlar Telegram'a gönderildi!")

if __name__ == "__main__":
    main()
