
from pathlib import Path

import pandas as pd
import streamlit as st

from src.data_loader import load_tickets, filter_tickets
from src.ticket_analyzer import analyze_ticket
from src.storage import save_results


PROJECT_ROOT = Path(__file__).resolve().parent
OUTPUT_DIR = PROJECT_ROOT / "outputs"
ANALYZED_FILE = OUTPUT_DIR / "analyzed_tickets.csv"
FILTERED_FILE = OUTPUT_DIR / "filtered_tickets.csv"


st.set_page_config(
    page_title="InsightDesk | Ticket Intelligence",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded",
)


# -------------------- CUSTOM THEME --------------------

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    :root {
        --background: #0b1020;
        --panel: #131b30;
        --border: #27334d;
        --text: #edf2ff;
        --muted: #a3b0ca;
        --violet: #8b5cf6;
        --cyan: #22d3ee;
    }

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    .stApp {
        background:
            radial-gradient(ellipse at 15% 0%, #20234a 0%, transparent 36%),
            radial-gradient(ellipse at 90% 5%, #103747 0%, transparent 28%),
            var(--background);
        color: var(--text);
    }

    [data-testid="stHeader"] {
        background: rgba(11, 16, 32, 0.75);
    }

    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #11182b, #0c1222);
        border-right: 1px solid var(--border);
    }

    [data-testid="stSidebar"] * {
        color: var(--text);
    }

    .hero {
        padding: 30px 32px;
        border: 1px solid #34365e;
        border-radius: 22px;
        background: linear-gradient(120deg, #211c46 0%, #17233f 55%, #103448 100%);
        margin-bottom: 25px;
        box-shadow: 0 15px 45px rgba(0, 0, 0, 0.20);
    }

    .eyebrow {
        color: #67e8f9;
        text-transform: uppercase;
        letter-spacing: 2px;
        font-size: 11px;
        font-weight: 800;
        margin-bottom: 10px;
    }

    .hero h1 {
        color: #ffffff;
        font-size: clamp(27px, 4vw, 39px);
        line-height: 1.2;
        margin: 0 0 12px 0;
        font-weight: 800;
    }

    .hero p {
        color: #c3cee7;
        font-size: 14px;
        margin: 0;
        line-height: 1.8;
    }

    .section-title {
        color: #f1f5ff;
        font-size: 19px;
        font-weight: 750;
        margin: 22px 0 5px 0;
    }

    .section-caption {
        color: #9eacc8;
        font-size: 12px;
        margin-bottom: 15px;
    }

    .metric-card {
        padding: 20px;
        min-height: 143px;
        border-radius: 17px;
        border: 1px solid #2b3650;
        background: linear-gradient(145deg, #18223a, #11192b);
        box-shadow: 0 8px 22px rgba(0, 0, 0, 0.12);
    }

    .metric-top {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 8px;
    }

    .metric-label {
        color: #b0bdd5;
        font-size: 12px;
        font-weight: 600;
    }

    .metric-icon {
        font-size: 23px;
    }

    .metric-value {
        color: #ffffff;
        font-size: 31px;
        font-weight: 800;
        margin-top: 13px;
        line-height: 1.1;
    }

    .metric-note {
        color: #91a1bf;
        font-size: 11px;
        margin-top: 9px;
    }

    .stTextInput input,
    .stSelectbox div[data-baseweb="select"] > div,
    .stMultiSelect div[data-baseweb="select"] > div {
        background-color: #151e33;
        border-color: #34415e;
        border-radius: 10px;
    }

    .stButton button,
    .stDownloadButton button {
        border-radius: 10px;
        border: 1px solid #51418c;
        background: linear-gradient(100deg, #7048e8, #4f46e5);
        color: white;
        font-weight: 650;
    }

    .stButton button:hover,
    .stDownloadButton button:hover {
        border-color: #67e8f9;
        color: white;
    }

    [data-testid="stDataFrame"] {
        border: 1px solid #27334d;
        border-radius: 12px;
        overflow: hidden;
    }

    div[data-testid="stExpander"] {
        border: 1px solid #2b3650;
        border-radius: 12px;
        background: #121a2d;
    }

    hr {
        border-color: #27334d;
    }

    #MainMenu, footer {
        visibility: hidden;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# -------------------- LOAD AND PREPARE DATA --------------------

@st.cache_data(show_spinner="Preparing ticket intelligence...")
def get_ticket_data():
    if ANALYZED_FILE.exists() and FILTERED_FILE.exists():
        analyzed = pd.read_csv(ANALYZED_FILE).fillna("")
        filtered = pd.read_csv(FILTERED_FILE).fillna("")
        return analyzed, filtered

    tickets = load_tickets()
    valid_tickets, filtered_tickets = filter_tickets(tickets)

    analyzed_tickets = []

    for _, ticket in valid_tickets.iterrows():
        analysis = analyze_ticket(ticket["message"])

        analyzed_tickets.append({
            "ticket_id": ticket["ticket_id"],
            "message": ticket["message"],
            **analysis,
        })

    save_results(analyzed_tickets, filtered_tickets)

    return (
        pd.DataFrame(analyzed_tickets),
        filtered_tickets,
    )


try:
    analyzed_df, filtered_df = get_ticket_data()
except Exception as error:
    st.error(f"Unable to load ticket data: {error}")
    st.info(
        "Check that the data folder, source files, and CSV dataset exist."
    )
    st.stop()


# -------------------- SIDEBAR --------------------

with st.sidebar:
    st.markdown(
        """
        <div style="padding: 12px 0 24px 0;">
            <div style="font-size: 32px;">🎯</div>
            <div style="font-size: 21px; font-weight: 800;">
                Insight<span style="color:#a78bfa;">Desk</span>
            </div>
            <div style="font-size: 11px; color:#91a1bf; margin-top:5px;">
                CUSTOMER TICKET INTELLIGENCE
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("---")
    st.markdown("### 🧭 Navigation")

    page = st.radio(
        "Choose a page",
        ["Overview", "Ticket Explorer", "Filtered Messages"],
        label_visibility="collapsed",
    )

    st.markdown("---")
    st.markdown("### 🎛️ Dashboard Filters")

    categories = sorted(
        analyzed_df["category"].dropna().unique().tolist()
    ) if "category" in analyzed_df else []

    priorities = ["Urgent", "High", "Medium", "Low"]

    selected_categories = st.multiselect(
        "Ticket category",
        categories,
        default=categories,
    )

    selected_priorities = st.multiselect(
        "Priority level",
        priorities,
        default=priorities,
    )

    st.markdown("---")

    if st.button("🔄 Refresh dashboard", use_container_width=True):
        get_ticket_data.clear()
        st.rerun()

    st.caption("InsightDesk · Ticket Intelligence")
    st.caption("Rule-based classification engine")


# -------------------- FILTER DATA --------------------

if "category" in analyzed_df.columns:
    filtered_analyzed = analyzed_df[
        analyzed_df["category"].isin(selected_categories)
        & analyzed_df["priority"].isin(selected_priorities)
    ].copy()
else:
    filtered_analyzed = analyzed_df.copy()


# -------------------- HERO --------------------

st.markdown(
    """
    <div class="hero">
        <div class="eyebrow">✦ CUSTOMER SUPPORT ANALYTICS</div>
        <h1>Ticket Intelligence Center</h1>
        <p>
            Turn customer feedback into actionable insights.
            Explore ticket categories, monitor urgency, understand sentiment,
            and review suggested customer replies — all in one workspace.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)


# -------------------- REUSABLE METRIC CARD --------------------

def metric_card(label, value, icon, note, accent):
    st.markdown(
        f"""
        <div class="metric-card" style="border-top:3px solid {accent};">
            <div class="metric-top">
                <span class="metric-label">{label}</span>
                <span class="metric-icon">{icon}</span>
            </div>
            <div class="metric-value">{value}</div>
            <div class="metric-note">{note}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# -------------------- OVERVIEW PAGE --------------------

if page == "Overview":
    st.markdown(
        '<div class="section-title">📊 Performance Overview</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="section-caption">Live summary based on the selected filters.</div>',
        unsafe_allow_html=True,
    )

    total_tickets = len(analyzed_df) + len(filtered_df)
    analyzed_count = len(filtered_analyzed)
    urgent_count = (
        int((filtered_analyzed["priority"] == "Urgent").sum())
        if "priority" in filtered_analyzed else 0
    )
    filtered_count = len(filtered_df)

    columns = st.columns(4, gap="medium")

    with columns[0]:
        metric_card(
            "TOTAL MESSAGES",
            total_tickets,
            "📨",
            "All imported messages",
            "#8b5cf6",
        )

    with columns[1]:
        metric_card(
            "ANALYZED TICKETS",
            analyzed_count,
            "🧠",
            "Valid tickets in current view",
            "#22d3ee",
        )

    with columns[2]:
        metric_card(
            "URGENT TICKETS",
            urgent_count,
            "🚨",
            "Require prompt attention",
            "#fb7185",
        )

    with columns[3]:
        metric_card(
            "FILTERED MESSAGES",
            filtered_count,
            "🛡️",
            "Ignored or rejected messages",
            "#fbbf24",
        )

    st.markdown(
        '<div class="section-title">📈 Support Insights</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="section-caption">Understand what customers are reporting and how they feel.</div>',
        unsafe_allow_html=True,
    )

    left, right = st.columns(2, gap="large")

    with left:
        st.markdown("#### 🗂️ Tickets by Category")

        if not filtered_analyzed.empty:
            category_counts = (
                filtered_analyzed["category"]
                .value_counts()
                .rename_axis("Category")
                .to_frame("Tickets")
            )
            st.bar_chart(
                category_counts,
                x_label="Category",
                y_label="Number of tickets",
                color="#8b5cf6",
            )
        else:
            st.info("No tickets match the current filters.")

    with right:
        st.markdown("#### 🎯 Priority Distribution")

        if not filtered_analyzed.empty:
            priority_counts = (
                filtered_analyzed["priority"]
                .value_counts()
                .reindex(priorities, fill_value=0)
                .rename_axis("Priority")
                .to_frame("Tickets")
            )
            st.bar_chart(
                priority_counts,
                x_label="Priority",
                y_label="Number of tickets",
                color="#fb7185",
            )
        else:
            st.info("No tickets match the current filters.")

    left, right = st.columns(2, gap="large")

    with left:
        st.markdown("#### 💬 Customer Sentiment")

        if not filtered_analyzed.empty:
            sentiment_counts = (
                filtered_analyzed["sentiment"]
                .value_counts()
                .rename_axis("Sentiment")
                .to_frame("Tickets")
            )
            st.bar_chart(
                sentiment_counts,
                x_label="Sentiment",
                y_label="Number of tickets",
                color="#22d3ee",
            )
        else:
            st.info("No sentiment data to display.")

    with right:
        st.markdown("#### ⚡ Priority Snapshot")

        if not filtered_analyzed.empty:
            snapshot = (
                filtered_analyzed["priority"]
                .value_counts()
                .reindex(priorities, fill_value=0)
            )

            for priority, color in [
                ("Urgent", "#fb7185"),
                ("High", "#fb923c"),
                ("Medium", "#fbbf24"),
                ("Low", "#34d399"),
            ]:
                count = int(snapshot.get(priority, 0))
                st.markdown(
                    f"""
                    <div style="display:flex;align-items:center;gap:12px;
                    padding:10px 12px;margin:8px 0;background:#131b30;
                    border:1px solid #27334d;border-radius:10px;">
                        <div style="width:9px;height:9px;border-radius:50%;
                        background:{color};"></div>
                        <div style="flex:1;color:#cbd5e1;font-size:13px;">
                            {priority}
                        </div>
                        <div style="font-weight:800;color:#fff;">
                            {count}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

    st.markdown(
        '<div class="section-title">🧾 Recent Ticket Activity</div>',
        unsafe_allow_html=True,
    )

    if not filtered_analyzed.empty:
        display_columns = [
            column for column in [
                "ticket_id",
                "category",
                "priority",
                "sentiment",
                "product",
            ]
            if column in filtered_analyzed.columns
        ]

        st.dataframe(
            filtered_analyzed[display_columns],
            use_container_width=True,
            hide_index=True,
        )
    else:
        st.info("No tickets are available for this selection.")


# -------------------- TICKET EXPLORER --------------------

elif page == "Ticket Explorer":
    st.markdown(
        '<div class="section-title">🔎 Ticket Explorer</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="section-caption">Search customer messages, inspect classifications, and review suggested replies.</div>',
        unsafe_allow_html=True,
    )

    search_text = st.text_input(
        "Search tickets",
        placeholder="Search ticket ID, message, or product...",
    )

    explorer_df = filtered_analyzed.copy()

    if search_text.strip():
        searchable = (
            explorer_df.astype(str)
            .agg(" ".join, axis=1)
            .str.contains(search_text.strip(), case=False, na=False)
        )
        explorer_df = explorer_df[searchable]

    st.caption(f"{len(explorer_df)} ticket(s) match your search.")

    table_columns = [
        column for column in [
            "ticket_id",
            "category",
            "priority",
            "sentiment",
            "product",
            "message",
        ]
        if column in explorer_df.columns
    ]

    st.dataframe(
        explorer_df[table_columns],
        use_container_width=True,
        hide_index=True,
    )

    st.markdown("#### 📝 Ticket Details")

    if not explorer_df.empty:
        ticket_ids = explorer_df["ticket_id"].astype(str).tolist()

        selected_ticket_id = st.selectbox(
            "Select a ticket",
            ticket_ids,
        )

        ticket_row = explorer_df[
            explorer_df["ticket_id"].astype(str) == selected_ticket_id
        ].iloc[0]

        st.markdown(
            f"""
            <div style="padding:20px;background:#131b30;
            border:1px solid #2b3650;border-radius:15px;">
                <div style="color:#67e8f9;font-size:12px;font-weight:700;">
                    TICKET {ticket_row.get('ticket_id', '')}
                </div>
                <div style="font-size:18px;font-weight:750;color:#fff;
                margin:12px 0;">
                    {ticket_row.get('category', 'N/A')}
                    &nbsp;·&nbsp; {ticket_row.get('priority', 'N/A')}
                </div>
                <div style="color:#cbd5e1;line-height:1.8;">
                    {ticket_row.get('message', '')}
                </div>
                <hr style="border-color:#2b3650;">
                <div style="color:#a5b4fc;font-size:12px;">
                    PRODUCT / FEATURE
                </div>
                <div style="color:#fff;margin:5px 0 15px 0;">
                    {ticket_row.get('product', 'Not identified')}
                </div>
                <div style="color:#a5b4fc;font-size:12px;">
                    SENTIMENT
                </div>
                <div style="color:#fff;margin-top:5px;">
                    {ticket_row.get('sentiment', 'N/A')}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("#### ✉️ Suggested Customer Reply")

        suggested_reply = str(
            ticket_row.get("suggested_reply", "")
        )

        st.text_area(
            "Review and copy the suggested reply",
            value=suggested_reply,
            height=115,
            key=f"reply_{selected_ticket_id}",
        )

        st.caption(
            "This is a draft for review, not an automatically sent message."
        )
    else:
        st.info("No tickets match the search and selected filters.")

    st.markdown("---")

    st.download_button(
        "⬇️ Download analyzed tickets (CSV)",
        data=filtered_analyzed.to_csv(index=False).encode("utf-8-sig"),
        file_name="analyzed_tickets.csv",
        mime="text/csv",
        use_container_width=True,
    )


# -------------------- FILTERED MESSAGES --------------------

elif page == "Filtered Messages":
    st.markdown(
        '<div class="section-title">🛡️ Ignored & Rejected Messages</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="section-caption">Messages excluded from customer ticket analysis, with reasons.</div>',
        unsafe_allow_html=True,
    )

    if filtered_df.empty:
        st.success("No messages were ignored or rejected.")
    else:
        if "status" in filtered_df.columns:
            status_options = sorted(
                filtered_df["status"].dropna().unique().tolist()
            )
            selected_status = st.multiselect(
                "Filter by status",
                status_options,
                default=status_options,
            )
            visible_filtered = filtered_df[
                filtered_df["status"].isin(selected_status)
            ]
        else:
            visible_filtered = filtered_df

        st.dataframe(
            visible_filtered,
            use_container_width=True,
            hide_index=True,
        )

        st.download_button(
            "⬇️ Download filtered messages (CSV)",
            data=visible_filtered.to_csv(index=False).encode("utf-8-sig"),
            file_name="filtered_tickets.csv",
            mime="text/csv",
            use_container_width=True,
        )

    with st.expander("ℹ️ How the analyzer works"):
        st.write(
            "The current version uses keyword-based rules to estimate "
            "ticket category, priority, sentiment, and product or feature. "
            "It is not yet a trained machine-learning model, so classifications "
            "should be reviewed before operational use."
        )


# -------------------- FOOTER --------------------

st.markdown("---")

st.markdown(
    """
    <div style="text-align:center;padding:8px 0 18px 0;">
        <div style="font-weight:750;color:#c4b5fd;">
            InsightDesk · Customer Ticket Intelligence
        </div>
        <div style="font-size:11px;color:#8190ad;margin-top:6px;">
            Built with Python, Pandas & Streamlit · Rule-based analysis
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)