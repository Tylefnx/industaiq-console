import streamlit as st

def init_page_layout():
    """Tüm sayfa tasarımını ve CSS ayarlarını yükler."""
    st.markdown("""
        <style>
            /* 1. Temizlik ve Reset */
            [data-testid="stSidebar"], [data-testid="stSidebarNav"] { display: none !important; }
            [data-testid="stStatusWidget"] { visibility: hidden; display: none !important; }
            [data-testid="stHeader"] { display: none !important; }
            
            /* 2. Global Genişlik ve Arka Plan */
            [data-testid="stAppViewBlockContainer"] {
                padding: 1rem 2rem !important;
                max-width: 100% !important;
            }
            .stApp {
                background-color: #0d1117; /* GitHub Dark Dimmed */
            }
            
            /* 3. Dropdown Fixes */
            /* Streamlit columns often clip overflow. We need to help it. */
            div[data-testid="column"] {
                overflow: visible !important; 
            }
            
            /* 4. Dropdown Container & Button */
            .dropdown {
                position: relative;
                display: inline-block;
            }
            .dropbtn {
                background: linear-gradient(180deg, #21262d 0%, #161b22 100%);
                color: #c9d1d9;
                padding: 8px 16px;
                font-family: 'Segoe UI', monospace;
                font-size: 0.9rem;
                border: 1px solid #30363d;
                border-radius: 6px;
                cursor: pointer;
                transition: all 0.2s cubic-bezier(0.3, 0, 0.5, 1);
                display: flex;
                align-items: center;
                gap: 8px;
                box-shadow: 0 1px 0 rgba(27,31,35,0.04), inset 0 1px 0 rgba(255,255,255,0.01);
            }
            .dropbtn:hover {
                background: #30363d;
                border-color: #8b949e;
                color: #f0f6fc;
                transform: translateY(-1px);
                box-shadow: 0 3px 6px rgba(0,0,0,0.2);
            }
            
            /* 5. Dropdown Content (Menu) */
            .dropdown-content {
                display: none;
                position: absolute;
                right: 0;
                top: 100%;
                /* Remove margin-top to prevent gap, use padding instead if needed to push visual box down */
                padding-top: 10px; 
                min-width: 160px;
                z-index: 99999;
            }
            
            /* The actual visible menu box */
            .dropdown-menu-inner {
                background-color: #161b22;
                border: 1px solid #30363d;
                border-radius: 8px;
                box-shadow: 0 8px 24px rgba(0,0,0,0.5), 0 2px 8px rgba(0,0,0,0.3);
                overflow: hidden;
            }
            
            /* Show logic */
            .dropdown:hover .dropdown-content {
                display: block;
                animation: fadeIn 0.2s;
            }
            
            @keyframes fadeIn {
                from { opacity: 0; transform: translateY(-10px); }
                to { opacity: 1; transform: translateY(0); }
            }
            
            /* Links inside dropdown */
            .dropdown-content a {
                color: #c9d1d9;
                padding: 10px 12px;
                text-decoration: none;
                display: block;
                font-size: 0.85rem;
                font-weight: 500;
                transition: background 0.15s;
            }
            .dropdown-content a:hover {
                background-color: #1f6feb; /* Brand Blue */
                color: white;
            }
            
            /* 6. Brand Styling */
            .brand { 
                font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
                font-size: 1.8rem; 
                font-weight: 700; 
                color: #f0f6fc; 
                letter-spacing: -0.5px;
                display: flex;
                align-items: center;
                gap: 12px;
                text-shadow: 0 2px 4px rgba(0,0,0,0.5);
            }
            .brand-icon {
                font-size: 2rem;
                filter: drop-shadow(0 0 15px rgba(88, 166, 255, 0.3));
            }
            
            /* 7. Native Column Gap Override */
            /* Force the last two columns (User and Lang) to be closer */
            div[data-testid="column"]:nth-last-child(2) {
                display: flex;
                justify-content: flex-end;
                padding-right: 0 !important;
            }
            div[data-testid="column"]:last-child {
                padding-left: 0 !important;
                margin-left: -1rem; /* Pull language dropdown closer to user pill */
            }
            
            /* 8. User Pill */
            .user-pill {
                display: flex;
                align-items: center;
                gap: 10px;
                background: #0d1117;
                border: 1px solid #30363d;
                padding: 6px 16px;
                border-radius: 100px;
                color: #7ee787;
                font-size: 0.85rem;
                font-weight: 600;
                box-shadow: inset 0 0 10px rgba(0,0,0,0.5);
                white-space: nowrap;
                height: 42px; /* Fix height to match selectbox */
            }
            .status-indicator {
                width: 8px;
                height: 8px;
                background-color: #238636;
                border-radius: 50%;
                box-shadow: 0 0 8px #238636;
                animation: pulse 2s infinite;
                flex-shrink: 0; /* Prevent indicator from squishing */
            }
            .user-text {
                overflow: hidden;
                text-overflow: ellipsis;
                white-space: nowrap;
                max-width: 15vw; /* Dynamic max width */
                min-width: 0;   /* Allow flex child to shrink below content size */
                display: block; /* Required for ellipsis on span */
            }
            
            /* 9. Popover & Button Styling (The "Real" Hybrid Solution) */
            
            /* Target the Popover Button itself */
            div[data-testid="stPopover"] button {
                background: linear-gradient(180deg, #21262d 0%, #161b22 100%);
                color: #c9d1d9;
                border: 1px solid #30363d;
                border-radius: 6px;
                min-height: 40px;
                box-shadow: 0 1px 0 rgba(27,31,35,0.04), inset 0 1px 0 rgba(255,255,255,0.01);
                transition: all 0.2s;
                font-family: 'Segoe UI', monospace;
                font-size: 0.9rem;
                justify-content: flex-start; /* Left align icon/text */
                width: 100%;
                transform: translateY(6px); /* Use transform for reliable visual positioning */
            }
            div[data-testid="stPopover"] > button:hover {
                background: #30363d;
                border-color: #8b949e;
                color: #f0f6fc;
            }
            /* Remove default Streamlit button arrow if possible or style it */
            div[data-testid="stPopover"] button::after {
                display: none; 
            }
            
            /* Target the Menu Items (Buttons inside Popover) */
            /* We need to be specific to not affect other buttons */
            div[data-testid="stPopoverBody"] button {
                background-color: transparent;
                border: none;
                color: #c9d1d9;
                text-align: left;
                padding: 8px 12px;
                font-size: 0.85rem;
                font-weight: 500;
                transition: background 0.15s;
                border-radius: 4px;
            }
            div[data-testid="stPopoverBody"] button:hover {
                background-color: #1f6feb; /* Brand Blue */
                color: white;
                border: none;
            }
            div[data-testid="stPopoverBody"] button:focus {
                color: white;
                border: none;
                box-shadow: none;
            }
            div[data-testid="stPopoverBody"] {
                padding: 6px;
                background-color: #161b22;
                border: 1px solid #30363d;
            }
        </style>
    """, unsafe_allow_html=True)
