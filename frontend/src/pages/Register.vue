<template>
    <div class="container">
      <h2>Register</h2>
      <form @submit.prevent="register">
        <div class="mb-3">
          <label class="form-label">Username</label>
          <input type="text" v-model="username" class="form-control" required />
        </div>
        <div class="mb-3">
          <label class="form-label">Password</label>
          <input type="password" v-model="password" class="form-control" required />
        </div>
        <div class="mb-3">
          <label class="form-label">Full Name</label>
          <input type="text" v-model="fullName" class="form-control" required />
        </div>
        <div class="mb-3">
          <label class="form-label">Date of Birth</label>
          <input type="date" v-model="dob" class="form-control" required />
        </div>
        <div class="mb-3">
          <label class="form-label">Qualification</label>
          <input type="text" v-model="qualification" class="form-control" required />
        </div>
        <button type="submit" class="btn btn-primary">Register</button>
        <p>Already have an account? <a href="/login">Login</a></p>
      </form>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    data() {
      return {
        username: '',
        password: '',
        fullName: '',
        dob: '',
        qualification: ''
      };
    },
    methods: {
      async register() {
        try {
          const formattedDob = new Date(this.dob).toLocaleDateString('en-GB');
          await axios.post('http://localhost:5000/api/register', {
            username: this.username,
            password: this.password,
            full_name: this.fullName,
            dob: formattedDob,
            qualification: this.qualification
          });
          alert('Registration successful! Please login.');
          this.$router.push('/login');
        } catch (error) {
          alert('Registration failed');
        }
      }
    }
  };
  </script>