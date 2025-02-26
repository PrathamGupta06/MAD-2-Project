<template>
    <div class="container">
      <h2>Login</h2>
      <form @submit.prevent="login">
        <div class="mb-3">
          <label class="form-label">Username</label>
          <input type="text" v-model="username" class="form-control" required />
        </div>
        <div class="mb-3">
          <label class="form-label">Password</label>
          <input type="password" v-model="password" class="form-control" required />
        </div>
        <button type="submit" class="btn btn-primary">Login</button>
      </form>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    data() {
      return {
        username: '',
        password: ''
      };
    },
    methods: {
      async login() {
        try {
          const response = await axios.post('http://localhost:5000/api/login', {
            username: this.username,
            password: this.password
          });
          
          localStorage.setItem('token', response.data.access_token);
          localStorage.setItem('role', response.data.role);

          if (response.data.role === 'admin') {
            this.$router.push('/admin/dashboard');
            return;
          }
          this.$router.push('/dashboard');
        } catch (error) {
          alert('Invalid credentials');
        }
      }
    }
  };
  </script>