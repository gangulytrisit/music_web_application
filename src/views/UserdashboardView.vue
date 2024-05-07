<template>
  <div class="user-dashboard">
    <h1>User Dashboard</h1>
    <nav class="navbar">
      <div class="navbar-left">
        <h1>User Dashboard</h1>
      </div>
      <div class="navbar-right">
        <button class="logout-button" @click="logout">Logout</button>
      </div>
    </nav>
    <div class="container">
      <!-- First Row -->
      <div class="row">
        <!-- Song Details -->
        <div class="box">
          <h3>Song Details</h3>
          <input
            type="text"
            v-model="searchText"
            placeholder="Search Song Details"
          />
          <div class="song-details-container">
            <div class="song-box" v-for="song in filteredSongs" :key="song.id">
              <div class="song-info">
                <p>Title: {{ song.title }}</p>
                <p>Genre: {{ song.genre }}</p>
                <p>Singer: {{ song.singer }}</p>
                <p>Rating: {{ Math.round(song.rating * 100) / 100 }}</p>
                <button @click="viewLyrics(song.id)" class="lyrics-button">
                  View Lyrics
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- Recommended Songs -->
        <div class="box">
          <h3>Recommended Songs</h3>
          <ul>
            <li v-for="song in recommendedSongs" :key="song.id">
              <div class="song-box">
                <span>{{ song.title }}</span>
                <button @click="viewLyrics(song.id)" class="lyrics-button">
                  View Lyrics
                </button>
              </div>
            </li>
          </ul>
        </div>

        <!-- Playlists -->
        <div class="box">
          <h3>Playlists</h3>
          <input
            type="text"
            v-model="playlistSearch"
            placeholder="Search Playlists"
          />
          <button
            @click="createPlaylist(user_id)"
            class="create-playlist-button"
          >
            Create Playlist
          </button>
          <ul>
            <li v-for="playlist in filteredPlaylists" :key="playlist.id">
              <div class="playlist-box">
                <span>{{ playlist.title }}</span>
                <ul>
                  <li v-for="song in playlist.songs" :key="song.id">
                    <div class="song-info">
                      <span>{{ song.title }} - {{ song.genre }}</span>
                    </div>
                  </li>
                  <button
                    @click="deletePlaylist(playlist.id)"
                    class="delete-button"
                  >
                    Delete
                  </button>
                </ul>
              </div>
            </li>
          </ul>
        </div>
      </div>
      <!-- End of First Row -->

      <!-- Second Row -->
      <div class="row">
        <!-- Album Details -->
        <div class="box">
          <h3>Album Details</h3>
          <ul>
            <li v-for="album in albums" :key="album.id">
              {{ album.title }}
            </li>
          </ul>
        </div>
      </div>
    </div>
    <!-- End of .container -->
  </div>
</template>

<script>
export default {
  data() {
    return {
      recommendedSongs: [],
      playlists: [],
      songs: [],
      albums: [],
      songSearch: "",
      playlistSearch: "",
      user_id: null,
      rating: null,
      searchText: "",
    };
  },
  created() {
    this.user_id = sessionStorage.getItem("user_id");
    this.fetchRecommendedSongs();
    this.fetchPlaylists();
    this.fetchSongs();
    this.fetchAlbums();
  },
  methods: {
    fetchRecommendedSongs() {
      fetch("http://127.0.0.1:5000/api/song")
        .then((response) => response.json())
        .then((data) => {
          this.recommendedSongs = data;
        })
        .catch((error) =>
          console.error("Error fetching recommended songs:", error)
        );
    },
    fetchPlaylists() {
      let url = `http://127.0.0.1:5000/api/playlist/user/${this.user_id}`;

      fetch(url)
        .then((response) => response.json())
        .then((data) => {
          this.playlists = data.playlists;
          console.log(this.playlists);
          console.log(data);
          console.log(data.playlists);
        })
        .catch((error) => console.error("Error fetching playlists:", error));
    },

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
    viewLyrics(songId) {
      this.$router.push({ name: "userviewsong", params: { song_id: songId } });
    },
    deletePlaylist(playlistId) {
      // Prompt the user with a confirmation dialog
      const confirmDelete = window.confirm(
        "Are you sure you want to delete this playlist?"
      );

      if (confirmDelete) {
        const url = `http://127.0.0.1:5000/api/playlist/${playlistId}`;
        fetch(url, {
          method: "DELETE",
          headers: {
            "Content-Type": "application/json",
          },
        })
          .then((response) => {
            if (response.ok) {
              // Remove the deleted playlist from the local state
              this.playlists = this.playlists.filter(
                (playlist) => playlist.id !== playlistId
              );
              this.$router.push("/userdashboard");
            } else {
              throw new Error("Failed to delete playlist");
            }
          })
          .catch((error) => console.error("Error deleting playlist:", error));
      }
    },

    createPlaylist(user_id) {
      this.$router.push({ name: "userplaylist", params: { user_id: user_id } });
    },
    logout() {
      sessionStorage.removeItem("auth-token");
      sessionStorage.removeItem("email");
      sessionStorage.removeItem("user_id");
      localStorage.removeItem("auth-token");
      localStorage.removeItem("email");
      localStorage.removeItem("user_id");
      this.$router.push("/userlogin");
    },
  },
  computed: {
    filteredPlaylists() {
      return this.playlists.filter((playlist) =>
        playlist.title.toLowerCase().includes(this.playlistSearch.toLowerCase())
      );
    },
    filteredSongs() {
      return this.songs.filter((song) => {
        const searchText = this.searchText.toLowerCase();
        return (
          !searchText ||
          song.title.toLowerCase().includes(searchText) ||
          song.genre.toLowerCase().includes(searchText) ||
          song.singer.toLowerCase().includes(searchText) ||
          (song.rating !== null && song.rating.toString().includes(searchText))
        );
      });
    },
  },
};
</script>

<style scoped>
.container {
  display: flex;
  flex-direction: column;
}

.row {
  display: flex;
  flex-wrap: wrap;
}

.box {
  flex: 1 1 45%;
  border: 1px solid #ccc;
  padding: 20px;
  margin: 0 10px 20px 0;
  background-color: #f9f9f9;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.song-box,
.playlist-box,
.song-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.lyrics-button,
.create-playlist-button {
  background-color: #007bff;
  color: #fff;
  border: none;
  padding: 10px 20px;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s;
}
.delete-button {
  background-color: #ea250b;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.delete-button:hover {
  background-color: #b30000;
}

.lyrics-button:hover,
.delete-button:hover,
.create-playlist-button:hover {
  background-color: #0056b3;
}

input[type="text"] {
  padding: 10px;
  border-radius: 5px;
  border: 1px solid #ccc;
  margin-bottom: 10px;
}

h3 {
  margin-bottom: 15px;
}

.navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: #333;
  padding: 10px 20px;
}

.navbar-left h1 {
  color: white;
  margin: 0;
}

.logout-button {
  background-color: #ea250b;
  color: white;
  border: none;
  padding: 8px 16px;
  margin-left: 10px;
  cursor: pointer;
}
.song-details-container {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  grid-gap: 20px;
}

.song-box {
  border: 1px solid #ccc;
  padding: 15px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.song-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.song-details-container {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  grid-gap: 20px;
}

.song-box {
  border: 1px solid #ccc;
  padding: 15px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.song-info {
  display: flex;
  flex-direction: column;
}

.song-info span {
  margin-bottom: 5px;
}

.song-info .rating {
  margin-top: 10px;
}
</style>
