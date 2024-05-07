<template>
  <div class="user-profile">
    <h1>User Profile</h1>
    <div v-if="selectedSong">
      <h2>{{ selectedSong.title }}</h2>
      <p>{{ selectedSong.artist }}</p>
      <pre>{{ selectedSong.lyrics }}</pre>
      <div>
        <label>Rating:</label>
        <select v-model="rating">
          <option v-for="n in 5" :key="n" :value="n">{{ n }}</option>
        </select>
        <button @click="rateSong">Rate</button>
      </div>
    </div>
    <div v-else>
      <p>No song selected</p>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      selectedSong: null,
      rating: 1,
    };
  },
  methods: {
    rateSong() {
      console.log(
        `Rated song ${this.selectedSong.title} with rating ${this.rating}`
      );
    },
  },
};
</script>

<style scoped></style>
