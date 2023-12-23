import os
import streamlit as st
import sqlite3
import time
from icv_database import create_table, insert_links
from icv_collections_parser import icv_collections_parsing
from icv_parse_magnet_links import parse_magnet_links
from icv_magnet_checker import check_seeders_and_leechers

# Define collection names for display on the UI
collection_display_names = {
    'film_h264': '📽️ Film H264',
    'film_h265': '📽️ Film H265',
    'serie_h264': '📺 Serie H264',
    'serie_h265': '📺 Serie H265',
    'tv_h264': '📺 TV H264',
}

# Define collection URLs and corresponding table names
collection_urls = {
    'film_h264': [
        'https://www.icv-crew.com/forum/index.php?topic=45246.0',
        'https://www.icv-crew.com/forum/index.php?topic=45245.0',
        'https://www.icv-crew.com/forum/index.php?topic=45244.0',
    ],
    'film_h265': [
        'https://www.icv-crew.com/forum/index.php?topic=45255.0',
        'https://www.icv-crew.com/forum/index.php?topic=45254.0',
        'https://www.icv-crew.com/forum/index.php?topic=45253.0',
    ],
    'serie_h264': [
        'https://www.icv-crew.com/forum/index.php?topic=45262.0',
        'https://www.icv-crew.com/forum/index.php?topic=45261.0',
        'https://www.icv-crew.com/forum/index.php?topic=45260.0',
    ],
    'serie_h265': [
        'https://www.icv-crew.com/forum/index.php?topic=73263.0',
        'https://www.icv-crew.com/forum/index.php?topic=73262.0',
        'https://www.icv-crew.com/forum/index.php?topic=73261.0',
    ],
    'tv_h264': [
        'https://www.icv-crew.com/forum/index.php?topic=12879.0',
    ],
}

# Function to create a table in the database
def refresh_collection_database(table_name, collection_url):
    # Check if the table exists
    conn = sqlite3.connect('./data/parsed_links.db')
    cursor = conn.cursor()
    cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'")
    table_exists = cursor.fetchone()
    conn.close()

    # If the table doesn't exist, create it
    if not table_exists:
        create_table(table_name)
    
    all_links = icv_collections_parsing(collection_url, table_name)
    insert_links(table_name, all_links)
    
# Function to create tables for all collections at startup
def create_tables_at_startup():
    conn = sqlite3.connect('./data/parsed_links.db')
    cursor = conn.cursor()
    
    for table_name, collection_url in collection_urls.items():
        # Check if the table exists
        cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'")
        table_exists = cursor.fetchone()

        if not table_exists:
            create_table(table_name)

    conn.commit()
    conn.close()
    
    st.success("Database ready.")

# Function to clean/empty all tables in the database
def clean_all_tables():
    st.toast('Cleaning database tables... hang tight!', icon='⌛')
    conn = sqlite3.connect('./data/parsed_links.db')
    cursor = conn.cursor()

    # Get a list of all tables in the database
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    # Clean/empty each table
    for table in tables:
        table_name = table[0]
        cursor.execute(f"DELETE FROM {table_name};")

    conn.commit()
    conn.close()
    
    time.sleep(.5)
    st.toast('Done!', icon='🎂')
    st.success("Database tables have been emptied.")

# Function to retrieve links from the database for a selected collection
def get_links_from_database(table_name, search_term=None):
    conn = sqlite3.connect('./data/parsed_links.db')
    cursor = conn.cursor()

    # Check if the table exists
    cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'")
    table_exists = cursor.fetchone()

    if not table_exists:
        st.warning(f"The collection is empty. Please refresh the collection first.")
        return []

    # Build the query based on the presence of a search term
    query = f'SELECT * FROM {table_name}'
    if search_term:
        query += f' WHERE inner_text LIKE "%{search_term}%"'
    
    query += ' ORDER BY inner_text'
    
    cursor.execute(query)
    links = cursor.fetchall()
    conn.close()

    # If the table is empty, display a warning
    if not links:
        st.warning(f"The collection is empty. Please refresh the collection first.")

    return links

