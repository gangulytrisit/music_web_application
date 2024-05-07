<template>
  <div class="song-container">
    <!-- Album Details -->
    <div class="box album-box">
      <h3>Album Details</h3>
      <input
        type="text"
        v-model="albumSearchText"
        placeholder="Search Album Details"
      />
      <ul>
        <li v-for="album in filteredAlbums" :key="album.id">
          {{ album.title }}
        </li>
      </ul>
    </div>
    <h3>Song Details</h3>
    <input
      type="text"
      v-model="songSearchText"
      placeholder="Search Song Details"
    />
    <div class="song-details-container">
      <div class="song-box" v-for="song in filteredSongs" :key="song.id">
        <div class="song-info">
          <div class="song-title">{{ song.title }}</div>
          <div class="song-metadata">
            <p>Genre: {{ song.genre }}</p>
            <p>Singer: {{ song.singer }}</p>
            <p>Genre: {{ song.genre }}</p>
            <p>Rating: {{ Math.round(song.rating * 100) / 100 }}</p>
          </div>
          <div class="lyrics-section">
            <h4>Lyrics</h4>
            <pre>{{ song.lyrics }}</pre>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      songs: [],
      albums: [],
      songSearchText: "",
      albumSearchText: "",
      user_id: sessionStorage.getItem("user_id"),
    };
  },
  created() {
    this.user_id = sessionStorage.getItem("user_id");
    this.fetchSongs();
    this.fetchAlbums();
  },
  methods: {
    fetchSongs() {
      fetch("http://127.0.0.1:5000/api/song")
        .then((response) => response.json())
        .then((data) => {
          this.songs = data;
        })
        .catch((error) => console.error("Error fetching songs:", error));
    },
    fetchAlbums() {
      fetch("http://127.0.0.1:5000/api/album")
        .then((response) => response.json())
        .then((data) => {
          this.albums = data;
        })
        .catch((error) => console.error("Error fetching albums:", error));
    },
  },
  computed: {
    filteredSongs() {
      return this.songs.filter((song) => {
        const searchText = this.songSearchText.toLowerCase();
        return (
          !searchText ||
          song.title.toLowerCase().includes(searchText) ||
          song.genre.toLowerCase().includes(searchText) ||
          song.singer.toLowerCase().includes(searchText) ||
          (song.rating !== null && song.rating.toString().includes(searchText))
        );
      });
    },
    filteredAlbums() {
      return this.albums.filter((album) => {
        const searchText = this.albumSearchText.toLowerCase();
        return !searchText || album.title.toLowerCase().includes(searchText);
      });
    },
  },
};
</script>

<style scoped>
.song-container {
  margin: 20px;
}

.album-box {
  width: 45%;
  margin-right: auto;
  margin-left: auto;
  padding: 15px;
  border: 1px solid #ccc;
  border-radius: 5px;
  background-color: #f9f9f9;
}

.song-details-container {
  display: flex;
  flex-wrap: wrap;
}

.song-box {
  width: 45%;
  margin: 10px;
  padding: 15px;
  border: 1px solid #ccc;
  border-radius: 5px;
  background-color: #f9f9f9;
}

.song-info {
  display: flex;
  flex-direction: column;
}

.song-title {
  font-size: 18px;
  font-weight: bold;
  margin-bottom: 10px;
}

.song-metadata {
  margin-bottom: 10px;
}

.lyrics-section {
  margin-bottom: 10px;
}

.rate-section {
  display: flex;
  align-items: center;
}
</style>
