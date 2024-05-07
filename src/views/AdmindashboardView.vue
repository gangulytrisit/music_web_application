<template>
  <div class="admin-dashboard">
    <h1>Admin Dashboard</h1>
    <nav class="navbar">
      <div class="navbar-left">
        <h1>Admin Dashboard</h1>
      </div>
      <div class="navbar-right">
        <button class="export-button" @click="exportCSV">Export CSV</button>
        <button class="logout-button" @click="logout">Logout</button>
      </div>
    </nav>
    <!-- Statistics Section -->
    <div class="statistics">
      <div class="statistic">
        <h2>Total Users</h2>
        <p>{{ totalUsers }}</p>
      </div>
      <div class="statistic">
        <h2>Total Creators</h2>
        <p>{{ totalCreators }}</p>
      </div>
      <div class="statistic">
        <h2>Total Albums</h2>
        <p>{{ totalAlbums }}</p>
      </div>
    </div>

    <!-- Album Table -->
    <h2>Albums</h2>
    <table>
      <thead>
        <tr>
          <th>ID</th>
          <th>Title</th>
          <th>User ID</th>
          <th>Action</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="album in albums" :key="album.id">
          <td>{{ album.id }}</td>
          <td>{{ album.title }}</td>
          <td>{{ album.user_id }}</td>
          <td>
            <button class="delete-button" @click="confirmDeleteAlbum(album.id)">
              Delete
            </button>
          </td>
        </tr>
      </tbody>
    </table>

    <!-- Song Table -->
    <h2>Songs</h2>
    <table>
      <thead>
        <tr>
          <th>ID</th>
          <th>Title</th>
          <th>Genre</th>
          <th>User ID</th>
          <th>Action</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="song in songs" :key="song.id">
          <td>{{ song.id }}</td>
          <td>{{ song.title }}</td>
          <td>{{ song.genre }}</td>
          <td>{{ song.user_id }}</td>
          <td>
            <button class="delete-button" @click="confirmDeleteSong(song.id)">
              Delete
            </button>
          </td>
        </tr>
      </tbody>
    </table>

    <!-- Graphs Section -->
    <h2>Graphs</h2>
    <div class="graphs">
      <div class="graph-box">
        <canvas id="songsByCreatorChart" width="400" height="200"></canvas>
      </div>
      <div class="graph-box">
        <canvas id="albumsByCreatorChart" width="400" height="200"></canvas>
      </div>
    </div>
  </div>
</template>

<script>
import Chart from "chart.js/auto"; // Import Chart.js

function getHeaders() {
  const headers = {
    "Content-Type": "application/json",
  };

  const auth_token = sessionStorage.getItem("auth-token");
  if (auth_token) {
    headers["Authentication-Token"] = `${auth_token}`;
  }

  return headers;
}

