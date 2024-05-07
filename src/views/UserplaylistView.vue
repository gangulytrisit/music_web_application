<template>
  <div class="create-playlist-container">
    <div class="playlist-box">
      <h2>Create Playlist</h2>
      <form @submit.prevent="createPlaylist">
        <div class="form-group">
          <label for="playlistName">Playlist Name:</label>
          <input
            type="text"
            id="playlistName"
            v-model="playlistName"
            class="form-control"
          />
        </div>
        <div class="form-group">
          <h3>Select Songs:</h3>
          <ul class="song-list">
            <li v-for="song in songs" :key="song.id">
              <label>
                <input
                  type="checkbox"
                  v-model="selectedSongs"
                  :value="song.id"
                />
                {{ song.title }}
              </label>
            </li>
          </ul>
        </div>
        <button type="submit" class="btn btn-primary">Create Playlist</button>
      </form>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      playlistName: "",
      selectedSongs: [],
      songs: [],
      user_id: sessionStorage.getItem("user_id"),
    };
  },
  methods: {
    async fetchSongs() {
      try {
        const response = await fetch("http://127.0.0.1:5000/api/song");
        const data = await response.json();
        this.songs = data;
      } catch (error) {
        console.error("Error fetching songs:", error);
      }
    },
    async createPlaylist() {
      try {
        const response = await fetch(
          `http://127.0.0.1:5000/api/playlist/user/${this.user_id}`,
          {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify({
              title: this.playlistName,
              song_ids: this.selectedSongs,
              user_id: this.user_id,
            }),
          }
        );
        const data = await response.json();
        console.log("Playlist created:", data);
        // Reset form fields
        this.playlistName = "";
        this.selectedSongs = [];
        // Navigate back to user dashboard
        this.$router.push({ name: "userdashboard" });
      } catch (error) {
        console.error("Error creating playlist:", error);
      }
    },
  },
  mounted() {
    // Fetch songs when the component is mounted
    this.fetchSongs();
  },
};
</script>

<style scoped>
.create-playlist-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%;
}

.playlist-box {
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
  padding: 30px;
}

.form-group {
  margin-bottom: 20px;
}

.song-list {
  list-style: none;
  padding-left: 0;
}

.btn-primary {
  background-color: #007bff;
  color: #fff;
  border: none;
  padding: 10px 20px;
  cursor: pointer;
  border-radius: 5px;
}

.btn-primary:hover {
  background-color: #0056b3;
}
</style>
