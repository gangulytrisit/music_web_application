<template>
  <div class="album-form">
    <form @submit.prevent="submitForm" class="form">
      <label for="title" class="label">Title:</label>
      <input
        type="text"
        id="title"
        v-model="formData.title"
        class="input"
        required
      />
      <br />
      <label for="artist" class="label">Artist:</label>
      <input
        type="text"
        id="artist"
        v-model="formData.artist"
        class="input"
        required
      />
      <br />
      <button type="submit" class="btn">Update Album</button>
    </form>
  </div>
</template>

<script>
export default {
  data() {
    return {
      id: this.$route.params.albumId,
      formData: {
        title: "",
        artist: "",
      },
    };
  },
  methods: {
    async fetchAlbumData() {
      try {
        const response = await fetch(
          `http://127.0.0.1:5000/api/album/${this.id}`
        );
        if (response.ok) {
          const albumData = await response.json();
          this.formData = albumData;
        } else {
          console.error("Failed to fetch album data");
        }
      } catch (error) {
        console.error("Error fetching album data:", error);
      }
    },
    async submitForm() {
      try {
        const response = await fetch(
          `http://127.0.0.1:5000/api/album/${this.id}`,
          {
            method: "PUT",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify(this.formData),
          }
        );
        if (response.ok) {
          console.log("Album updated successfully");
          this.$router.go(-1);
        } else {
          console.error("Failed to update album");
        }
      } catch (error) {
        console.error("Error updating album:", error);
      }
    },
  },
  mounted() {
    this.fetchAlbumData();
  },
};
</script>

<style scoped>
.album-form {
  margin: 50px auto;
  max-width: 400px;
}

.form {
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 8px;
}

.label {
  font-weight: bold;
}

.input {
  width: 100%;
  padding: 10px;
  margin-bottom: 15px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

.btn {
  display: block;
  width: 100%;
  padding: 10px;
  background-color: #007bff;
  color: #fff;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.btn:hover {
  background-color: #0056b3;
}
</style>
