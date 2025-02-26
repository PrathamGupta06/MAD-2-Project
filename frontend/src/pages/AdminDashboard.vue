<template>
    <div class="container">
        <h2 class="mb-4">Admin Dashboard</h2>
        
        <div class="row mb-4">
            <div class="col-md-6">
                <div class="card">
                    <div class="card-header">
                        <h3 class="card-title">Quizzes</h3>
                    </div>
                    <div class="card-body">
                        <div v-if="loading.quizzes">Loading quizzes...</div>
                        <div v-else-if="error.quizzes" class="text-danger">{{ error.quizzes }}</div>
                        <div v-else-if="quizzes.length === 0" class="text-muted">
                            No quizzes available.
                        </div>
                        <div v-else>
                            <ul class="list-group">
                                <li v-for="quiz in quizzes" :key="quiz.id" class="list-group-item">
                                    <div class="d-flex justify-content-between align-items-center">
                                        <div>
                                            <h5 class="mb-1">Quiz #{{ quiz.id }}</h5>
                                            <p class="mb-1">Chapter: {{ quiz.chapter_id }}</p>
                                            <small>Date: {{ new Date(quiz.date_of_quiz).toLocaleString() }}</small>
                                        </div>
                                        <span class="badge bg-primary rounded-pill">{{ quiz.num_questions }} questions</span>
                                    </div>
                                </li>
                            </ul>
                        </div>
                    </div>
                </div>
            </div>
            <div class="card-body">
                        <div v-if="loading.subjects">Loading subjects...</div>
                        <div v-else-if="error.subjects" class="text-danger">{{ error.subjects }}</div>
                        <div v-else-if="subjects.length === 0" class="text-muted">
                            No subjects available.
                        </div>
                        <div v-else>
                            <div v-for="subject in subjects" :key="subject.id" class="mb-4 col-md-4">
                                <div class="card">
                                    <div class="card-header bg-light">
                                        <h5 class="mb-0">{{ subject.name }}</h5>
                                    </div>
                                    <div class="card-body">
                                        <p class="card-text">{{ subject.description }}</p>
                                        <h6 class="mt-3 mb-2">Chapters:</h6>
                                        <div class="table-responsive">
                                            <table class="table table-bordered table-hover">
                                                <thead class="table-light">
                                                    <tr>
                                                        <th>Chapter Name</th>
                                                        <th>Description</th>
                                                        <th>Actions</th>
                                                    </tr>
                                                </thead>
                                                <tbody>
                                                    <tr v-for="chapter in subject.chapters" :key="chapter.id">
                                                        <td>{{ chapter.name }}</td>
                                                        <td>{{ chapter.description }}</td>
                                                        <td>
                                                            <button class="btn btn-sm btn-outline-primary me-2" @click="editChapter(chapter.id)">
                                                                <i class="bi bi-pencil"></i> Edit
                                                            </button>
                                                            <button class="btn btn-sm btn-outline-danger" @click="deleteChapter(chapter.id)">
                                                                <i class="bi bi-trash"></i> Delete
                                                            </button>
                                                        </td>
                                                    </tr>
                                                </tbody>
                                            </table>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
        </div>

        

        <div class="row mb-4">
            <div class="col-md-4">
                <router-link to="/admin/quizzes" class="btn btn-primary w-100">Manage Quizzes</router-link>
            </div>
            <div class="col-md-4">
                <router-link to="/admin/questions" class="btn btn-primary w-100">Manage Questions</router-link>
            </div>
            <div class="col-md-4">
                <router-link to="/admin/users" class="btn btn-primary w-100">Manage Users</router-link>
            </div>
        </div>
        
        <router-view />
    </div>
</template>

<script>
import axios from 'axios';

export default {
    name: 'AdminDashboard',
    data() {
        return {
            quizzes: [],
            subjects: [],
            loading: {
                quizzes: true,
                subjects: true
            },
            error: {
                quizzes: null,
                subjects: null
            }
        };
    },
    mounted() {
        this.fetchData();
    },
    methods: {
        async fetchData() {
            // Fetch quizzes
            try {
                const quizzesResponse = await axios.get('http://localhost:5000/api/quizzes', {
                    headers: {
                        'Authorization': `Bearer ${localStorage.getItem('token')}`
                    }
                });
                this.quizzes = quizzesResponse.data.quizzes;
                this.error.quizzes = null;
            } catch (error) {
                this.error.quizzes = 'Failed to load quizzes';
                console.error('Error fetching quizzes:', error);
            } finally {
                this.loading.quizzes = false;
            }

            // Fetch subjects
            try {
                const subjectsResponse = await axios.get('http://localhost:5000/api/subjects', {
                    headers: {
                        'Authorization': `Bearer ${localStorage.getItem('token')}`
                    }
                });
                this.subjects = subjectsResponse.data.subjects;
                this.error.subjects = null;
            } catch (error) {
                this.error.subjects = 'Failed to load subjects';
                console.error('Error fetching subjects:', error);
            } finally {
                this.loading.subjects = false;
            }
        }
    },
};

</script>