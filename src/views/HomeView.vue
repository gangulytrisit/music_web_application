<template>
  <div class="home">
    <img class="logo" alt="Vue logo" src="../assets/logo.png" />
    <router-link to="/signup" class="signup">Signup</router-link>
    <div class="login-dropdown">
      <button class="login-dropdown-button">Login</button>
      <div class="login-dropdown-content">
        <!-- <router-link to="/adminlogin">Admin Login</router-link> -->
        <router-link to="/userlogin">User Login</router-link>
        <router-link to="/creatorlogin">Creator Login</router-link>
      </div>
    </div>

    <div class="welcome-message">Welcome to, <b class="swar-text">Swar</b></div>
  </div>
</template>

<script>
export default {
  name: "HomeView",
};
</script>

<style>
.welcome-message {
  position: fixed;
  top: 0;
  left: 0;
  margin: 20px;
  font-weight: bold;
  font-size: 24px;
  color: #333;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2);
}
.swar-text {
  color: #760505;
  font-style: italic;
}

.signup {
  position: absolute;
  top: 0;
  right: 0;
  margin: 20px;
  color: red;
}

.logo {
  max-width: 100%;
  max-height: 100%;
}

.login-dropdown {
  position: absolute;
  top: 0;
  right: 100px;
  margin: 20px;
  display: inline-block;
  color: red;
}

.login-dropdown-button {
  background-color: transparent;
  border: none;
  cursor: pointer;
}

.login-dropdown-content {
  display: none;
  position: absolute;
  background-color: #f9f9f9;
  min-width: 120px;
  z-index: 1;
}

.login-dropdown-content a {
  color: black;
  padding: 12px 16px;
  text-decoration: none;
  display: block;
}

.login-dropdown-content a:hover {
  background-color: #f1f1f1;
}

.login-dropdown:hover .login-dropdown-content {
  display: block;
  background-color: #ec8495;
}
</style>