# Main Streamlit app
def main(collection_urls, collection_display_names):
    st.title(':green[iCV Magnet Parser :magnet:]')

    # Create a collapsible left column
    with st.sidebar:
        st.title("Collections")
        collection_selected = st.selectbox("Select a collection", list(collection_urls.keys()), format_func=lambda x: collection_display_names[x])

        if st.button(f"Refresh database {collection_display_names[collection_selected]}", use_container_width=True):
            collection_name = collection_display_names[collection_selected]
            st.toast(f'Refreshing collection {collection_name}...', icon='🔄️')
            # Use st.spinner to display a spinner during the database refresh
            with st.spinner(f'Refreshing collection {collection_name}...'):
                refresh_collection_database(collection_selected, collection_urls[collection_selected])

            st.toast(f'Collection {collection_name} refreshed!', icon='✅')
    
        # Create tables for all collections at startup
        create_tables_at_startup()
        
        # Add an empty space
        st.markdown("---")

        # Button to clean/empty all tables in the database
        if st.button(":red[Clean all database tables]", use_container_width=True):
            clean_all_tables()

    # Get search term
    search_term = st.text_input("Search by title:", "").strip()

    # Display links for the selected collection
    st.header(f"{collection_display_names[collection_selected]}")

    # Get links based on the search term
    links = get_links_from_database(collection_selected, search_term)

    # Paginate and display links in a table
    page_size = 25  # You can adjust this as needed

    # Display the current page number
    try:
        page_number = st.number_input("Go to Page", min_value=1, max_value=(len(links) - 1) // page_size + 1, value=1, key="page_number_input")
    except:
        st.stop()
    st.markdown("<style>.step-down {width: 3em !important; border-left: 1px solid #62657c !important; background: #262730;}</style>", unsafe_allow_html=True)
    st.markdown("<style>.step-up {width: 3em !important; border-left: 1px solid #62657c !important; background: #262730;}</style>", unsafe_allow_html=True)

    # Calculate the start and end index for the selected page
    start_index = (page_number - 1) * page_size
    end_index = min(start_index + page_size, len(links))

    # Display links for the selected page
    paginated_links = links[start_index:end_index]

    for link in paginated_links:
        # Check if the row is expanded
        row_expander = st.expander(f"{link[2]}", expanded=False)
        with row_expander:
            # Set the link URL for the expanded row
            link_url = link[1]

            # Create a unique key for the button using the link URL
            parse_button_key = f"parse_button_{link_url}"

            # Add a button to trigger parsing of magnet links
            parse_button_col, emoji_col = st.columns([9, 1])
            if parse_button_col.button("Parse Magnet Links", key=parse_button_key):
                # Call the script to parse magnet links and display them
                magnet_links = parse_magnet_links(link_url)
                print("Starting parsing")
                if magnet_links:
                    st.header("Magnet Links")
                    for magnet_link, inner_text in magnet_links:
                        # Use st.columns to display text and link in separate columns
                        inner_text_col, seeders_col, leechers_col, magnet_link_col = st.columns([7, 0.5, 0.5, 1])

                        # Display Seeders and Leechers
                        seeders, leechers = check_seeders_and_leechers(magnet_link)
                        inner_text_col.write(inner_text)
                        seeders_col.write(f'<span style="color: #3dd56d"><strong>{seeders}</strong></a>', unsafe_allow_html=True)
                        leechers_col.write(f'<span style="color: #fcfc03">{leechers}</a>', unsafe_allow_html=True)
                        magnet_link_col.write(f'<a href="{magnet_link}">🧲</a>', unsafe_allow_html=True)
                emoji_col.write(f'<a href="{link_url}">🔗</a>', unsafe_allow_html=True)

if __name__ == "__main__":
    main(collection_urls, collection_display_names)
