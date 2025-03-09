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

    
</template>

<script>
export default {
    name: 'AdminSummary',
    data() {
        return {}
    }
}
</script>