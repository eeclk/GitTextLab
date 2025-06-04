import json
import streamlit as st
from analysis.github_analysis import analyze_github_repository
from analysis.visualization import (
    create_function_chart,
    create_module_chart,
    create_score_bar,
)
from analysis.shared import score_project_with_llama
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "deepseek-coder:6.7b"


# --- Streamlit Arayüzü ---

st.set_page_config(page_title="GitTextLab", layout="wide", page_icon="🛠️")

# Responsive theme-aware styling
st.markdown(
    """
<style>
    /* Light theme variables */
    :root {
        --bg-primary: #ffffff;
        --bg-secondary: #f8f9fa;
        --bg-gradient-start: #667eea;
        --bg-gradient-end: #764ba2;
        --text-primary: #212529;
        --text-secondary: #6c757d;
        --text-on-dark: #ffffff;
        --border-color: #dee2e6;
        --shadow-light: rgba(0, 0, 0, 0.1);
        --shadow-medium: rgba(0, 0, 0, 0.15);
    }
    
    /* Dark theme detection */
    @media (prefers-color-scheme: dark) {
        :root {
            --bg-primary: #1e1e1e;
            --bg-secondary: #2d2d2d;
            --bg-gradient-start: #4a90e2;
            --bg-gradient-end: #7b68ee;
            --text-primary: #ffffff;
            --text-secondary: #cccccc;
            --text-on-dark: #ffffff;
            --border-color: #404040;
            --shadow-light: rgba(255, 255, 255, 0.1);
            --shadow-medium: rgba(255, 255, 255, 0.15);
        }
    }
    
    /* Streamlit dark theme override */
    .stApp[data-theme="dark"] {
        --bg-primary: #0e1117;
        --bg-secondary: #262730;
        --bg-gradient-start: #4a90e2;
        --bg-gradient-end: #7b68ee;
        --text-primary: #fafafa;
        --text-secondary: #cccccc;
        --text-on-dark: #ffffff;
        --border-color: #404040;
        --shadow-light: rgba(255, 255, 255, 0.05);
        --shadow-medium: rgba(255, 255, 255, 0.1);
    }
    
    .main-header {
        background: linear-gradient(90deg, var(--bg-gradient-start) 0%, var(--bg-gradient-end) 100%);
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 2rem;
        color: var(--text-on-dark) !important;
        box-shadow: 0 8px 25px var(--shadow-medium);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .main-header h1 {
        font-size: 2.5rem;
        margin: 0;
        color: var(--text-on-dark) !important;
        text-shadow: 2px 2px 8px rgba(0,0,0,0.4);
        font-weight: 700;
    }
    
    .main-header p {
        color: rgba(255, 255, 255, 0.9) !important;
        margin-top: 1rem;
        font-size: 1.2rem;
        text-shadow: 1px 1px 3px rgba(0,0,0,0.3);
    }
    
    .stForm {
        background: var(--bg-primary) !important;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 4px 20px var(--shadow-light);
        border: 1px solid var(--border-color);
    }
    
    .chart-container {
        background: var(--bg-primary) !important;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 15px var(--shadow-light);
        margin: 1rem 0;
        border: 1px solid var(--border-color);
    }
    
    .gradient-header {
        background: linear-gradient(90deg, var(--bg-gradient-start) 0%, var(--bg-gradient-end) 100%);
        padding: 1.5rem;
        border-radius: 10px;
        margin: 2rem 0;
        text-align: center;
        color: var(--text-on-dark) !important;
        box-shadow: 0 4px 15px var(--shadow-medium);
    }
    
    .gradient-header h2 {
        color: var(--text-on-dark) !important;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        font-weight: 600;
    }
    
    .info-card {
        background: var(--bg-secondary) !important;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        border-left: 4px solid var(--bg-gradient-start);
        box-shadow: 0 2px 10px var(--shadow-light);
        border: 1px solid var(--border-color);
    }
    
    .function-card {
        background: linear-gradient(135deg, var(--bg-secondary) 0%, var(--bg-primary) 100%);
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
        border-left: 4px solid var(--bg-gradient-start);
        box-shadow: 0 3px 12px var(--shadow-light);
        border: 1px solid var(--border-color);
    }
    
    .function-card h4 {
        color: var(--text-primary) !important;
        margin: 0;
        font-weight: 600;
    }
    
    .function-card span {
        color: var(--text-secondary) !important;
    }
    
    .footer-gradient {
        background: linear-gradient(90deg, var(--bg-gradient-start) 0%, var(--bg-gradient-end) 100%);
        padding: 2rem;
        border-radius: 15px;
        margin-top: 3rem;
        text-align: center;
        box-shadow: 0 6px 20px var(--shadow-medium);
    }
    
    .footer-gradient p {
        color: var(--text-on-dark) !important;
        margin: 0;
        font-size: 1.1rem;
        text-shadow: 1px 1px 3px rgba(0,0,0,0.3);
    }
    
    .footer-gradient p:last-child {
        color: rgba(255, 255, 255, 0.85) !important;
        margin: 0.5rem 0 0 0;
        font-size: 0.95rem;
    }
    
    /* Form styling fixes */
    .stSelectbox label, .stTextInput label, .stCheckbox label {
        color: var(--text-primary) !important;
        font-weight: 500;
    }
    
    /* Button styling */
    .stFormSubmitButton button {
        background: linear-gradient(90deg, var(--bg-gradient-start) 0%, var(--bg-gradient-end) 100%) !important;
        color: var(--text-on-dark) !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 0.75rem 2rem !important;
        font-weight: 600 !important;
        box-shadow: 0 4px 15px var(--shadow-medium) !important;
        transition: all 0.3s ease !important;
    }
    
    .stFormSubmitButton button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px var(--shadow-medium) !important;
    }
</style>
""",
    unsafe_allow_html=True,
)

