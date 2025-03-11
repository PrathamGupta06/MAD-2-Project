<template>
    <nav class="navbar navbar-expand-lg navbar-light bg-light mb-4">
        <div class="container">
            <router-link class="navbar-brand" to="/user/dashboard">User</router-link>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav me-auto">
                    <li class="nav-item">
                        <router-link class="nav-link" to="/user/dashboard">Home</router-link>
                    </li>
                    <li class="nav-item">
                        <router-link class="nav-link" to="/user/scores">Scores</router-link>
                    </li>
                    <li class="nav-item">
                        <router-link class="nav-link" to="/user/summary">Summary</router-link>
                    </li>
                </ul>
                <button class="btn btn-outline-danger" @click="logout">Logout</button>
            </div>
        </div>
    </nav>
    <div class="container mt-4">
    <div class="row">
      <div class="col-md-6">
        <h2>Subject-wise Quiz Summary</h2>
        <div class="chart-container">
          <canvas id="subjectChart"></canvas>
        </div>
      </div>
      <div class="col-md-6">
        <h2>Monthly Quiz Attempts</h2>
        <div class="chart-container">
          <canvas id="monthlyChart"></canvas>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import Chart from 'chart.js/auto';
import axios from 'axios';

export default {
  data() {
    return {
      subjectAttemptsData: [],
      monthlyData: []
    };
  },
  async mounted() {
    await this.fetchUserSummary();
    this.renderCharts();
  },
  methods: {
    async fetchUserSummary() {
      const response = await axios.get('http://localhost:5000/api/user/summary', {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      });
      this.subjectAttemptsData = response.data.subject_data;
      this.monthlyData = response.data.monthly_data;
    },
    renderCharts() {
      const subjectNames = this.subjectAttemptsData.map(item => item.subject_name);
      const attemptedQuizzes = this.subjectAttemptsData.map(item => item.attempted_quizzes);
      
      new Chart(document.getElementById('subjectChart'), {
        type: 'bar',
        data: {
          labels: subjectNames,
          datasets: [{
            label: 'Attempted Quizzes',
            data: attemptedQuizzes,
            backgroundColor: 'rgba(75, 192, 192, 0.6)'
          }]
        }
      });

      const months = this.monthlyData.map(item => item.month);
      const attempts = this.monthlyData.map(item => item.attempts);
      
      new Chart(document.getElementById('monthlyChart'), {
        type: 'line',
        data: {
          labels: months,
          datasets: [{
            label: 'Monthly Attempts',
            data: attempts,
            borderColor: 'rgba(255, 99, 132, 1)',
            fill: false
          }]
        }
      });
    }
  }
};
</script>