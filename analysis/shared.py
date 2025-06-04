import json
import re
import requests


def analyze_function_with_llama(function_code, prompt=None):
    if prompt is None:
        prompt = f"Aşağıdaki Python fonksiyonunu açıkla:\n\n{function_code}"

    payload = {
        "model": "local-model",  # LM Studio sunucusu model ismine çok takılmaz
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.1,
    }

    try:
        response = requests.post(
            "http://localhost:1234/v1/chat/completions",  # LM Studio API
            headers={"Content-Type": "application/json"},
            json=payload,
        )
        return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return f"❌ LLM Hatası: {e}"


def optimize_function_with_llama(function_code):
    prompt = (
        f"Aşağıdaki Python fonksiyonunu daha verimli ve optimize bir şekilde yeniden yaz. "
        f"Eğer birden fazla alternatif varsa birkaç farklı çözüm öner:\n\n{function_code}"
    )
    return analyze_function_with_llama(function_code, prompt)


def check_errors_in_function(function_code):
    prompt = (
        f"Aşağıdaki Python fonksiyonunda herhangi bir hata, kötü uygulama veya potansiyel sorun var mı? "
        f"Syntax hatası, edge case eksikliği, kötü pratik gibi her türlü sorunu belirt:\n\n{function_code}"
    )
    return analyze_function_with_llama(function_code, prompt)


def summarize_full_file(code):
    prompt = (
        f"Aşağıdaki Python dosyasının genel yapısını açıkla. Dosyada hangi modüller var, hangi işlemleri yapıyor? "
        f"Önemli sınıflar, fonksiyonlar ve dosyanın amacı nedir? Güvenlik, verimlilik ya da okunabilirlik açısından genel bir değerlendirme yap:\n\n{code}"
    )
    return analyze_function_with_llama(code, prompt)


def score_project_with_llama(analysis_results):
    total_functions = sum(len(file.get("functions", [])) for file in analysis_results)
    total_files = len(analysis_results)

    project_summary = f"""
    Proje Özeti:
    - Toplam {total_files} Python dosyası
    - Toplam {total_functions} fonksiyon
    
    Dosya Özetleri:
    """

    for file in analysis_results[:5]:  # İlk 5 dosyayı özetle
        file_summary = file.get("file_summary", "Özet bulunamadı")
        # Ensure file_summary is a string and handle None case
        summary_text = (
            str(file_summary) if file_summary is not None else "Özet bulunamadı"
        )
        truncated_summary = (
            summary_text[:300] if len(summary_text) > 300 else summary_text
        )
        project_summary += (
            f"- {file.get('source_file', 'Bilinmeyen dosya')}: {truncated_summary}...\n"
        )
    # Geliştirilmiş prompt
    prompt = f"""Aşağıdaki Python kod projesini analiz et ve 0-100 arasında SADECE SAYISAL BİR PUAN ver.

    Değerlendirme Kriterleri:
    1. Kod Okunabilirliği (25%): Değişken isimleri, yorumlar, docstring kullanımı
    2. Yapılandırma ve Düzen (20%): Dosya organizasyonu, fonksiyon düzeni
    3. Fonksiyonel Doğruluk (25%): Kodun çalışabilirliği, mantıksal akış
    4. Hata Kontrolü ve Güvenlik (15%): Try-catch blokları, input validasyonu
    5. Modül Kullanımı ve Verimlilik (15%): Uygun kütüphane seçimi, algoritma verimliliği

    ÖNEMLI: Sadece 0-100 arasında bir sayı döndür. Açıklama yazma.
    
    Örnek çıktı: 73

    {project_summary}"""

    try:
        response = analyze_function_with_llama("", prompt)
        print(f"LLM Yanıtı: {response}")  # Debug için

        # Çoklu regex pattern ile sayı çıkarma
        patterns = [
            r"\b(\d{1,3})\b",  # Mevcut pattern
            r"(\d{1,3})/100",  # X/100 formatı
            r"Puan[:\s]*(\d{1,3})",  # "Puan: X" formatı
            r"Score[:\s]*(\d{1,3})",  # "Score: X" formatı
            r"(\d{1,3})(?:\s*puan|\s*point)",  # "X puan" formatı
        ]

        for pattern in patterns:
            score_match = re.search(pattern, response, re.IGNORECASE)
            if score_match:
                score = int(score_match.group(1))
                # Geçerli aralıkta olup olmadığını kontrol et
                if 0 <= score <= 100:
                    print(f"Bulunan puan: {score}")
                    return score

        # Eğer hiç sayı bulunamazsa, daha basit bir prompt dene
        simple_prompt = f"""Bu Python projesine 0-100 arasında puan ver. Sadece sayı yaz:
        
        Proje: {total_files} dosya, {total_functions} fonksiyon
        
        Puan:"""

        simple_response = analyze_function_with_llama("", simple_prompt)
        print(f"Basit prompt yanıtı: {simple_response}")

        # Basit yanıttan sayı çıkar
        numbers = re.findall(r"\b(\d{1,3})\b", simple_response)
        if numbers:
            score = int(numbers[0])
            if 0 <= score <= 100:
                return score

        print("Hiç geçerli puan bulunamadı, varsayılan döndürülüyor")
        return 65  # Varsayılan orta puan

    except Exception as e:
        print(f"Puanlama hatası: {e}")
        return 65
