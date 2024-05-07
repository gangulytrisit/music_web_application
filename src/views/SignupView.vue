<template>
  <div class="container">
    <div class="row justify-content-center">
      <div class="col-md-6 col-sm-12">
        <div class="signup-form p-4 rounded">
          <p class="alert alert-danger" v-if="error_1 || error_2">
            {{ error_1 || error_2 }}
          </p>
          <h3 class="title" align="center">Sign Up</h3>
          <div class="form-group">
            <label for="email">Email Address</label>
            <input
              type="email"
              class="form-control"
              name="email"
              id="email"
              v-model="email"
              placeholder="Enter your email..."
              required
            />
          </div>
          <div class="form-group">
            <label for="username">Name</label>
            <input
              type="text"
              class="form-control"
              name="username"
              id="username"
              v-model="username"
              placeholder="Enter your name..."
              required
            />
          </div>
          <div class="form-group">
            <label for="password">Password</label>
            <input
              type="password"
              class="form-control"
              name="password"
              id="password"
              v-model="password"
              placeholder="Enter your password..."
              minlength="6"
              required
            />
          </div>
          <div class="form-group">
            <label for="role">Select Role</label>
            <select v-model="role" class="form-control" required>
              <option disabled value="">Please select</option>
              <option value="creator">Creator</option>
              <option value="user">User</option>
            </select>
          </div>
          <button
            type="submit"
            @click="signup"
            class="btn btn-primary btn-lg btn-block"
          >
            Sign Up
          </button>

          <p class="mt-3 text-center">
            Already registered?<br />
            <router-link :to="{ name: 'userlogin' }">User Login</router-link>
            <span class="mx-2"></span>
            <router-link :to="{ name: 'creatorlogin' }"
              >Creator Login</router-link
            >
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "SignupForm",
  data() {
    return {
      email: null,
      username: null,
      password: null,
      role: null,
      error_1: "",
      error_2: "",
    };
  },
  methods: {
    async signup() {
      try {
        fetch("http://127.0.0.1:5000/api/user", {
          method: "POST",
          headers: {
            "Access-Control-Allow-Origin": "*",
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            email: this.email,
            username: this.username,
            password: this.password,
            role: this.role,
          }),
        })
          .then((response) => response.json())
          .then(async (data) => {
            console.log(data);
            if (!this.username) {
              this.error_1 = "Please enter a valid username";
            }
            if (!this.password) {
              this.error_2 = "Please enter a valid password";
            } else if (!this.passValidation(this.password)) {
              this.error_2 = "Password requires at least 6 characters.";
            }
            if (!this.email) {
              this.error_1 = "Please enter a valid email";
              console.log("wrong email");
            } else if (!this.emailValidation(this.email)) {
              this.error_1 = "Not valid email";
            } else {
              if (this.role === "creator") {
                this.$router.push("creatorlogin");
              } else {
                this.$router.push("userlogin");
              }
            }
          })
          .catch((err) => {
            console.log(err);
          });
      } catch (error) {
        console.log("Registration Failed: ", error);
      }
    },
    emailValidation: function (email) {
      var result =
        /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,3}))$/;
      return result.test(email);
    },
    passValidation: function (passs) {
      // var result = /(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{6,}/
      var result = /.{6,}/;
      return result.test(passs);
    },
  },
};
</script>

<style scoped>
.signup-form {
  max-width: 400px;
  margin: 50px auto;
  padding: 20px;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}

.title {
  font-size: 24px;
}

.form-group label {
  font-weight: bold;
}

.form-group input[type="email"],
.form-group input[type="text"],
.form-group input[type="password"],
.form-group select {
  width: 100%;
  padding: 10px;
  margin-bottom: 15px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

.btn {
  padding: 10px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.btn-primary {
  background-color: #007bff;
  color: #fff;
}

.btn-primary:hover {
  background-color: #0056b3;
}

.text-center {
  text-align: center;
}

.text-center span {
  margin: 0 10px;
}
</style>