st.markdown(
    """
<div class="main-header">
    <h1>🛠️ GitHub Python Kod Analizi ve Görüntüleyici</h1>
    <p style="font-size: 1.2rem; margin-top: 1rem; opacity: 0.9;">
        Python projelerinizi analiz edin, optimize edin ve görselleştirin
    </p>
</div>
""",
    unsafe_allow_html=True,
)

with st.form("analyze_form"):
    st.markdown("### 🔍 Analiz Bilgileri")

    col1, col2 = st.columns(2)
    with col1:
        username = st.text_input("GitHub Kullanıcı Adı", placeholder="örnek: microsoft")
    with col2:
        repo_name = st.text_input("Repo Adı", placeholder="örnek: vscode")

    st.markdown("### ⚙️ Analiz Seçenekleri")

    # Ana seçenekler
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**🔧 Kod Analizi**")
        do_optimize = st.checkbox(
            "🚀 Fonksiyonları optimize et",
            help="Kodlarınız için optimizasyon önerileri alın",
        )
        do_check_errors = st.checkbox(
            "🐛 Hata analizi yap", help="Potansiyel hataları ve riskleri tespit edin"
        )

    with col2:
        st.markdown("**📊 Görselleştirme Seçenekleri**")
        show_function_chart = st.checkbox(
            "📈 Fonksiyon Analizi Grafiği",
            value=True,
            help="En çok kullanılan fonksiyonları göster",
        )
        show_module_chart = st.checkbox(
            "📦 Modül Kullanımı Grafiği",
            value=True,
            help="En çok kullanılan Python modüllerini göster",
        )
        show_score_bar = st.checkbox(
            "🏆 Proje Puanlama Barı", value=True, help="AI tabanlı proje kalite puanı"
        )

    st.markdown("---")
    submitted = st.form_submit_button("🚀 Analizi Başlat", use_container_width=True)

