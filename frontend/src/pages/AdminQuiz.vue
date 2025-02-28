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
    
    <div class="container">
        <div class="d-flex justify-content-between align-items-center mb-4">
            <h2>Quizzes</h2>
            <button class="btn btn-primary" @click="openCreateQuizModal">
                <i class="bi bi-plus-circle"></i> Create Quiz
            </button>
        </div>
        <div class="row">
            <div v-for="quiz in quizzes" :key="quiz.id" class="col-md-6 mb-4">
                <div class="card">
                    <div class="card-header d-flex justify-content-between align-items-center">
                        <h5 class="card-title mb-0">Quiz #{{ quiz.id }}</h5>
                        <button class="btn btn-sm btn-info text-white" @click="viewQuizDetails(quiz)">
                            <i class="bi bi-eye"></i> View Details
                            # TODO: Add a modal for this view Details button
                        </button>
                    </div>
                    <div class="card-body">
                        <div class="table-responsive">
                            <table class="table">
                                <thead>
                                    <tr>
                                        <th>Question ID</th>
                                        <th>Question Title</th>
                                        <th>Actions</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr v-for="question in quiz.questions" :key="question.id">
                                        <td>{{ question.id }}</td>
                                        <td>{{ question.question_statement }}</td>
                                        <td>
                                            <button class="btn btn-sm btn-primary me-2" @click="editQuestion(question.id)">Edit</button>
                                            <button class="btn btn-sm btn-danger" @click="deleteQuestion(question.id)">Delete</button>
                                        </td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                        <button class="btn btn-success mt-3" @click="addQuestion(quiz.id)">
                            Add Question
                        </button>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- Create Quiz Modal -->
    <div class="modal fade" id="createQuizModal" tabindex="-1" aria-labelledby="createQuizModalLabel" aria-hidden="true">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title" id="createQuizModalLabel">Create New Quiz</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    <form @submit.prevent="createQuiz">
                        <div class="mb-3">
                            <label for="subjectId" class="form-label">Subject</label>
                            <select class="form-control" id="subjectId" v-model="quizForm.subject_id" required @change="loadChapters">
                                <option value="">Select a subject</option>
                                <option v-for="subject in subjects" :key="subject.id" :value="subject.id">
                                    {{ subject.name }}
                                </option>
                            </select>
                        </div>
                        <div class="mb-3">
                            <label for="chapterId" class="form-label">Chapter</label>
                            <select class="form-control" id="chapterId" v-model="quizForm.chapter_id" required>
                                <option value="">Select a chapter</option>
                                <option v-for="chapter in filteredChapters" :key="chapter.id" :value="chapter.id">
                                    {{ chapter.name }}
                                </option>
                            </select>
                        </div>
                        <div class="mb-3">
                            <label for="quizDate" class="form-label">Date of Quiz</label>
                            <input type="datetime-local" class="form-control" id="quizDate" v-model="quizForm.date_of_quiz" required>
                        </div>
                        <div class="mb-3">
                            <label for="timeDuration" class="form-label">Time Duration (minutes)</label>
                            <input type="number" class="form-control" id="timeDuration" v-model="quizForm.time_duration" required>
                        </div>
                        <div class="modal-footer">
                            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
                            <button type="submit" class="btn btn-primary">Create Quiz</button>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </div>

    <!-- Question Modal -->
    <div class="modal fade" id="questionModal" tabindex="-1" aria-labelledby="questionModalLabel" aria-hidden="true">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title" id="questionModalLabel">{{ editingQuestion ? 'Edit Question' : 'Add Question' }}</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    <form @submit.prevent="submitQuestion">
                        <div class="mb-3">
                            <label for="questionStatement" class="form-label">Question Statement</label>
                            <textarea class="form-control" id="questionStatement" v-model="questionForm.question_statement" required rows="3"></textarea>
                        </div>
                        <div class="mb-3">
                            <label for="option1" class="form-label">Option 1</label>
                            <input type="text" class="form-control" id="option1" v-model="questionForm.option1" required>
                        </div>
                        <div class="mb-3">
                            <label for="option2" class="form-label">Option 2</label>
                            <input type="text" class="form-control" id="option2" v-model="questionForm.option2" required>
                        </div>
                        <div class="mb-3">
                            <label for="option3" class="form-label">Option 3</label>
                            <input type="text" class="form-control" id="option3" v-model="questionForm.option3" required>
                        </div>
                        <div class="mb-3">
                            <label for="option4" class="form-label">Option 4</label>
                            <input type="text" class="form-control" id="option4" v-model="questionForm.option4" required>
                        </div>
                        <div class="mb-3">
                            <label for="correctAnswer" class="form-label">Correct Answer</label>
                            <select class="form-control" id="correctAnswer" v-model="questionForm.correct_answer" required>
                                <option value="">Select correct answer</option>
                                <option :value="questionForm.option1">Option 1</option>
                                <option :value="questionForm.option2">Option 2</option>
                                <option :value="questionForm.option3">Option 3</option>
                                <option :value="questionForm.option4">Option 4</option>
                            </select>
                        </div>
                        <div class="modal-footer">
                            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
                            <button type="submit" class="btn btn-primary">{{ editingQuestion ? 'Update' : 'Create' }}</button>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios';

