import requests
from analysis.function_analysis import extract_functions_code
from analysis.shared import (
    analyze_function_with_llama,
    check_errors_in_function,
    optimize_function_with_llama,
    summarize_full_file,
)
import streamlit as st


def analyze_github_repository(
    username, repo_name, do_optimize=False, do_check_errors=False
):
    """Fixed version with better error handling"""
    api_url = f"https://api.github.com/repos/{username}/{repo_name}/contents"
    raw_base = f"https://raw.githubusercontent.com/{username}/{repo_name}/master/"
    headers = {"Accept": "application/vnd.github.v3+json"}

    py_files = get_all_py_files(api_url, raw_base, headers)

    if not py_files:
        st.error("Bu repository'de Python dosyası bulunamadı!")
        return []

    analysis_results = []

    for raw_url in py_files:
        file_name = raw_url.split("/")[-1]

        try:
            code_response = requests.get(raw_url, timeout=10)
            if code_response.status_code != 200:
                st.warning(
                    f"Dosya alınamadı: {file_name} (HTTP {code_response.status_code})"
                )
                continue

            code = code_response.text

            # Boş dosya kontrolü
            if len(code.strip()) < 10:
                st.info(f"Çok küçük dosya atlandı: {file_name}")
                continue

            st.info(f"İşleniyor: {file_name} ({len(code)} karakter)")

            # Timeout ile LLM çağrıları
            file_summary = summarize_full_file(code)
            functions = extract_functions_code(code)

            if not functions:
                st.warning(f"{file_name}: Fonksiyon bulunamadı")
                continue

            func_results = []

            for func in functions[:10]:  # İlk 10 fonksiyonu analiz et (performans için)
                try:
                    explanation = analyze_function_with_llama(func["code"])
                    optimization = (
                        optimize_function_with_llama(func["code"])
                        if do_optimize
                        else ""
                    )
                    error_check = (
                        check_errors_in_function(func["code"])
                        if do_check_errors
                        else ""
                    )

                    func_results.append(
                        {
                            "name": func["name"],
                            "lineno": func["lineno"],
                            "length": func["length"],
                            "complexity": func["complexity"],
                            "docstring": func.get("docstring"),
                            "explanation": explanation,
                            "optimization": optimization,
                            "error_check": error_check,
                        }
                    )
                except Exception as e:
                    st.warning(f"Fonksiyon analiz hatası ({func['name']}): {e}")
                    continue

            file_analysis = {
                "source_file": file_name,
                "file_summary": file_summary,
                "functions": func_results,
            }
            analysis_results.append(file_analysis)

        except Exception as e:
            st.error(f"Dosya işleme hatası ({file_name}): {e}")
            continue

    return analysis_results


def get_all_py_files(api_url, raw_base, headers):
    py_files = []
    response = requests.get(api_url, headers=headers)
    if response.status_code != 200:
        return py_files

    items = response.json()
    for item in items:
        if item["type"] == "file" and item["name"].endswith(".py"):
            py_files.append(raw_base + item["path"])
        elif item["type"] == "dir":
            sub_api_url = item["url"]
            py_files.extend(get_all_py_files(sub_api_url, raw_base, headers))
    return py_files
