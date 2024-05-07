<template>
  <div class="login-container">
    <h2>Admin Login</h2>
    <p v-if="error" class="error">{{ error }}</p>
    <p v-if="error2" class="error">{{ error2 }}</p>
    <form @submit.prevent="login" class="login-form">
      <div>
        <label for="email">Email:</label>
        <input type="text" id="email" v-model="email" />
      </div>
      <div>
        <label for="password">Password:</label>
        <input type="password" id="password" v-model="password" />
      </div>
      <button type="submit">Login</button>
    </form>
    <!-- Pop-up message -->
    <div v-if="showNonAdminMessage" class="popup">
      <div class="popup-content">
        <p class="popup-text">You are not an Admin.</p>
        <button @click="redirectToSignup" class="popup-button">OK</button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      username: "",
      password: "",
      email: "",
      user_id: 1,
      auth: null,
      error: "",
      error2: "",
      showNonAdminMessage: false, // Flag to control the display of the pop-up
    };
  },
  methods: {
    async login() {
      try {
        const data = await fetch("http://127.0.0.1:5000/api/login", {
          method: "POST",
          headers: {
            "Access-Control-Allow-Origin": "*",
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            email: this.email,
            password: this.password,
          }),
        });
        const response = await data.json();
        if (response.errors) {
          if (response.errors[1]) {
            this.error = response.errors[1];
          } else {
            this.error2 = response.errors[0];
          }
        } else {
          this.auth = response.auth_token;
          if (response.user_role === "admin") {
            sessionStorage.setItem("auth-token", this.auth);
            sessionStorage.setItem("email", response.email);
            sessionStorage.setItem("user_id", response.user_id);
            sessionStorage.setItem("user_role", response.user_role);
            this.$router.push("/admindashboard");
          } else {
            // Show pop-up message
            this.showNonAdminMessage = true;
          }
        }
      } catch (error) {
        console.error("error during admin login", error);
      }
      console.log("Logging in...");
    },
    redirectToSignup() {
      // Hide the pop-up message
      this.showNonAdminMessage = true;
      // Redirect to the signup page
      this.$router.push("/signup");
    },
  },
};
</script>

<style scoped>
.popup {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}

.popup-content {
  background-color: #fff;
  padding: 20px;
  border-radius: 5px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.3);
}

.popup-text {
  margin-bottom: 10px;
}

.popup-button {
  padding: 10px 20px;
  background-color: #22c96d;
  color: #fff;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.popup-button:hover {
  background-color: #890636;
}
.login-container {
  width: 100%;
  max-width: 400px;
  margin: 0 auto;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 5px;
  background-color: #fff;
}

.login-form {
  margin-top: 20px;
}

.login-form div {
  margin-bottom: 15px;
}

.login-form label {
  display: block;
  margin-bottom: 5px;
}

.login-form input[type="text"],
.login-form input[type="password"] {
  width: 100%;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
}

.login-form button {
  width: 100%;
  padding: 10px;
  border: none;
  border-radius: 5px;
  background-color: #007bff;
  color: #fff;
  cursor: pointer;
}

.login-form button:hover {
  background-color: #0056b3;
}

.error {
  color: #ff0000;
  margin-bottom: 10px;
}
</style>
