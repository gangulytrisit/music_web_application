<template>
  <div class="song-details-container">
    <h2 class="heading">Song Details</h2>
    <div v-if="song" class="song-details">
      <h3>Title: {{ song.title }}</h3>
      <p>Singer: {{ song.singer }}</p>
      <p>Release Date: {{ song.date }}</p>
      <p>Genre: {{ song.genre }}</p>
      <p>Rating: {{ Math.round(song.rating * 100) / 100 }}</p>
      <div class="lyrics-section">
        <h4>Lyrics</h4>
        <pre>{{ song.lyrics }}</pre>
      </div>
      <div class="rate-section">
        <h4>Rate This Song:</h4>
        <select v-model="userRating" class="rating-select">
          <option value="1">1</option>
          <option value="2">2</option>
          <option value="3">3</option>
          <option value="4">4</option>
          <option value="5">5</option>
        </select>
        <button @click="rateSong" class="rate-button">Rate</button>
      </div>
    </div>
    <div v-else>
      <p>Loading...</p>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      song: [],
      userRating: null,
      song_id: null,
      user_id: sessionStorage.getItem("user_id"),
      email: sessionStorage.getItem("email"),
    };
  },
  mounted() {
    this.fetchSongDetails();
  },
  methods: {
    fetchSongDetails() {
      this.song_id = this.$route.params.song_id;
      fetch(`http://127.0.0.1:5000/api/song/${this.song_id}`)
        .then((response) => {
          if (!response.ok) {
            throw new Error("Network response was not ok");
          }
          return response.json();
        })
        .then((data) => {
          this.song = data;
        })
        .catch((error) => {
          console.error("Error fetching song details:", error);
        });
    },
    rateSong() {
      this.song_id = this.song.id;
      fetch(`http://127.0.0.1:5000/api/rating/${this.song_id}`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          rating: this.userRating,
          user_id: this.user_id,
          song_id: this.song_id,
        }),
      })
        .then((response) => {
          if (!response.ok) {
            throw new Error("Network response was not ok");
          }
          return response.json();
        })
        .then((data) => {
          console.log(data);
          this.fetchSongDetails();
        })
        .catch((error) => {
          console.error("Error rating song:", error);
        });
    },
  },
};
</script>

<style scoped>
.song-details-container {
  max-width: 600px;
  margin: 0 auto;
  padding: 20px;
  background-color: #f7f7f7;
  border-radius: 8px;
}

.heading {
  font-size: 24px;
  margin-bottom: 20px;
}

.song-details {
  background-color: #fff;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.lyrics-section {
  margin-top: 20px;
}

.rate-section {
  margin-top: 20px;
}

.rating-select {
  padding: 8px;
  font-size: 16px;
}

.rate-button {
  padding: 8px 16px;
  font-size: 16px;
  background-color: #007bff;
  color: #fff;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.rate-button:hover {
  background-color: #0056b3;
}
</style>