if submitted:
    if not username or not repo_name:
        st.warning("Lütfen hem kullanıcı adı hem repo adını girin.")
    else:
        # Session state'e kaydet (grafiklerde kullanmak için)
        st.session_state["username"] = username
        st.session_state["repo_name"] = repo_name

        with st.spinner("Analiz yapılıyor, lütfen bekleyin..."):
            results = analyze_github_repository(
                username, repo_name, do_optimize, do_check_errors
            )
            if results:
                json_path = f"{username}_{repo_name}_analysis.json"
                with open(json_path, "w", encoding="utf-8") as f:
                    json.dump(results, f, indent=4, ensure_ascii=False)
                st.success(f"Analiz tamamlandı ve '{json_path}' dosyasına kaydedildi.")

                # Grafikleri göster
                if show_function_chart or show_module_chart or show_score_bar:
                    st.markdown(
                        """
                    <div class="gradient-header">
                        <h2>📊 Proje İstatistikleri ve Grafikler</h2>
                    </div>
                    """,
                        unsafe_allow_html=True,
                    )

                col1, col2 = st.columns(2)

                # Fonksiyon grafiği
                st.markdown("#### 🔧 Fonksiyon Analizi")
                if show_function_chart:
                    with col1:
                        # st.markdown(
                        #     '<div class="chart-container">', unsafe_allow_html=True
                        # )

                        func_chart = create_function_chart(results)
                        if func_chart:
                            st.pyplot(func_chart)
                        else:
                            st.info(
                                "🔍 Fonksiyon grafiği için yeterli veri bulunamadı."
                            )
                        st.markdown("</div>", unsafe_allow_html=True)

                # Modül grafiği
                if show_module_chart:
                    with col2:
                        # st.markdown(
                        #     '<div class="chart-container">', unsafe_allow_html=True
                        # )
                        # st.markdown("#### 📦 Modül Kullanımı")
                        module_chart = create_module_chart(results)
                        if module_chart:
                            st.pyplot(module_chart)
                        else:
                            st.info("🔍 Modül grafiği için yeterli veri bulunamadı.")
                        st.markdown("</div>", unsafe_allow_html=True)

                # Proje puanlama barı
                if show_score_bar:
                    # st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                    with st.spinner("🤖 AI modeli projeyi değerlendiriyor..."):
                        score = score_project_with_llama(results)
                        score_chart = create_score_bar(score)
                        st.pyplot(score_chart)

                        # Puanlama açıklaması
                        col1, col2, col3 = st.columns([1, 2, 1])
                        with col2:
                            if score >= 80:
                                st.success(
                                    f"🎉 **Mükemmel!** Projeniz **{score}** puan aldı. Kod kalitesi çok yüksek."
                                )
                            elif score >= 60:
                                st.warning(
                                    f"👍 **İyi!** Projeniz **{score}** puan aldı. Bazı iyileştirmeler yapılabilir."
                                )
                            else:
                                st.error(
                                    f"🔧 **Geliştirilmeli!** Projeniz **{score}** puan aldı. Kod kalitesini artırmaya odaklanın."
                                )
                    st.markdown("</div>", unsafe_allow_html=True)

                st.markdown(
                    """
                <div class="gradient-header">
                    <h2>📋 Detaylı Analiz Sonuçları</h2>
                </div>
                """,
                    unsafe_allow_html=True,
                )

                # Detaylı sonuçları göster
                for i, file in enumerate(results):
                    with st.expander(
                        f"📄 **{file['source_file']}** ({len(file.get('functions', []))} fonksiyon)",
                        expanded=(i == 0),
                    ):
                        st.markdown(
                            """
                        <div class="info-card">
                            <strong style="color: var(--text-primary);">📝 Dosya Özeti:</strong>
                        </div>
                        """,
                            unsafe_allow_html=True,
                        )
                        st.info(file["file_summary"])

                        for j, func in enumerate(file.get("functions", [])):
                            st.markdown(
                                f"""
                            <div class="function-card">
                                <h4>
                                    🔧 {func.get("name", "isimsiz")} 
                                    <span>
                                        (Satır: {func.get("lineno", "?")} | Uzunluk: {func.get("length", "?")} | Karmaşıklık: {func.get("complexity", "?")})
                                    </span>
                                </h4>
                            </div>
                            """,
                                unsafe_allow_html=True,
                            )

                            with st.container():
                                st.markdown("**💡 Açıklama:**")
                                st.markdown(
                                    func.get("explanation", "Açıklama bulunamadı.")
                                )

                                if do_optimize and func.get("optimization"):
                                    st.markdown("**🚀 Optimizasyon Önerisi:**")
                                    st.code(
                                        func.get("optimization", "Yok"),
                                        language="python",
                                    )

                                if do_check_errors and func.get("error_check"):
                                    st.markdown("**🐛 Hata ve Risk Analizi:**")
                                    st.warning(
                                        func.get(
                                            "error_check",
                                            "Belirtilen bir hata analizi bulunamadı.",
                                        )
                                    )

                            if j < len(file.get("functions", [])) - 1:
                                st.markdown("---")
            else:
                st.error("Analiz için geçerli bir sonuç alınamadı.")

# Footer
st.markdown(
    """
<div class="footer-gradient">
    <p>
        💡 <strong>İpucu:</strong> Daha detaylı analiz için optimizasyon ve hata kontrolü seçeneklerini aktif edebilirsiniz!
    </p>
    <p>
        🤖 AI destekli kod analizi ile projelerinizi geliştirin
    </p>
</div>
""",
    unsafe_allow_html=True,
)
