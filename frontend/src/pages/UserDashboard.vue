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
                        <router-link class="nav-link" to="/user/quiz">Scores</router-link>
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
        <div v-if="loading" class="text-center">Loading upcoming quizzes...</div>
        <div v-if="error" class="alert alert-danger">{{ error }}</div>

        <div v-if="todayQuizzes.length > 0">
            <h3>Today's Quizzes</h3>
            <div class="table-responsive">
                <table class="table table-striped table-hover">
                    <thead>
                        <tr>
                            <th>Chapter Name</th>
                            <th>Subject</th>
                            <th>Date</th>
                            <th>Duration (mins)</th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="quiz in todayQuizzes" :key="quiz.id">
                            <td>{{ quiz.chapter_name }}</td>
                            <td>{{ quiz.subject_name }}</td>
                            <td>{{ quiz.date_of_quiz }}</td>
                            <td>{{ quiz.time_duration }}</td>
                            <td v-if="quiz.attempted"> Already Attempted this quiz </td>
                            <td v-else>
                                <router-link :to="`/user/quiz/${quiz.id}`" class="btn btn-primary">Attempt Quiz</router-link>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
        <div v-else>
            <h3>No quizzes today</h3>
        </div>
        <div v-if="upcomingQuizzes.length > 0">
            <h3>Upcoming Quizzes</h3>
            <div class="table-responsive">
                <table class="table table-striped table-hover">
                    <thead>
                        <tr>
                            <th>Chapter Name</th>
                            <th>Subject</th>
                            <th>Date</th>
                            <th>Duration (mins)</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="quiz in upcomingQuizzes" :key="quiz.id">
                            <td>{{ quiz.chapter_name }}</td>
                            <td>{{ quiz.subject_name }}</td>
                            <td>{{ quiz.date_of_quiz }}</td>
                            <td>{{ quiz.time_duration }}</td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'UserDashboard',
  data() {
    return {
      upcomingQuizzes: [],
      todayQuizzes: [],
      loading: false,
      error: ''
    }
  },
  methods: {
    async fetchUpcomingQuizzes() {
      this.loading = true;
      this.error = '';
      try {
        const response = await axios.get('http://localhost:5000/api/quizzes/upcoming', {
                    headers: {
                        'Authorization': `Bearer ${localStorage.getItem('token')}`
                    }
                });
        this.upcomingQuizzes = response.data.upcoming_quizzes;
        this.todayQuizzes = response.data.today_quizzes;
      } catch (err) {
        this.error = 'Failed to load upcoming quizzes';
        console.error(err);
      } finally {
        this.loading = false;
      }
    },
    logout() {
        localStorage.removeItem('token');
        this.$router.push('/login');    }
  },
  mounted() {
    this.fetchUpcomingQuizzes();
  }
};
</script>