import streamlit as st
import pandas as pd
import os

# Set page configuration
st.set_page_config(
    page_title="Spotify Songs Search",
    layout="wide"
)

# File path
updated_spotify_data_csv = "updated_spotify_data.csv"

def load_songs():
    """Load songs from CSV file"""
    if os.path.exists(updated_spotify_data_csv):
        return pd.read_csv(updated_spotify_data_csv)
    else:
        st.error(f"File '{updated_spotify_data_csv}' not found. Please make sure your data file exists.")
        return pd.DataFrame()

def main():
    st.title("Spotify Songs Search")
    st.markdown("Search and filter through your Spotify songs collection")
    st.markdown("---")
    
    # Load songs data
    songs_df = load_songs()
    
    if songs_df.empty:
        st.warning("No songs data available. Please check if your CSV file exists and contains data.")
        return
    
    # Display basic statistics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Songs", len(songs_df))
    with col2:
        st.metric("Unique Artists", songs_df['artist_name'].nunique())
    with col3:
        st.metric("Years Range", f"{songs_df['year'].min()}-{songs_df['year'].max()}")
    with col4:
        st.metric("Genres", songs_df['genre'].nunique())
    
    st.markdown("---")
    
    # Search and filters section
    st.header("Search Filters")
    
    col1, col2 = st.columns(2)
    
    with col1:
        artist_name = st.text_input("Artist Name", placeholder="Search by artist name...")
        track_name = st.text_input("Track Name", placeholder="Search by track name...")
    
    with col2:
        # Year range filter
        min_year = int(songs_df['year'].min())
        max_year = int(songs_df['year'].max())
        year_range = st.slider(
            "Year Range",
            min_value=min_year,
            max_value=max_year,
            value=(min_year, max_year)
        )
        
        # Genre filter
        all_genres = sorted(songs_df['genre'].unique().tolist())
        selected_genres = st.multiselect(
            "Genres",
            options=all_genres,
            default=all_genres,
            placeholder="Select genres..."
        )
    
    # Search button
    if st.button("Search Songs", type="primary"):
        # Apply filters
        filtered_songs = songs_df.copy()
        
        # Artist name filter
        if artist_name:
            filtered_songs = filtered_songs[
                filtered_songs["artist_name"].str.contains(artist_name, case=False, na=False)
            ]
        
        # Track name filter
        if track_name:
            filtered_songs = filtered_songs[
                filtered_songs["track_name"].str.contains(track_name, case=False, na=False)
            ]
        
        # Year range filter
        filtered_songs = filtered_songs[
            (filtered_songs["year"] >= year_range[0]) & 
            (filtered_songs["year"] <= year_range[1])
        ]
        
        # Genre filter
        if selected_genres:
            filtered_songs = filtered_songs[filtered_songs["genre"].isin(selected_genres)]
        
        # Display results
        st.markdown("---")
        st.header("📊 Search Results")
        
        if filtered_songs.empty:
            st.error("No songs found matching your criteria. Try adjusting your filters.")
        else:
            # Results summary
            st.success(f"Found **{len(filtered_songs)}** song(s) matching your criteria")
            
            # Quick statistics for filtered results
            if len(filtered_songs) > 0:
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Artists in Results", filtered_songs['artist_name'].nunique())
                with col2:
                    st.metric("Years Covered", f"{filtered_songs['year'].min()}-{filtered_songs['year'].max()}")
                with col3:
                    st.metric("Genres in Results", filtered_songs['genre'].nunique())
            
            # Display the filtered data
            st.dataframe(
                filtered_songs,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "id": st.column_config.NumberColumn("ID", width="small"),
                    "artist_name": "Artist",
                    "track_name": "Track Name", 
                    "track_id": "Track ID",
                    "year": "Year",
                    "genre": "Genre"
                }
            )
            
            # Download option for filtered results
            csv = filtered_songs.to_csv(index=False)
            st.download_button(
                label="📥 Download Filtered Results as CSV",
                data=csv,
                file_name="filtered_spotify_songs.csv",
                mime="text/csv",
                type="primary"
            )
    
    # Display sample of data when no search is performed
    else:
        st.markdown("---")
        st.header("All Songs Preview")
        st.info("Use the filters above to search for specific songs, then click 'Search Songs'")
        
        # Show a preview of the data
        st.dataframe(
            songs_df.head(10),
            use_container_width=True,
            hide_index=True,
            column_config={
                "id": st.column_config.NumberColumn("ID", width="small"),
                "artist_name": "Artist",
                "track_name": "Track Name",
                "track_id": "Track ID", 
                "year": "Year",
                "genre": "Genre"
            }
        )
        
        if len(songs_df) > 10:
            st.caption(f"Showing 10 of {len(songs_df)} total songs. Use search to see more.")

if __name__ == "__main__":
    main()