export default {
    name: 'AdminQuiz',
    data() {
        return {
            quizzes: [],
            subjects: [],
            quizForm: {
                subject_id: '',
                chapter_id: '',
                date_of_quiz: '',
                time_duration: ''
            },
            questionForm: {
                quiz_id: null,
                question_statement: '',
                option1: '',
                option2: '',
                option3: '',
                option4: '',
                correct_answer: ''
            },
            editingQuestion: false,
            editingQuestionId: null,
            quizModal: null,
            questionModal: null,
            selectedQuiz: null,
            quizDetailsModal: null,
        }
    },
    computed: {
        filteredChapters() {
            if (!this.quizForm.subject_id) return [];
            const subject = this.subjects.find(s => s.id === this.quizForm.subject_id);
            return subject ? subject.chapters : [];
        }
    },
    mounted() {
        this.getSubjects();
        this.getQuizzes();
    },
    methods: {
        async getSubjects() {
            try {
                const response = await axios.get('http://localhost:5000/api/subjects', {
                    headers: {
                        'Authorization': `Bearer ${localStorage.getItem('token')}`
                    }
                });
                this.subjects = response.data.subjects;
            } catch (error) {
                console.error(error);
            }
        },
        loadChapters() {
            this.quizForm.chapter_id = '';
        },
        resetForm() {
            this.quizForm = {
                subject_id: '',
                chapter_id: '',
                date_of_quiz: '',
                time_duration: ''
            };
        },
        logout() {
            localStorage.removeItem('token');
            this.$router.push('/login');
        },
        async getQuizzes() {
            try {
                const QuizResponse = await axios.get('http://localhost:5000/api/quizzes', {
                    headers: {
                        'Authorization': `Bearer ${localStorage.getItem('token')}`
                    }
                });
                this.quizzes = QuizResponse.data.quizzes;
            } catch (error) {
                console.error(error);
            }
        },
        async editQuestion(questionId) {
            try {
                const response = await axios.get(`http://localhost:5000/api/questions/${questionId}`, {
                    headers: {
                        'Authorization': `Bearer ${localStorage.getItem('token')}`
                    }
                });
                const question = response.data;
                this.questionForm = {
                    quiz_id: question.quiz_id,
                    question_statement: question.question_statement,
                    option1: question.options[0],
                    option2: question.options[1],
                    option3: question.options[2],
                    option4: question.options[3],
                    correct_answer: question.correct_answer
                };
                this.editingQuestion = true;
                this.editingQuestionId = questionId;
                this.questionModal = new bootstrap.Modal(document.getElementById('questionModal'));
                this.questionModal.show();
            } catch (error) {
                console.error(error);
                alert('Failed to load question details');
            }
        },
        addQuestion(quizId) {
            this.questionForm = {
                quiz_id: quizId,
                question_statement: '',
                option1: '',
                option2: '',
                option3: '',
                option4: '',
                correct_answer: ''
            };
            this.editingQuestion = false;
            this.editingQuestionId = null;
            this.questionModal = new bootstrap.Modal(document.getElementById('questionModal'));
            this.questionModal.show();
        },
        async submitQuestion() {
            try {
                if (this.editingQuestion) {
                    await axios.put(`http://localhost:5000/api/questions/${this.editingQuestionId}`, this.questionForm, {
                        headers: {
                            'Authorization': `Bearer ${localStorage.getItem('token')}`
                        }
                    });
                } else {
                    await axios.post('http://localhost:5000/api/questions', this.questionForm, {
                        headers: {
                            'Authorization': `Bearer ${localStorage.getItem('token')}`
                        }
                    });
                }
                this.questionModal.hide();
                await this.getQuizzes();
            } catch (error) {
                console.error(error);
                alert(`Failed to ${this.editingQuestion ? 'update' : 'create'} question`);
            }
        },
        async deleteQuestion(questionId) {
            try {
                await axios.delete(`http://localhost:5000/api/questions/${questionId}`, {
                    headers: {
                        'Authorization': `Bearer ${localStorage.getItem('token')}`
                    }
                });
                await this.getQuizzes();
            } catch (error) {
                console.error(error);
            }
        },
        openCreateQuizModal() {
            this.quizModal = new bootstrap.Modal(document.getElementById('createQuizModal'));
            this.quizModal.show();
        },
        async createQuiz() {
            try {
                const formattedDate = new Date(this.quizForm.date_of_quiz).toISOString().slice(0, 10);
                await axios.post('http://localhost:5000/api/quizzes', {
                    chapter_id: parseInt(this.quizForm.chapter_id),
                    date_of_quiz: formattedDate,
                    time_duration: parseInt(this.quizForm.time_duration)
                }, {
                    headers: {
                        'Authorization': `Bearer ${localStorage.getItem('token')}`
                    }
                });
                this.quizModal.hide();
                this.resetForm();
                await this.getQuizzes();
            } catch (error) {
                console.error(error);
                alert('Failed to create quiz. Please try again.');
            }
        },
        resetForm() {
            this.quizForm = {
                chapter_id: '',
                date_of_quiz: '',
                time_duration: ''
            };
        },
        initializeModals() {
            this.createQuizModal = new bootstrap.Modal(document.getElementById('createQuizModal'));
            this.questionModal = new bootstrap.Modal(document.getElementById('questionModal'));
            this.quizDetailsModal = new bootstrap.Modal(document.getElementById('quizDetailsModal'));
        },
        viewQuizDetails(quiz) {
            this.selectedQuiz = quiz;
            this.quizDetailsModal.show();
        },
        methods: {
            getSubjectName(subjectId) {
                const subject = this.subjects.find(s => s.id === subjectId);
                return subject ? subject.name : 'N/A';
            },
            getChapterName(chapterId) {
                for (const subject of this.subjects) {
                    const chapter = subject.chapters.find(c => c.id === chapterId);
                    if (chapter) return chapter.name;
                }
                return 'N/A';
            },
            formatDate(dateString) {
                return new Date(dateString).toLocaleDateString();
            },
        },
        logout() {
            localStorage.removeItem('token');
            this.$router.push('/login');
        },
        async getQuizzes() {
            try {
                const QuizResponse = await axios.get('http://localhost:5000/api/quizzes', {
                    headers: {
                        'Authorization': `Bearer ${localStorage.getItem('token')}`
                    }
                });
                this.quizzes = QuizResponse.data.quizzes;
            } catch (error) {
                console.error(error);
            }
        },
        async editQuestion(questionId) {
            try {
                const response = await axios.get(`http://localhost:5000/api/questions/${questionId}`, {
                    headers: {
                        'Authorization': `Bearer ${localStorage.getItem('token')}`
                    }
                });
                const question = response.data;
                this.questionForm = {
                    quiz_id: question.quiz_id,
                    question_statement: question.question_statement,
                    option1: question.options[0],
                    option2: question.options[1],
                    option3: question.options[2],
                    option4: question.options[3],
                    correct_answer: question.correct_answer
                };
                this.editingQuestion = true;
                this.editingQuestionId = questionId;
                this.questionModal = new bootstrap.Modal(document.getElementById('questionModal'));
                this.questionModal.show();
            } catch (error) {
                console.error(error);
                alert('Failed to load question details');
            }
        },
        addQuestion(quizId) {
            this.questionForm = {
                quiz_id: quizId,
                question_statement: '',
                option1: '',
                option2: '',
                option3: '',
                option4: '',
                correct_answer: ''
            };
            this.editingQuestion = false;
            this.editingQuestionId = null;
            this.questionModal = new bootstrap.Modal(document.getElementById('questionModal'));
            this.questionModal.show();
        },
        async submitQuestion() {
            try {
                if (this.editingQuestion) {
                    await axios.put(`http://localhost:5000/api/questions/${this.editingQuestionId}`, this.questionForm, {
                        headers: {
                            'Authorization': `Bearer ${localStorage.getItem('token')}`
                        }
                    });
                } else {
                    await axios.post('http://localhost:5000/api/questions', this.questionForm, {
                        headers: {
                            'Authorization': `Bearer ${localStorage.getItem('token')}`
                        }
                    });
                }
                this.questionModal.hide();
                await this.getQuizzes();
            } catch (error) {
                console.error(error);
                alert(`Failed to ${this.editingQuestion ? 'update' : 'create'} question`);
            }
        },
        async deleteQuestion(questionId) {
            try {
                await axios.delete(`http://localhost:5000/api/questions/${questionId}`, {
                    headers: {
                        'Authorization': `Bearer ${localStorage.getItem('token')}`
                    }
                });
                await this.getQuizzes();
            } catch (error) {
                console.error(error);
            }
        },
        openCreateQuizModal() {
            this.quizModal = new bootstrap.Modal(document.getElementById('createQuizModal'));
            this.quizModal.show();
        },
        async createQuiz() {
            try {
                const formattedDate = new Date(this.quizForm.date_of_quiz).toISOString().slice(0, 10);
                await axios.post('http://localhost:5000/api/quizzes', {
                    chapter_id: parseInt(this.quizForm.chapter_id),
                    date_of_quiz: formattedDate,
                    time_duration: parseInt(this.quizForm.time_duration)
                }, {
                    headers: {
                        'Authorization': `Bearer ${localStorage.getItem('token')}`
                    }
                });
                this.quizModal.hide();
                this.resetForm();
                await this.getQuizzes();
            } catch (error) {
                console.error(error);
                alert('Failed to create quiz. Please try again.');
            }
        },
        resetForm() {
            this.quizForm = {
                chapter_id: '',
                date_of_quiz: '',
                time_duration: ''
            };
        },
        initializeModals() {
            this.createQuizModal = new bootstrap.Modal(document.getElementById('createQuizModal'));
            this.questionModal = new bootstrap.Modal(document.getElementById('questionModal'));
            this.quizDetailsModal = new bootstrap.Modal(document.getElementById('quizDetailsModal'));
        },
        viewQuizDetails(quiz) {
            this.selectedQuiz = quiz;
            this.quizDetailsModal.show();
        },
        formatDate(dateString) {
            return new Date(dateString).toLocaleString();
        },
        logout() {
            localStorage.removeItem('token');
            this.$router.push('/login');
        },
        async getQuizzes() {
            try {
                const QuizResponse = await axios.get('http://localhost:5000/api/quizzes', {
                    headers: {
                        'Authorization': `Bearer ${localStorage.getItem('token')}`
                    }
                });
                this.quizzes = QuizResponse.data.quizzes;
            } catch (error) {
                console.error(error);
            }
        },
        async editQuestion(questionId) {
            try {
                const response = await axios.get(`http://localhost:5000/api/questions/${questionId}`, {
                    headers: {
                        'Authorization': `Bearer ${localStorage.getItem('token')}`
                    }
                });
                const question = response.data;
                this.questionForm = {
                    quiz_id: question.quiz_id,
                    question_statement: question.question_statement,
                    option1: question.options[0],
                    option2: question.options[1],
                    option3: question.options[2],
                    option4: question.options[3],
                    correct_answer: question.correct_answer
                };
                this.editingQuestion = true;
                this.editingQuestionId = questionId;
                this.questionModal = new bootstrap.Modal(document.getElementById('questionModal'));
                this.questionModal.show();
            } catch (error) {
                console.error(error);
                alert('Failed to load question details');
            }
        },
        addQuestion(quizId) {
            this.questionForm = {
                quiz_id: quizId,
                question_statement: '',
                option1: '',
                option2: '',
                option3: '',
                option4: '',
                correct_answer: ''
            };
            this.editingQuestion = false;
            this.editingQuestionId = null;
            this.questionModal = new bootstrap.Modal(document.getElementById('questionModal'));
            this.questionModal.show();
        },
        async submitQuestion() {
            try {
                if (this.editingQuestion) {
                    await axios.put(`http://localhost:5000/api/questions/${this.editingQuestionId}`, this.questionForm, {
                        headers: {
                            'Authorization': `Bearer ${localStorage.getItem('token')}`
                        }
                    });
                } else {
                    await axios.post('http://localhost:5000/api/questions', this.questionForm, {
                        headers: {
                            'Authorization': `Bearer ${localStorage.getItem('token')}`
                        }
                    });
                }
                this.questionModal.hide();
                await this.getQuizzes();
            } catch (error) {
                console.error(error);
                alert(`Failed to ${this.editingQuestion ? 'update' : 'create'} question`);
            }
        },
        async deleteQuestion(questionId) {
            try {
                await axios.delete(`http://localhost:5000/api/questions/${questionId}`, {
                    headers: {
                        'Authorization': `Bearer ${localStorage.getItem('token')}`
                    }
                });
                await this.getQuizzes();
            } catch (error) {
                console.error(error);
            }
        },
        openCreateQuizModal() {
            this.quizModal = new bootstrap.Modal(document.getElementById('createQuizModal'));
            this.quizModal.show();
        },
        async createQuiz() {
            try {
                const formattedDate = new Date(this.quizForm.date_of_quiz).toISOString().slice(0, 10);
                await axios.post('http://localhost:5000/api/quizzes', {
                    chapter_id: parseInt(this.quizForm.chapter_id),
                    date_of_quiz: formattedDate,
                    time_duration: parseInt(this.quizForm.time_duration)
                }, {
                    headers: {
                        'Authorization': `Bearer ${localStorage.getItem('token')}`
                    }
                });
                this.quizModal.hide();
                this.resetForm();
                await this.getQuizzes();
            } catch (error) {
                console.error(error);
                alert('Failed to create quiz. Please try again.');
            }
        },
        resetForm() {
            this.quizForm = {
                chapter_id: '',
                date_of_quiz: '',
                time_duration: ''
            };
        },
        initializeModals() {
            this.createQuizModal = new bootstrap.Modal(document.getElementById('createQuizModal'));
            this.questionModal = new bootstrap.Modal(document.getElementById('questionModal'));
            this.quizDetailsModal = new bootstrap.Modal(document.getElementById('quizDetailsModal'));
        },
        viewQuizDetails(quiz) {
            this.selectedQuiz = quiz;
            this.quizDetailsModal.show();
        },
        formatDate(dateString) {
            return new Date(dateString).toLocaleString();
        },
        logout() {
            localStorage.removeItem('token');
            this.$router.push('/login');
        },
        async getQuizzes() {
            try {
                const QuizResponse = await axios.get('http://localhost:5000/api/quizzes', {
                    headers: {
                        'Authorization': `Bearer ${localStorage.getItem('token')}`
                    }
                });
                this.quizzes = QuizResponse.data.quizzes;
            } catch (error) {
                console.error(error);
            }
        },
        async editQuestion(questionId) {
            try {
                const response = await axios.get(`http://localhost:5000/api/questions/${questionId}`, {
                    headers: {
                        'Authorization': `Bearer ${localStorage.getItem('token')}`
                    }
                });
                const question = response.data;
                this.questionForm = {
                    quiz_id: question.quiz_id,
                    question_statement: question.question_statement,
                    option1: question.options[0],
                    option2: question.options[1],
                    option3: question.options[2],
                    option4: question.options[3],
                    correct_answer: question.correct_answer
                };
                this.editingQuestion = true;
                this.editingQuestionId = questionId;
                this.questionModal = new bootstrap.Modal(document.getElementById('questionModal'));
                this.questionModal.show();
            } catch (error) {
                console.error(error);
                alert('Failed to load question details');
            }
        },
        addQuestion(quizId) {
            this.questionForm = {
                quiz_id: quizId,
                question_statement: '',
                option1: '',
                option2: '',
                option3: '',
                option4: '',
                correct_answer: ''
            };
            this.editingQuestion = false;
            this.editingQuestionId = null;
            this.questionModal = new bootstrap.Modal(document.getElementById('questionModal'));
            this.questionModal.show();
        },
        async submitQuestion() {
            try {
                if (this.editingQuestion) {
                    await axios.put(`http://localhost:5000/api/questions/${this.editingQuestionId}`, this.questionForm, {
                        headers: {
                            'Authorization': `Bearer ${localStorage.getItem('token')}`
                        }
                    });
                } else {
                    await axios.post('http://localhost:5000/api/questions', this.questionForm, {
                        headers: {
                            'Authorization': `Bearer ${localStorage.getItem('token')}`
                        }
                    });
                }
                this.questionModal.hide();
                await this.getQuizzes();
            } catch (error) {
                console.error(error);
                alert(`Failed to ${this.editingQuestion ? 'update' : 'create'} question`);
            }
        },
        async deleteQuestion(questionId) {
            try {
                await axios.delete(`http://localhost:5000/api/questions/${questionId}`, {
                    headers: {
                        'Authorization': `Bearer ${localStorage.getItem('token')}`
                    }
                });
                await this.getQuizzes();
            } catch (error) {
                console.error(error);
            }
        },
        openCreateQuizModal() {
            this.quizModal = new bootstrap.Modal(document.getElementById('createQuizModal'));
            this.quizModal.show();
        },
        async createQuiz() {
            try {
                const formattedDate = new Date(this.quizForm.date_of_quiz).toISOString().slice(0, 10);
                await axios.post('http://localhost:5000/api/quizzes', {
                    chapter_id: parseInt(this.quizForm.chapter_id),
                    date_of_quiz: formattedDate,
                    time_duration: parseInt(this.quizForm.time_duration)
                }, {
                    headers: {
                        'Authorization': `Bearer ${localStorage.getItem('token')}`
                    }
                });
                this.quizModal.hide();
                this.resetForm();
                await this.getQuizzes();
            } catch (error) {
                console.error(error);
                alert('Failed to create quiz. Please try again.');
            }
        },
        resetForm() {
            this.quizForm = {
                chapter_id: '',
                date_of_quiz: '',
                time_duration: ''
            };
        }
    },
};
</script>

<style scoped>
.card {
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.table {
    margin-bottom: 0;
}

.btn-sm {
    padding: 0.25rem 0.5rem;
    font-size: 0.875rem;
}
</style>