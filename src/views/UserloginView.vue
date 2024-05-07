<template>
  <div class="login-container">
    <h2>User Login</h2>
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
    <p class="register-link">
      Don't have an account?
      <router-link to="/signup">Register here</router-link>
    </p>
    <div v-if="showNonUserMessage" class="popup">
      <div class="popup-content">
        <p class="popup-text">You are not registered as an User.</p>
        <button @click="redirectToSignup" class="popup-button">OK</button>
      </div>
    </div>
  </div>
</template>

<script>
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
      username: "",
      password: "",
      email: "",
      user_id: null,
      auth: null,
      error: "",
      error2: "",
      showNonUserMessage: false,
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
          console.log(response);
          this.auth = response.auth_token;
          this.user_id = response.user_id; // Set user_id from response
          sessionStorage.setItem("email", this.email);
          sessionStorage.setItem("auth-token", this.auth);
          sessionStorage.setItem("user_id", this.user_id); // Set user_id in session storage
          console.log(this.user_id);
          console.log(response.user_role);
          if (response.user_role === "user") {
            try {
              const initialDataResponse = await fetch(
                `http://127.0.0.1:5000/api/user/${this.email}`,
                {
                  headers: getHeaders(),
                }
              );
              const initialData = await initialDataResponse.json();
              console.log(initialData);
              sessionStorage.setItem("user_id", initialData.user_id);
            } catch (error) {
              console.error("Error fetching initial data:", error);
            }
            this.$router.push("/userdashboard");
          } else {
            this.showNonUserMessage = true;
          }
        }
      } catch (error) {
        console.error("error during creator login", error);
      }
      console.log("Logging in...");
    },
    redirectToSignup() {
      this.showNonUserMessage = true;
      // Redirect to the signup page
      this.$router.push("/signup");
    },
  },
};
</script>

<style scoped>
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

.register-link {
  margin-top: 10px;
  text-align: center;
}
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
</style>
