"""
map_visualization.py - Utility functions for interactive map visualizations
Handles choropleth maps, markers, and geographic data processing
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import json
import requests


def get_theme_colors():
    """Get the unified theme colors from CSS variables"""
    return {
        'PRIMARY': '#807A81',
        'ACCENT1': '#6C5C7C',
        'ACCENT2': '#A08692',
        'NEUTRAL1': '#E1C8C2',
        'NEUTRAL2': '#E8DED9',
        'TEXT': '#FFFFFF',
        'BACKGROUND': '#1A1623',
        'INPUT_BG': '#2A2533',
        'white': '#E8DED9'
    }


class MapVisualizer:
    """Manages map visualization and geographic data"""
    
    def __init__(self):
        self.colors = get_theme_colors()
        self.COLORS = ["#2927F7", "#6C5C7C", "#A08692", "#807A81", "#80FAD6"]
        
    @st.cache_data(ttl=3600)
    def load_geojsons(self):
        """Load GeoJSON data for world and India"""
        world_url = "https://raw.githubusercontent.com/holtzy/D3-graph-gallery/master/DATA/world.geojson"
        world_geo = requests.get(world_url).json()
        
        india_geo = None
        try:
            with open('india_states.geojson', 'r') as f:
                india_geo = json.load(f)
        except:
            st.warning("⚠️ india_states.geojson not found. Download from: https://github.com/udit-001/india-maps-data")
        
        return world_geo, india_geo

    @staticmethod
    def get_state_coordinates():
        """Return coordinates for all major Indian states"""
        return {
            'Karnataka': (12.97, 77.59), 
            'Punjab': (30.90, 75.85),
            'Maharashtra': (19.07, 72.87), 
            'West Bengal': (22.57, 88.36),
            'Tamil Nadu': (13.08, 80.27), 
            'Delhi': (28.61, 77.23),
            'Uttar Pradesh': (26.85, 80.95), 
            'Gujarat': (23.02, 72.57),
            'Rajasthan': (27.59, 75.62),
            'Madhya Pradesh': (22.85, 77.99),
            'Andhra Pradesh': (15.91, 78.16),
            'Telangana': (18.11, 79.01),
            'Bihar': (25.59, 85.54),
            'Jharkhand': (23.61, 85.28),
            'Odisha': (20.95, 85.09),
            'Assam': (26.20, 92.94)
        }

    def create_choropleth_map(self, df, geojson, title, color_column='Violations', 
                             color_scale='Viridis', height=700):
        """
        Create an interactive choropleth map
        
        Args:
            df: DataFrame with 'Location' and metric columns
            geojson: GeoJSON data
            title: Map title
            color_column: Column to color by
            color_scale: Plotly color scale
            height: Map height in pixels
        
        Returns:
            Plotly figure object
        """
        fig = px.choropleth_mapbox(
            df,
            geojson=geojson,
            locations='Location',
            color=color_column,
            hover_data={color_column: ':,d'},
            mapbox_style="carto-darkmatter",
            center={"lat": 20.59, "lon": 78.96},
            zoom=4,
            color_continuous_scale=color_scale,
            opacity=0.8,
            title=f"<b>{title}</b>"
        )
        
        fig.update_layout(
            height=height,
            template='plotly_dark',
            title_font_size=20,
            font=dict(size=12, color=self.colors.get('white', '#E8DED9')),
            hoverlabel=dict(bgcolor="#2a2533", font_size=13),
            margin={"r": 0, "t": 50, "l": 0, "b": 0},
            coloraxis_colorbar=dict(
                title=color_column,
                thickness=15,
                len=0.7,
                x=1.02
            )
        )
        
        return fig

    def create_globe_choropleth(self, df, geojson, title, color_column='Violations',
                                color_scale='Plasma_r', height=700):
        """
        Create an interactive globe choropleth with projections
        
        Args:
            df: DataFrame with 'Location' and metric columns
            geojson: GeoJSON data
            title: Map title
            color_column: Column to color by
            color_scale: Plotly color scale
            height: Map height in pixels
        
        Returns:
            Plotly figure object
        """
        fig = px.choropleth(
            df,
            geojson=geojson,
            locations='Location',
            color=color_column,
            color_continuous_scale=color_scale,
            projection="orthographic",
            title=f"<b>{title}</b>",
            hover_data={color_column: ':,d'}
        )
        
        # Orthographic globe settings
        fig.update_geos(
            projection_type="orthographic",
            resolution=110,
            showcountries=True,
            countrycolor="#333",
            countrywidth=1.5,
            landcolor="#1a1b2e",
            showocean=True,
            oceancolor="#0a0e17",
            coastlinecolor="#555",
            coastlinewidth=1.5
        )
        
        # Add projection buttons
        fig.update_layout(
            height=height,
            template='plotly_dark',
            title_font_size=20,
            font=dict(size=12, color=self.colors.get('white', '#E8DED9')),
            updatemenus=[
                dict(
                    buttons=[
                        dict(args=[{"projection.type": "orthographic", "zoom": 2}], 
                             label="🌐 GLOBE", method="relayout"),
                        dict(args=[{"projection.type": "equirectangular", "zoom": 2.2}], 
                             label="🗺️ FLAT", method="relayout"),
                        dict(args=[{"projection.type": "conic conformal", 
                                   "center": {"lat": 20, "lon": 78}, "zoom": 5}],
                             label="🇮🇳 INDIA", method="relayout")
                    ],
                    direction="left",
                    pad={"r": 15, "t": 15},
                    x=0.01, xanchor="left", y=1.02, yanchor="top",
                    bgcolor="#0A0A3D",
                    font=dict(color=self.colors.get('white', '#E8DED9'), size=11)
                )
            ],
            margin={"r": 0, "t": 50, "l": 0, "b": 0}
        )
        
        return fig

    def add_state_labels(self, fig, state_data, offset_x=0, offset_y=0):
        """
        Add state labels to a map figure
        
        Args:
            fig: Plotly figure object
            state_data: DataFrame with Location and count/metric
            offset_x: X-axis offset for labels
            offset_y: Y-axis offset for labels
        """
        state_coords = self.get_state_coordinates()
        
        for _, row in state_data.iterrows():
            state = row['Location']
            if state in state_coords:
                lat, lon = state_coords[state]
                value = int(row.iloc[1])  # Get the metric value (second column)
                
                fig.add_annotation(
                    x=lon + offset_x,
                    y=lat + offset_y,
                    text=f"<b style='color:#94FEFE;font-size:16px'>{state[:2].upper()}</b><br>"
                         f"<span style='color:#80FAD6;font-size:12px'>{value:,}</span>",
                    showarrow=False,
                    font=dict(size=14, color=self.colors.get('white', '#E8DED9')),
                    bgcolor="rgba(0,20,60,0.95)",
                    bordercolor="#6C5C7C",
                    borderwidth=2,
                    borderpad=8,
                    xanchor="center",
                    yanchor="middle"
                )
        
        return fig

    def create_scrollable_card(self, title, content, card_id):
        """
        Create a scrollable card container
        
        Args:
            title: Card title
            content: Card content (can be HTML)
            card_id: Unique identifier for the card
        """
        st.markdown(f"""
        <div class="card-container" id="{card_id}">
            <div class="card-title">{title}</div>
            <div class="card-content">{content}</div>
        </div>
        """, unsafe_allow_html=True)

    @staticmethod
    def filter_dataframe_by_date(df, start_date, end_date, date_column='Date'):
        """
        Filter dataframe by date range
        
        Args:
            df: Input DataFrame
            start_date: Start date (pandas Timestamp)
            end_date: End date (pandas Timestamp)
            date_column: Name of date column
        
        Returns:
            Filtered DataFrame
        """
        if date_column not in df.columns:
            return df
        
        df[date_column] = pd.to_datetime(df[date_column], errors='coerce')
        return df[(df[date_column] >= start_date) & (df[date_column] <= end_date)]

    @staticmethod
    def aggregate_by_location(df, location_column='Location', metric_column='Fine_Amount', 
                             aggregation='sum'):
        """
        Aggregate metrics by location
        
        Args:
            df: Input DataFrame
            location_column: Column containing locations
            metric_column: Column to aggregate
            aggregation: 'sum', 'mean', 'count', 'max'
        
        Returns:
            Aggregated DataFrame
        """
        if aggregation == 'sum':
            return df.groupby(location_column)[metric_column].sum().reset_index(name=f'{metric_column}_Total')
        elif aggregation == 'mean':
            return df.groupby(location_column)[metric_column].mean().reset_index(name=f'{metric_column}_Avg')
        elif aggregation == 'count':
            return df.groupby(location_column).size().reset_index(name='Count')
        elif aggregation == 'max':
            return df.groupby(location_column)[metric_column].max().reset_index(name=f'{metric_column}_Max')
        else:
            return df.groupby(location_column)[metric_column].sum().reset_index(name=f'{metric_column}_Total')


def display_map_metrics(total_violations, top_state, active_states):
    """
    Display key metrics in columns
    
    Args:
        total_violations: Total count of violations
        top_state: State with most violations
        active_states: Number of active states
    """
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("📊 Total Violations", f"{total_violations:,}", 
                 help="Total number of violations in filtered data")
    
    with col2:
        st.metric("🏆 Hottest State", top_state,
                 help="State with highest violations")
    
    with col3:
        st.metric("📍 Active States", active_states,
                 help="Number of states with violations")


def create_comparison_table(df, columns_to_show=None, sort_by=None, ascending=False):
    """
    Create a formatted comparison table
    
    Args:
        df: DataFrame to display
        columns_to_show: List of columns to display
        sort_by: Column to sort by
        ascending: Sort ascending or descending
    
    Returns:
        Formatted DataFrame
    """
    if columns_to_show:
        df = df[columns_to_show]
    
    if sort_by:
        df = df.sort_values(by=sort_by, ascending=ascending)
    
    return df.reset_index(drop=True)


# --- Lightweight page helpers (8 cards + expanders) ---
COLORS = get_theme_colors()


def render_sidebar():
    """Render a minimal sidebar containing only the page selector."""
    # Premium Sidebar with Purple Borders
    with st.sidebar:
        st.markdown(f"<h2 style='color:{COLORS['ACCENT2']};'>Map Visuals</h2>", unsafe_allow_html=True)
        # Page selector with dividers and emoji labels (visual-only emojis)
        page = st.radio(
            "Select Analysis:",
            [
                "🚦 Violation Type Intelligence",
                "🚗 Vehicle Class Hotspots", 
                "👤 Driver Demographics Map",
                "☁️ Weather-Violation Nexus",
                "🗺️ State-Level Risk Matrix",
                "🛣️ Infrastructure Danger Zones",
                "⏰ Peak Hour Violation Peaks",
                "💰 Fine Severity Distribution"
            ],
            index=0,
            format_func=lambda x: x,
            key="page_radio"
        )

        # Visual dividers between options (CSS handles appearance)
        st.markdown('<div class="sidebar-radio-divider"></div>', unsafe_allow_html=True)


def _nav_cards():
    """Render 8 horizontal nav cards (two rows). Sets `st.session_state.scroll_to` when clicked."""
    if 'scroll_to' not in st.session_state:
        st.session_state.scroll_to = None
    nav_cards = [
        ("🚦", "Violation Type Intelligence"),
        ("🚗", "Vehicle Class Hotspots"),
        ("👤", "Driver Demographics Map"),
        ("☁️", "Weather-Violation Nexus"),
        ("🗺️", "State-Level Risk Matrix"),
        ("🛣️", "Infrastructure Danger Zones"),
        ("⏰", "Peak Hour Violation Peaks"),
        ("💰", "Fine Severity Distribution")
    ]

    cols = st.columns(8)
    for i, (icon, title) in enumerate(nav_cards):
        with cols[i]:
            if st.button(f"{icon} {title}", key=f"nav_{i}"):
                st.session_state.scroll_to = i
                st.experimental_rerun()


def _safe_plot_hist(df, col, title):
    """Return a small histogram figure configured for the theme."""
    if col not in df.columns:
        empty = pd.DataFrame({col: []})
        fig = px.histogram(empty, x=col, title=title)
    else:
        fig = px.histogram(df.sample(min(len(df), 2000)), x=col, title=title)

    fig.update_layout(template='plotly_dark', paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    fig.update_layout(font=dict(color=COLORS['TEXT']))
    return fig


def render_expanders(df: pd.DataFrame):
    """Render the 8 expanders using the exact premium titles requested.

    Each expander contains a placeholder subheader and spots for filters, maps and tables.
    """
    st.markdown("---")
    st.markdown("### Filter by Section (click a card above to jump)")

    _nav_cards()

    expanders = [
        "1. Violation Type Intelligence",
        "2. Vehicle Class Hotspots", 
        "3. Driver Demographics Map",
        "4. Weather-Violation Nexus",
        "5. State-Level Risk Matrix",
        "6. Infrastructure Danger Zones",
        "7. Peak Hour Violation Peaks",
        "8. Fine Severity Distribution"
    ]

    for i, title in enumerate(expanders, 1):
        anchor = f"exp{i}"
        with st.expander(title, expanded=False):
            st.markdown(f'<div id="{anchor}"></div>', unsafe_allow_html=True)
            st.subheader(title)
            # Placeholder filters area
            cols = st.columns([2, 1])
            with cols[0]:
                st.selectbox("Filter", options=["All", "Top 10", "Top 25"], key=f"filter_{i}")
            with cols[1]:
                st.button("Apply", key=f"apply_{i}")

            st.markdown("---")
            # Placeholder for a native Plotly map/chart
            fig = _safe_plot_hist(df, df.columns[1] if len(df.columns) > 1 else df.columns[0], title)
            st.plotly_chart(fig, width='stretch')

            st.markdown("---")
            # Placeholder table
            if len(df) > 0:
                st.dataframe(create_comparison_table(df.head(50)), width='stretch')
            else:
                st.info("No data available for this section")


def render_map_page(df: pd.DataFrame):
    """Top-level helper to render the full map page with sidebar, cards and expanders."""
    render_sidebar()
    render_expanders(df)
