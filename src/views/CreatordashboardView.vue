<template>
  <div class="creator-dashboard">
    <h1>Creator Dashboard</h1>
    <nav class="navbar">
      <div class="navbar-left">
        <h1>Creator Dashboard</h1>
      </div>
      <div class="navbar-right">
        <button class="song-details-button" @click="goToSongDetails">
          Song Details
        </button>
        <button class="logout-button" @click="logout">Logout</button>
      </div>
    </nav>

    <!-- Form to add new album -->
    <div class="form-container">
      <form @submit.prevent="addAlbum" class="form">
        <h3>Add Album</h3>
        <div>
          <label for="albumTitle">Title:</label>
          <input type="text" id="albumTitle" v-model="newAlbum.title" />
        </div>
        <div>
          <label for="creator">Creator Name:</label>
          <input type="text" id="creator" v-model="newAlbum.artist" />
        </div>
        <button type="submit">Add Album</button>
      </form>
    </div>

    <!-- Form to add new song -->
    <div class="form-container">
      <form @submit.prevent="addSong" class="form">
        <h3>Add Song</h3>
        <div>
          <label for="songTitle">Title:</label>
          <input type="text" id="songTitle" v-model="newSong.title" />
        </div>
        <div>
          <label for="genre">Genre:</label>
          <input type="text" id="genre" v-model="newSong.genre" />
        </div>
        <div>
          <label for="lyrics">Lyrics:</label>
          <textarea id="lyrics" v-model="newSong.lyrics"></textarea>
        </div>
        <div>
          <label for="singer">Singer:</label>
          <input type="text" id="singer" v-model="newSong.singer" />
        </div>
        <div>
          <label for="date">Date:</label>
          <input type="date" id="date" v-model="newSong.date" />
        </div>
        <div>
          <label for="album">Select Album:</label>
          <select id="album" v-model="newSong.album_id">
            <option v-for="album in albums" :key="album.id" :value="album.id">
              {{ album.title }}
            </option>
          </select>
        </div>
        <button type="submit">Add Song</button>
      </form>
    </div>

    <!-- Display added albums -->
    <div class="data-container">
      <h3>Albums</h3>
      <table class="data-table">
        <thead>
          <tr>
            <th>Title</th>
            <th>Creator Name</th>
            <th>Action</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="album in albums" :key="album.id">
            <td>{{ album.title }}</td>
            <td>{{ album.artist }}</td>
            <td>
              <button @click="deleteAlbum(album.id)">Delete</button>
              <button @click="updateAlbum(album)">Update</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Display added songs -->
    <div class="data-container">
      <h3>Songs</h3>
      <table class="data-table">
        <thead>
          <tr>
            <th>Title</th>
            <th>Genre</th>
            <th>Singer</th>
            <th>Date</th>
            <th>Lyrics</th>
            <th>Action</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="song in songs" :key="song.id">
            <td>{{ song.title }}</td>
            <td>{{ song.genre }}</td>
            <td>{{ song.singer }}</td>
            <td>{{ song.date }}</td>
            <td>{{ song.lyrics }}</td>
            <td>
              <button @click="deleteSong(song.id)">Delete</button>
              <button @click="updateSong(song)">Update</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      user_id: null,
      albums: [],
      songs: [],
      newAlbum: { title: "", artist: "", flag: false, user_id: null },
      newSong: {
        title: "",
        genre: "",
        lyrics: "",
        singer: "",
        date: "",
        user_id: null,
        album_id: "",
        flag: false,
      },
    };
  },
  created() {
    this.user_id = sessionStorage.getItem("user_id");
    console.log(this.user_id);
  },
  methods: {
    async addAlbum() {
      try {
        const response = await fetch("http://127.0.0.1:5000/api/album", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            title: this.newAlbum.title,
            artist: this.newAlbum.artist,
            flag: this.newAlbum.flag,
            user_id: this.user_id,
          }),
        });
        const data = await response.json();
        console.log("Album added:", data);
        this.fetchAlbums();
        this.albums.push(data);
        this.newAlbum = { title: "", artist: "" };
      } catch (error) {
        console.error("Error adding album:", error);
      }
    },
    async addSong() {
      try {
        const response = await fetch("http://127.0.0.1:5000/api/song", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            title: this.newSong.title,
            genre: this.newSong.genre,
            lyrics: this.newSong.lyrics,
            singer: this.newSong.singer,
            date: this.newSong.date,
            user_id: this.user_id,
            album_id: this.newSong.album_id,
            flag: this.newSong.flag,
          }),
        });
        const data = await response.json();
        console.log("Song added:", data);
        this.fetchSongs();
        // Clear the newSong object to reset form fields
        this.newSong = {
          title: "",
          genre: "",
          lyrics: "",
          singer: "",
          date: "",
          user_id: null,
          album_id: "",
          flag: false,
        };
      } catch (error) {
        console.error("Error adding song:", error);
      }
    },

    async deleteAlbum(albumId) {
      try {
        const confirmed = confirm(
          "Are you sure you want to delete this album?"
        );
        if (confirmed) {
          const response = await fetch(
            `http://127.0.0.1:5000/api/album/${albumId}`,
            {
              method: "DELETE",
              headers: {
                "Content-Type": "application/json",
              },
            }
          );
          if (response.ok) {
            this.albums = this.albums.filter((album) => album.id !== albumId);
          } else {
            console.error("Failed to delete album");
          }
        }
      } catch (error) {
        console.error("Error deleting album:", error);
      }
    },
    async deleteSong(songId) {
      try {
        const confirmed = confirm("Are you sure you want to delete this song?");
        if (confirmed) {
          const response = await fetch(
            `http://127.0.0.1:5000/api/song/${songId}`,
            {
              method: "DELETE",
              headers: {
                "Content-Type": "application/json",
              },
            }
          );
          if (response.ok) {
            this.songs = this.songs.filter((song) => song.id !== songId);
          } else {
            console.error("Failed to delete song");
          }
        }
      } catch (error) {
        console.error("Error deleting song:", error);
      }
    },
    updateAlbum(album) {
      this.$router.push({ name: "updatealbum", params: { albumId: album.id } });
    },

    updateSong(song) {
      this.$router.push({ name: "updatesong", params: { songId: song.id } });
    },

    async fetchAlbums() {
      try {
        const response = await fetch("http://127.0.0.1:5000/api/album");
        const data = await response.json();
        this.albums = data.filter((album) => album.user_id == this.user_id);
      } catch (error) {
        console.error("Error fetching albums:", error);
      }
    },
    async fetchSongs() {
      try {
        const response = await fetch("http://127.0.0.1:5000/api/song");
        const data = await response.json();
        this.songs = data.filter((song) => song.user_id == this.user_id);
      } catch (error) {
        console.error("Error fetching songs:", error);
      }
    },

    logout() {
      // Clear session data
      sessionStorage.removeItem("auth-token");
      sessionStorage.removeItem("email");
      sessionStorage.removeItem("user_id");
      localStorage.removeItem("auth-token");
      localStorage.removeItem("email");
      localStorage.removeItem("user_id");
      this.$router.push("/creatorlogin");
    },
    goToSongDetails() {
      this.$router.push("/creatorviewsong");
    },
  },
  mounted() {
    this.fetchAlbums();
    this.fetchSongs();
    this.user_id = sessionStorage.getItem("user_id");
  },
};
</script>

<style scoped>
.form-container {
  width: 45%;
  float: left;
  margin-right: 5%;
}

.data-container {
  width: 45%;
  float: left;
  margin-bottom: 20px;
}

.form {
  background-color: #f0f0f0;
  padding: 20px;
  border-radius: 5px;
}

.data-table {
  width: 100%;
  border-collapse: collapse;
}

.data-table th,
.data-table td {
  border: 1px solid #ddd;
  padding: 8px;
  text-align: left;
}

.data-table th {
  background-color: #f2f2f2;
}

.data-table td button {
  margin-right: 5px;
}

button {
  padding: 8px 12px;
  background-color: #007bff;
  color: #fff;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

button:hover {
  background-color: #0056b3;
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
  background-color: #f12f0d;
  color: white;
  border: none;
  padding: 8px 16px;
  margin-left: 10px;
  cursor: pointer;
}
input[type="text"],
input[type="date"],
textarea,
select {
  width: 100%;
  padding: 8px;
  margin: 6px 0;
  display: inline-block;
  border: 1px solid #ccc;
  border-radius: 4px;
  box-sizing: border-box;
}
</style>
