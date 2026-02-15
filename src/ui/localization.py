import streamlit as st

TRANSLATIONS = {
    "en": {
        "page_title": "IndustAIQ Console",
        "app_tagline": "Intelligent Diagnostics",
        "connecting": "Connecting to Telemetry Stream...",
        "system_malfunction": "System Malfunction: Internal processing error.",
        "system_nominal": "SYSTEM NOMINAL",
        "signal_label": "Signal",
        "critical_fault": "CRITICAL FAULT EVENT",
        "remediation_protocol": "Remediation Protocol",
        "reference_documents": "Reference Documents",
        "system_logs": "System Logs",
        "view_alarm_history": "View Alarm History",
        "download_report": "Download Report",
        "no_data": "No historical data available.",
        "runtime_exception": "Runtime Exception",
        "user_badge": "Operator"
    },
    "tr": {
        "page_title": "IndustAIQ Konsolu",
        "app_tagline": "Akıllı Teşhis Sistemi",
        "connecting": "Telemetri Akışına Bağlanılıyor...",
        "system_malfunction": "Sistem Arızası: Dahili işlem hatası.",
        "system_nominal": "SİSTEM NORMAL",
        "signal_label": "Sinyal",
        "critical_fault": "KRİTİK ARIZA OLAYI",
        "remediation_protocol": "Çözüm Protokolü",
        "reference_documents": "Referans Belgeler",
        "system_logs": "Sistem Günlükleri",
        "view_alarm_history": "Alarm Geçmişini Görüntüle",
        "download_report": "Raporu İndir",
        "no_data": "Geçmiş veri bulunamadı.",
        "runtime_exception": "Çalışma Zamanı Hatası",
        "user_badge": "Operatör"
    },
    "de": {
        "page_title": "IndustAIQ Konsole",
        "app_tagline": "Intelligentes Diagnosesystem",
        "connecting": "Verbindung zum Telemetrie-Stream wird hergestellt...",
        "system_malfunction": "Systemstörung: Interner Verarbeitungsfehler.",
        "system_nominal": "SYSTEM NOMINAL",
        "signal_label": "Signal",
        "critical_fault": "KRITISCHES STÖRUNGS EREIGNIS",
        "remediation_protocol": "Abhilfeprotokoll",
        "reference_documents": "Referenzdokumente",
        "system_logs": "Systemprotokolle",
        "view_alarm_history": "Alarmverlauf anzeigen",
        "download_report": "Bericht herunterladen",
        "no_data": "Keine historischen Daten verfügbar.",
        "runtime_exception": "Laufzeitfehler",
        "user_badge": "Bediener"
    },
    "es": {
        "page_title": "Consola IndustAIQ",
        "app_tagline": "Diagnóstico Inteligente",
        "connecting": "Conectando al flujo de telemetría...",
        "system_malfunction": "Mal funcionamiento del sistema: Error interno.",
        "system_nominal": "SISTEMA NOMINAL",
        "signal_label": "Señal",
        "critical_fault": "EVENTO DE FALLO CRÍTICO",
        "remediation_protocol": "Protocolo de Remediación",
        "reference_documents": "Documentos de Referencia",
        "system_logs": "Registros del Sistema",
        "view_alarm_history": "Ver Historial de Alarmas",
        "download_report": "Descargar Informe",
        "no_data": "No hay datos históricos disponibles.",
        "runtime_exception": "Excepción en tiempo de ejecución",
        "user_badge": "Operador"
    },
    "fr": {
        "page_title": "Console IndustAIQ",
        "app_tagline": "Diagnostics Intelligents",
        "connecting": "Connexion au flux de télémétrie...",
        "system_malfunction": "Dysfonctionnement du système : Erreur interne.",
        "system_nominal": "SYSTÈME NOMINAL",
        "signal_label": "Signal",
        "critical_fault": "ÉVÉNEMENT DE DÉFAILLANCE CRITIQUE",
        "remediation_protocol": "Protocole de Remédiation",
        "reference_documents": "Documents de Référence",
        "system_logs": "Journaux Système",
        "view_alarm_history": "Voir l'Historique des Alarmes",
        "download_report": "Télécharger le Rapport",
        "no_data": "Aucune donnée historique disponible.",
        "runtime_exception": "Exception d'exécution",
        "user_badge": "Opérateur"
    },
    "zh": {
        "page_title": "IndustAIQ 控制台",
        "app_tagline": "智能诊断系统",
        "connecting": "正在连接遥测流...",
        "system_malfunction": "系统故障：内部处理错误。",
        "system_nominal": "系统正常",
        "signal_label": "信号",
        "critical_fault": "严重故障事件",
        "remediation_protocol": "补救协议",
        "reference_documents": "参考文档",
        "system_logs": "系统日志",
        "view_alarm_history": "查看报警历史",
        "download_report": "下载报告",
        "no_data": "暂无历史数据。",
        "runtime_exception": "运行时异常",
        "user_badge": "操作员"
    },
    "ja": {
        "page_title": "IndustAIQ コンソール",
        "app_tagline": "インテリジェント診断",
        "connecting": "テレメトリストリームに接続中...",
        "system_malfunction": "システム誤動作：内部処理エラー。",
        "system_nominal": "システム正常",
        "signal_label": "信号",
        "critical_fault": "重大な障害イベント",
        "remediation_protocol": "修復プロトコル",
        "reference_documents": "参照ドキュメント",
        "system_logs": "システムログ",
        "view_alarm_history": "アラーム履歴を表示",
        "download_report": "レポートをダウンロード",
        "no_data": "履歴データはありません。",
        "runtime_exception": "実行時例外",
        "user_badge": "オペレーター"
    },
    "pt": {
        "page_title": "Console IndustAIQ",
        "app_tagline": "Diagnóstico Inteligente",
        "connecting": "Conectando ao fluxo de telemetria...",
        "system_malfunction": "Mau funcionamento do sistema: Erro interno.",
        "system_nominal": "SISTEMA NOMINAL",
        "signal_label": "Sinal",
        "critical_fault": "EVENTO DE FALHA CRÍTICA",
        "remediation_protocol": "Protocolo de Correção",
        "reference_documents": "Documentos de Referência",
        "system_logs": "Logs do Sistema",
        "view_alarm_history": "Ver Histórico de Alarmes",
        "download_report": "Baixar Relatório",
        "no_data": "Não há dados históricos disponíveis.",
        "runtime_exception": "Exceção de tempo de execução",
        "user_badge": "Operador"
    },
    "ru": {
        "page_title": "Консоль IndustAIQ",
        "app_tagline": "Интеллектуальная диагностика",
        "connecting": "Подключение к потоку телеметрии...",
        "system_malfunction": "Сбой системы: Внутренняя ошибка обработки.",
        "system_nominal": "СИСТЕМА В НОРМЕ",
        "signal_label": "Сигнал",
        "critical_fault": "КРИТИЧЕСКИЙ СБОЙ",
        "remediation_protocol": "Протокол восстановления",
        "reference_documents": "Справочные документы",
        "system_logs": "Системные журналы",
        "view_alarm_history": "Просмотр истории сигналов",
        "download_report": "Скачать отчет",
        "no_data": "Нет исторических данных.",
        "runtime_exception": "Ошибка выполнения",
        "user_badge": "Оператор"
    },
    "it": {
        "page_title": "Console IndustAIQ",
        "app_tagline": "Diagnostica Intelligente",
        "connecting": "Connessione al flusso di telemetria...",
        "system_malfunction": "Malfunzionamento del sistema: Errore interno.",
        "system_nominal": "SISTEMA NOMINALE",
        "signal_label": "Segnale",
        "critical_fault": "EVENTO DI GUASTO CRITICO",
        "remediation_protocol": "Protocollo di Ripristino",
        "reference_documents": "Documenti di Riferimento",
        "system_logs": "Log di Sistema",
        "view_alarm_history": "Visualizza Cronologia Allarmi",
        "download_report": "Scarica Rapporto",
        "no_data": "Nessun dato storico disponibile.",
        "runtime_exception": "Eccezione di Runtime",
        "user_badge": "Operatore"
    }
}

def get_text(key):
    """
    Returns the translation for the given key based on the current session state language.
    Defaults to 'en' if language is not set or key is missing.
    """
    lang = st.session_state.get("language", "en")
    return TRANSLATIONS.get(lang, TRANSLATIONS["en"]).get(key, key)

def toggle_language():
    """Toggles the language between English and Turkish."""
    current_lang = st.session_state.get("language", "en")
    st.session_state.language = "tr" if current_lang == "en" else "en"
