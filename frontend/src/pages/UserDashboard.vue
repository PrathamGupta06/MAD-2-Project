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
                            <td>
                                <button class="btn btn-info btn-sm me-2" @click="showQuizDetails(quiz)">View Details</button>
                                <router-link v-if="!quiz.attempted" :to="`/user/quiz/${quiz.id}`" class="btn btn-primary btn-sm">Attempt Quiz</router-link>
                                <span v-else class="text-muted">Already Attempted</span>
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
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="quiz in upcomingQuizzes" :key="quiz.id">
                            <td>{{ quiz.chapter_name }}</td>
                            <td>{{ quiz.subject_name }}</td>
                            <td>{{ quiz.date_of_quiz }}</td>
                            <td>{{ quiz.time_duration }}</td>
                            <td>
                                <button class="btn btn-info btn-sm" @click="showQuizDetails(quiz)">View Details</button>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    </div>

    <!-- Quiz Details Modal -->
    <div class="modal fade" id="quizDetailsModal" tabindex="-1" aria-labelledby="quizDetailsModalLabel" aria-hidden="true">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title" id="quizDetailsModalLabel">Quiz Details</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body" v-if="selectedQuiz">
                    <div class="card">
                        <div class="card-body">
                            <h6 class="card-subtitle mb-2 text-muted">{{ selectedQuiz.subject_name }}</h6>
                            <h5 class="card-title">{{ selectedQuiz.chapter_name }}</h5>
                            <div class="quiz-details">
                                <p><strong>Date:</strong> {{ selectedQuiz.date_of_quiz }}</p>
                                <p><strong>Duration:</strong> {{ selectedQuiz.time_duration }} minutes</p>
                                <p><strong>Num Questions:</strong> {{ selectedQuiz.num_questions }} </p>
                                <p>
                                    <strong>Status: </strong> 
                                    <span v-if="selectedQuiz.attempted" class="text-success">Attempted</span>
                                    <span v-else class="text-warning">Not Attempted</span>
                                </p>
                            </div>
                        </div>
                    </div>
                </div>
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
      error: '',
      selectedQuiz: null,
      quizModal: null
    }
  },
  methods: {
    async getRequest(route) {
        const response = await axios.get(route, {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          }
        });
        return response;
    },
    async fetchUpcomingQuizzes() {
      this.loading = true;
      this.error = '';
      try {
        const response = await this.getRequest('http://localhost:5000/api/quizzes/upcoming');
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
      this.$router.push('/login');
    },
    showQuizDetails(quiz) {
      this.selectedQuiz = quiz;
      this.quizModal.show();
    },
    closeModal() {
      this.quizModal.hide();
    }
  },
  mounted() {
    this.fetchUpcomingQuizzes();
    this.quizModal = new bootstrap.Modal(document.getElementById('quizDetailsModal'));
  }
};
</script>