export default {
  data() {
    return {
      totalUsers: 0,
      totalCreators: 0,
      totalAlbums: 0,
      albums: [],
      songs: [],
      email: null,
    };
  },
  created() {
    this.fetchStatistics();
    this.fetchAlbums();
    this.fetchSongs();
    this.fetchSongsByCreator();
    this.fetchAlbumsByCreator(); // Fetch albums by creator
  },
  methods: {
    fetchStatistics() {
      // Fetch total users
      fetch("http://127.0.0.1:5000/api/user", { headers: getHeaders() })
        .then((response) => {
          if (!response.ok) {
            throw new Error("Network response was not ok");
          }
          return response.json();
        })
        .then((data) => {
          this.totalUsers = data.length - 1;
        })
        .catch((error) => {
          console.error("Error fetching total users:", error);
        });

      // Fetch total creators
      fetch("http://127.0.0.1:5000/api/user", { headers: getHeaders() })
        .then((response) => {
          if (!response.ok) {
            throw new Error("Network response was not ok");
          }
          return response.json();
        })
        .then((data) => {
          this.totalCreators = data.filter((user) => {
            return user.roles.some((role) => role.name === "creator");
          }).length;
        })
        .catch((error) => {
          console.error("Error fetching total creators:", error);
        });

      // Fetch total albums
      fetch("http://127.0.0.1:5000/api/album")
        .then((response) => {
          if (!response.ok) {
            throw new Error("Network response was not ok");
          }
          return response.json();
        })
        .then((data) => {
          this.totalAlbums = data.length;
        })
        .catch((error) => {
          console.error("Error fetching total albums:", error);
        });
    },
    fetchAlbums() {
      fetch("http://127.0.0.1:5000/api/album")
        .then((response) => {
          if (!response.ok) {
            throw new Error("Network response was not ok");
          }
          return response.json();
        })
        .then((data) => {
          this.albums = data;
        })
        .catch((error) => {
          console.error("Error fetching albums:", error);
        });
    },
    fetchSongs() {
      fetch("http://127.0.0.1:5000/api/song")
        .then((response) => {
          if (!response.ok) {
            throw new Error("Network response was not ok");
          }
          return response.json();
        })
        .then((data) => {
          this.songs = data;
        })
        .catch((error) => {
          console.error("Error fetching songs:", error);
        });
    },
    confirmDeleteAlbum(albumId) {
      if (confirm("Are you sure you want to delete this album?")) {
        this.deleteAlbum(albumId);
      }
    },
    confirmDeleteSong(songId) {
      if (confirm("Are you sure you want to delete this song?")) {
        this.deleteSong(songId);
      }
    },
    deleteAlbum(albumId) {
      fetch(`http://127.0.0.1:5000/api/album/${albumId}`, {
        method: "DELETE",
        headers: getHeaders(),
      })
        .then((response) => {
          if (!response.ok) {
            throw new Error("Network response was not ok");
          }
          // Refresh albums after deletion
          this.fetchAlbums();
          // Delete associated songs
          this.deleteAssociatedSongs(albumId);
          // Fetch updated data for the graphs
          this.fetchSongsByCreator();
          this.fetchAlbumsByCreator();
        })
        .catch((error) => {
          console.error("Error deleting album:", error);
        });
    },
    deleteAssociatedSongs(albumId) {
      // Filter out songs associated with the deleted album
      this.songs = this.songs.filter((song) => song.album_id !== albumId);
    },
    deleteSong(songId) {
      fetch(`http://127.0.0.1:5000/api/song/${songId}`, {
        method: "DELETE",
        headers: getHeaders(),
      })
        .then((response) => {
          if (!response.ok) {
            throw new Error("Network response was not ok");
          }
          // Refresh songs after deletion
          this.fetchSongs();
          // Fetch updated data for the graphs
          this.fetchSongsByCreator();
          this.fetchAlbumsByCreator();
        })
        .catch((error) => {
          console.error("Error deleting song:", error);
        });
    },
    exportCSV() {
      this.email = "admin@admin.com";
      fetch(`http://127.0.0.1:5000/api/export/${this.email}`, {
        method: "GET",
        headers: getHeaders(),
      })
        .then((response) => {
          if (!response.ok) {
            throw new Error("Network response was not ok");
          }
          alert("mail sent");
        })
        .catch((error) => {
          console.error("Error logging out:", error);
        });
    },
    logout() {
      // Clear session data
      sessionStorage.removeItem("auth-token");
      sessionStorage.removeItem("email");
      sessionStorage.removeItem("user_id");
      localStorage.removeItem("auth-token");
      localStorage.removeItem("email");
      localStorage.removeItem("user_id");
      this.$router.push("/adminlogin");
    },
    fetchSongsByCreator() {
      // Fetch data for songs by creator graph
      fetch("http://127.0.0.1:5000/api/song")
        .then((response) => {
          if (!response.ok) {
            throw new Error("Network response was not ok");
          }
          return response.json();
        })
        .then((data) => {
          // Group songs by creator ID
          const songsByCreator = data.reduce((acc, song) => {
            if (!acc[song.user_id]) {
              acc[song.user_id] = [];
            }
            acc[song.user_id].push(song);
            return acc;
          }, {});

          // Prepare data for the chart
          const creatorLabels = Object.keys(songsByCreator);
          const creatorSongCounts = creatorLabels.map(
            (creatorId) => songsByCreator[creatorId].length
          );

          // Render the chart
          const songsByCreatorChartCtx = document
            .getElementById("songsByCreatorChart")
            .getContext("2d");
          new Chart(songsByCreatorChartCtx, {
            type: "bar",
            data: {
              labels: creatorLabels,
              datasets: [
                {
                  label: "Songs Created",
                  data: creatorSongCounts,
                  backgroundColor: "rgba(255, 99, 132, 0.2)",
                  borderColor: "rgba(255, 99, 132, 1)",
                  borderWidth: 1,
                },
              ],
            },
            options: {
              plugins: {
                title: {
                  display: true,
                  text: "Number of Songs Created by Individual Users", // Heading inside the graph
                  padding: {
                    top: 10,
                    bottom: 10,
                  },
                },
              },
              scales: {
                x: {
                  title: {
                    display: true,
                    text: "Creator ID", // X-axis label
                  },
                },
                y: {
                  title: {
                    display: true,
                    text: "No of Songs", // Y-axis label
                  },
                },
              },
            },
          });
        })
        .catch((error) => {
          console.error("Error fetching songs by creator:", error);
        });
    },
    fetchAlbumsByCreator() {
      // Fetch data for albums by creator graph
      fetch("http://127.0.0.1:5000/api/album")
        .then((response) => {
          if (!response.ok) {
            throw new Error("Network response was not ok");
          }
          return response.json();
        })
        .then((data) => {
          // Group albums by creator ID
          const albumsByCreator = data.reduce((acc, album) => {
            if (!acc[album.user_id]) {
              acc[album.user_id] = [];
            }
            acc[album.user_id].push(album);
            return acc;
          }, {});

          // Prepare data for the chart
          const creatorLabels = Object.keys(albumsByCreator);
          const creatorAlbumCounts = creatorLabels.map(
            (creatorId) => albumsByCreator[creatorId].length
          );

          // Render the chart
          // Render the chart
          const albumsByCreatorChartCtx = document
            .getElementById("albumsByCreatorChart")
            .getContext("2d");
          new Chart(albumsByCreatorChartCtx, {
            type: "bar",
            data: {
              labels: creatorLabels,
              datasets: [
                {
                  label: "Albums Created",
                  data: creatorAlbumCounts,
                  backgroundColor: "rgba(54, 162, 235, 0.2)",
                  borderColor: "rgba(54, 162, 235, 1)",
                  borderWidth: 1,
                },
              ],
            },
            options: {
              plugins: {
                title: {
                  display: true,
                  text: "Number of Albums Created by Individual Users", // Heading inside the graph
                  padding: {
                    top: 10,
                    bottom: 10,
                  },
                },
              },
              scales: {
                x: {
                  title: {
                    display: true,
                    text: "Creator ID", // X-axis label
                  },
                },
                y: {
                  title: {
                    display: true,
                    text: "No of Albums", // Y-axis label
                  },
                },
              },
            },
          });
        })
        .catch((error) => {
          console.error("Error fetching albums by creator:", error);
        });
    },
  },
};
</script>

<style scoped>
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

.navbar-right {
  display: flex;
}

.export-button,
.logout-button {
  background-color: #2e9007;
  color: white;
  border: none;
  padding: 8px 16px;
  margin-left: 10px;
  cursor: pointer;
}

.logout-button {
  background-color: #f44336;
}

.statistics {
  display: flex;
  justify-content: space-around;
}

.statistic {
  text-align: center;
}

table {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 20px;
}

table th,
table td {
  border: 1px solid #ddd;
  padding: 8px;
  text-align: left;
}

table th {
  background-color: #f2f2f2;
}

.delete-button {
  background-color: red;
  color: white;
  border: none;
  padding: 5px 10px;
  cursor: pointer;
}

.graphs {
  margin-top: 20px;
  display: flex;
  justify-content: space-around;
}

.graph-box {
  border: 1px solid #ddd;
  border-radius: 5px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.graph-box canvas {
  width: 100%;
  height: 100%;
}
</style>
