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
        <h2>My Quiz Scores</h2>
        <div v-if="loading" class="text-center">Loading scores...</div>
        <div v-if="error" class="alert alert-danger">{{ error }}</div>
        <div v-if="userScores.length > 0" class="table-responsive">
            <table class="table table-striped table-hover">
                <thead>
                    <tr>
                        <th>Quiz ID</th>
                        <th>Attempt Date</th>
                        <th>Total Score</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="score in userScores" :key="score.quiz_id">
                        <td><a href="#" @click.prevent="showQuizDetails(score.quiz_id)">{{ score.quiz_id }}</a></td>
                        <td>{{ formatDate(score.timestamp) }}</td>
                        <td>{{ score.total_score }}</td>
                    </tr>
                </tbody>
            </table>
        </div>
        <div v-else-if="!loading" class="alert alert-info">
            No quiz scores available yet.
        </div>
    </div>
    <div class="modal fade" id="quizDetailsModal" tabindex="-1" aria-labelledby="quizDetailsModalLabel" aria-hidden="true">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title" id="quizDetailsModalLabel">Quiz Details</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    <div v-if="selectedQuizDetails">
                        <div class="mb-3">
                            <strong>Chapter Name:</strong> {{ selectedQuizDetails.chapter_name }}
                        </div>
                        <div class="mb-3">
                            <strong>Subject Name:</strong> {{ selectedQuizDetails.subject_name }}
                        </div>
                        <div class="mb-3">
                            <strong>Number of Questions:</strong> {{ selectedQuizDetails.num_questions }}
                        </div>
                        <div class="mb-3">
                            <strong>Quiz Date:</strong> {{ selectedQuizDetails.date_of_quiz }}
                        </div>
                    </div>
                    <div v-else class="text-center">
                        <div class="spinner-border" role="status" v-if="loadingQuizDetails">
                            <span class="visually-hidden">Loading...</span>
                        </div>
                        <div v-else class="text-danger">Failed to load quiz details</div>
                    </div>
                </div>
            </div>
        </div>
    </div>

</template>

<script>
import axios from 'axios';

export default {
    name: 'UserScores',
    data() {
        return {
            userScores: [],
            loading: false,
            error: '',
            selectedQuizDetails: null,
            loadingQuizDetails: false
        }
    },
    methods: {
        async fetchScores() {
            this.loading = true;
            this.error = '';
            try {
                const response = await axios.get('http://localhost:5000/api/scores', {
                    headers: {
                        'Authorization': `Bearer ${localStorage.getItem('token')}`
                    }
                });
                this.userScores = response.data.scores;
            } catch (err) {
                this.error = 'Failed to load scores';
                console.error(err);
            } finally {
                this.loading = false;
            }
        },
        formatDate(timestamp) {
            return new Date(timestamp).toLocaleString();
        },
        logout() {
            localStorage.removeItem('token');
            this.$router.push('/login');
        },
        async showQuizDetails(quizId) {
            this.loadingQuizDetails = true;
            this.selectedQuizDetails = null;
            try {
                const response = await axios.get(`http://localhost:5000/api/quizzes/${quizId}`, {
                    headers: {
                        'Authorization': `Bearer ${localStorage.getItem('token')}`
                    }
                });
                this.selectedQuizDetails = response.data;
                const modal = new bootstrap.Modal(document.getElementById('quizDetailsModal'));
                modal.show();
            } catch (err) {
                console.error('Failed to load quiz details:', err);
            } finally {
                this.loadingQuizDetails = false;
            }
        }
    },
    mounted() {
        this.fetchScores();
    }
};
</script>