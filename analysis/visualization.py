from collections import Counter
import numpy as np
import streamlit as st
from matplotlib import pyplot as plt
import requests

from analysis.function_analysis import extract_modules_from_code


def create_function_chart(analysis_results):
    """En çok kullanılan fonksiyon isimlerinin pasta grafiği"""
    function_names = []
    for file in analysis_results:
        for func in file.get("functions", []):
            function_names.append(func["name"])

    if not function_names:
        return None

    # En çok kullanılan fonksiyon isimlerini say
    func_counter = Counter(function_names)
    top_functions = func_counter.most_common(8)

    if len(top_functions) == 0:
        return None

    fig, ax = plt.subplots(figsize=(10, 8))
    labels = [f"{name} ({count})" for name, count in top_functions]
    sizes = [count for name, count in top_functions]
    colors = plt.cm.Set3(np.linspace(0, 1, len(labels)))

    wedges, texts, autotexts = ax.pie(
        sizes, labels=labels, autopct="%1.1f%%", startangle=90, colors=colors
    )
    ax.set_title("En Çok Kullanılan Fonksiyon İsimleri", fontsize=16, fontweight="bold")

    # Yazı boyutlarını ayarla
    for text in texts:
        text.set_fontsize(10)
    for autotext in autotexts:
        autotext.set_color("white")
        autotext.set_fontweight("bold")

    plt.tight_layout()
    return fig


def create_module_chart(analysis_results):
    """En çok kullanılan modüllerin pasta grafiği"""
    all_modules = []
    for file in analysis_results:
        # Her dosyanın kodundan modülleri çıkar
        code_response = requests.get(
            f"https://raw.githubusercontent.com/{st.session_state.get('username', '')}/{st.session_state.get('repo_name', '')}/master/{file['source_file']}"
        )
        if code_response.status_code == 200:
            modules = extract_modules_from_code(code_response.text)
            all_modules.extend(modules)

    if not all_modules:
        return None

    module_counter = Counter(all_modules)
    top_modules = module_counter.most_common(10)

    if len(top_modules) == 0:
        return None

    fig, ax = plt.subplots(figsize=(10, 8))
    labels = [f"{module} ({count})" for module, count in top_modules]
    sizes = [count for module, count in top_modules]
    colors = plt.cm.Pastel1(np.linspace(0, 1, len(labels)))

    wedges, texts, autotexts = ax.pie(
        sizes, labels=labels, autopct="%1.1f%%", startangle=90, colors=colors
    )
    ax.set_title("En Çok Kullanılan Python Modülleri", fontsize=16, fontweight="bold")

    # Yazı boyutlarını ayarla
    for text in texts:
        text.set_fontsize(10)
    for autotext in autotexts:
        autotext.set_color("white")
        autotext.set_fontweight("bold")

    plt.tight_layout()
    return fig


def create_score_bar(score):
    """Proje puanını bar grafiği olarak göster"""
    fig, ax = plt.subplots(figsize=(12, 2))

    # Bar arka planı
    ax.barh(0, 100, height=0.6, color="lightgray", alpha=0.3)

    # Puan barı - renk gradyanı
    if score >= 80:
        color = "#4CAF50"  # Yeşil
    elif score >= 60:
        color = "#FF9800"  # Turuncu
    else:
        color = "#F44336"  # Kırmızı

    ax.barh(0, score, height=0.6, color=color, alpha=0.8)

    # Puan metni
    ax.text(
        score / 2,
        0,
        f"{score}/100",
        ha="center",
        va="center",
        fontsize=16,
        fontweight="bold",
        color="white",
    )

    # Grafik ayarları
    ax.set_xlim(0, 100)
    ax.set_ylim(-0.5, 0.5)
    ax.set_xlabel("Kullanılabilirlik Puanı", fontsize=12, fontweight="bold")
    ax.set_title(
        "🏆 Proje Kullanılabilirlik Değerlendirmesi", fontsize=14, fontweight="bold"
    )
    ax.set_yticks([])

    # Grid
    ax.grid(True, axis="x", alpha=0.3)

    plt.tight_layout()
    return fig
