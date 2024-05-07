<template>
  <div class="form-container">
    <form @submit.prevent="submitForm" class="form-box">
      <h2>Update Song Details</h2>
      <label for="title">Title:</label>
      <input type="text" id="title" v-model="formData.title" required />
      <br />
      <label for="genre">Genre:</label>
      <input type="text" id="genre" v-model="formData.genre" required />
      <br />
      <label for="lyrics">Lyrics:</label>
      <textarea id="lyrics" v-model="formData.lyrics" required></textarea>
      <br />
      <label for="singer">Singer:</label>
      <input type="text" id="singer" v-model="formData.singer" required />
      <br />
      <label for="date">Date:</label>
      <input type="date" id="date" v-model="formData.date" required />
      <br />
      <div>
        <label for="album">Select Album:</label>
        <select id="album" v-model="formData.album_id">
          <option value="" disabled>Select Album</option>
          <option v-for="album in albums" :key="album.id" :value="album.id">
            {{ album.title }}
          </option>
        </select>
      </div>
      <button type="submit">Update Song</button>
    </form>
  </div>
</template>

<script>
export default {
  data() {
    return {
      id: this.$route.params.songId,
      user_id: sessionStorage.getItem("user_id"),
      formData: {
        title: "",
        genre: "",
        lyrics: "",
        singer: "",
        album_id: null,
      },
      albums: [],
    };
  },
  methods: {
    async fetchSongData() {
      try {
        const response = await fetch(
          `http://127.0.0.1:5000/api/song/${this.id}`
        );
        if (response.ok) {
          const songData = await response.json();
          this.formData = songData;
          this.formData.album_id = songData.album_id;
          await this.fetchAlbums();
        } else {
          console.error("Failed to fetch song data");
        }
      } catch (error) {
        console.error("Error fetching song data:", error);
      }
    },
    async fetchAlbums() {
      try {
        const response = await fetch("http://127.0.0.1:5000/api/album");
        if (response.ok) {
          const data = await response.json();
          // Filter albums based on the current user's ID
          this.albums = data.filter((album) => album.user_id == this.user_id);
        } else {
          console.error("Failed to fetch albums");
        }
      } catch (error) {
        console.error("Error fetching albums:", error);
      }
    },
    async submitForm() {
      try {
        const response = await fetch(
          `http://127.0.0.1:5000/api/song/${this.id}/${this.user_id}`,
          {
            method: "PUT",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify(this.formData),
          }
        );
        if (response.ok) {
          console.log("Song updated successfully");
          this.$router.go(-1);
        } else {
          console.error("Failed to update song");
        }
      } catch (error) {
        console.error("Error updating song:", error);
      }
    },
  },
  mounted() {
    this.fetchSongData();
  },
};
</script>

<style scoped>
.form-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
}

.form-box {
  width: 400px;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 8px;
  background-color: #f9f9f9;
}

label {
  margin-bottom: 5px;
}

input,
textarea,
select,
button {
  width: 100%;
  margin-bottom: 10px;
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

button {
  background-color: #007bff;
  color: #fff;
  cursor: pointer;
}

button:hover {
  background-color: #0056b3;
}
</style>
