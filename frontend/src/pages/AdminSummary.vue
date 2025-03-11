<template>
    <nav class="navbar navbar-expand-lg navbar-light bg-light mb-4">
        <div class="container">
            <router-link class="navbar-brand" to="/admin/dashboard">Admin Panel</router-link>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav me-auto">
                    <li class="nav-item">
                        <router-link class="nav-link" to="/admin/dashboard">Home</router-link>
                    </li>
                    <li class="nav-item">
                        <router-link class="nav-link" to="/admin/quiz">Quiz</router-link>
                    </li>
                    <li class="nav-item">
                        <router-link class="nav-link" to="/admin/summary">Summary</router-link>
                    </li>
                </ul>
                <button class="btn btn-outline-danger" @click="logout">Logout</button>
            </div>
        </div>
    </nav>

    <div class="container mt-4">
    <div class="row">
      <div class="col-md-6">
        <h2>Total Quiz Attempts per Subject</h2>
        <div class="chart-container">
          <canvas id="adminAttemptsChart"></canvas>
        </div>
      </div>
      <div class="col-md-6">
        <h2>Average Score per Subject</h2>
        <div class="chart-container">
          <canvas id="averageScoreChart"></canvas>
        </div>
      </div>
    </div>
    <div class="row mt-4">
      <div class="col-md-6">
        <h2>Total Users</h2>
        <p>{{ totalUsers }}</p>
      </div>
      <div class="col-md-6">
        <h2>Total Quiz Attempts</h2>
        <p>{{ totalAttempts }}</p>
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
      averageScoreData: [],
      totalUsers: 0,
      totalAttempts: 0
    };
  },
  async mounted() {
    await this.fetchAdminSummary();
    this.renderAdminCharts();
  },
  methods: {
    async fetchAdminSummary() {
      const response = await axios.get('http://localhost:5000/api/admin/summary', {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      });
      this.subjectAttemptsData = response.data.subject_stats;
      this.averageScoreData = response.data.subject_stats;
      this.totalUsers = response.data.user_stats.total_users;
      this.totalAttempts = response.data.user_stats.total_attempts;
    },
    renderAdminCharts() {
      const subjectNames = this.subjectAttemptsData.map(item => item.subject_name);
      const totalAttempts = this.subjectAttemptsData.map(item => item.total_attempts);
      const averageScores = this.averageScoreData.map(item => item.average_score);
      
      new Chart(document.getElementById('adminAttemptsChart'), {
        type: 'pie',
        data: {
          labels: subjectNames,
          datasets: [{
            label: 'Total Quiz Attempts',
            data: totalAttempts,
            backgroundColor: [
              'rgba(255, 99, 132, 0.6)',
              'rgba(54, 162, 235, 0.6)',
              'rgba(255, 206, 86, 0.6)',
              'rgba(75, 192, 192, 0.6)',
              'rgba(153, 102, 255, 0.6)',
              'rgba(255, 159, 64, 0.6)'
            ]
          }]
        }
      });
      
      new Chart(document.getElementById('averageScoreChart'), {
        type: 'bar',
        data: {
          labels: subjectNames,
          datasets: [{
            label: 'Average Score',
            data: averageScores,
            backgroundColor: 'rgba(255, 206, 86, 0.6)'
          }]
        }
      });
    }
  }
};
</script>
