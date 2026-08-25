import streamlit as st

def terapkan_gaya_css():
    """Menyuntikkan gaya CSS Custom untuk mempercantik UI Dashboard."""
    st.markdown("""
        <style>
        .main { 
            background-color: #f8f9fa; 
        }
        .main-header { 
            font-size: 2.2rem; 
            font-weight: 700; 
            color: #1E293B; 
            margin-bottom: 0.2rem; 
        }
        .sub-header { 
            font-size: 1rem; 
            color: #64748B; 
            margin-bottom: 1.5rem; 
        }
        .metric-card {
            background: #ffffff; 
            border-radius: 12px; 
            padding: 20px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
            border: 1px solid #e2e8f0; 
            text-align: center;
            transition: transform 0.2s ease;
        }
        .metric-card:hover {
            transform: translateY(-2px);
        }
        .metric-label { 
            font-size: 0.85rem; 
            color: #64748B; 
            font-weight: 600; 
            text-transform: uppercase; 
            letter-spacing: 0.05em;
        }
        .metric-value { 
            font-size: 1.8rem; 
            font-weight: 700; 
            color: #0F172A; 
            margin-top: 5px; 
        }
        .metric-badge { 
            display: inline-block; 
            padding: 4px 12px; 
            border-radius: 20px; 
            font-size: 0.8rem; 
            font-weight: 600; 
            margin-top: 8px; 
        }
        .badge-good { background-color: #DCFCE7; color: #166534; }
        .badge-warning { background-color: #FEF9C3; color: #854D0E; }
        .badge-danger { background-color: #FEE2E2; color: #991B1B; }
        .section-title { 
            font-size: 1.3rem; 
            font-weight: 600; 
            color: #334155; 
            margin-top: 1.5rem; 
            margin-bottom: 1rem; 
            display: flex;
            align-items: center;
            gap: 8px;
        }
        </style>
    """, unsafe_allow_html=True)