<template>
  <div class="flex items-center justify-center min-h-[calc(100vh-var(--navbar-height)-var(--footer-height))]">
    <div class="max-w-md w-full bg-white/70 backdrop-blur-lg p-8 rounded-2xl shadow-2xl border border-slate-200">
        <div class="text-center mb-8">
            <h2 class="text-3xl font-extrabold text-slate-800 flex items-center justify-center gap-3">
                <i class="fa fa-door-open text-sky-500"></i> Welcome Back
            </h2>
            <p class="text-slate-500 mt-2">Sign in to continue your Gradly journey.</p>
        </div>
        <form @submit.prevent="handleSubmit" class="space-y-6">
            <div>
                <label for="email_or_roll" class="block text-sm font-semibold text-slate-600 mb-2">Email or Roll Number</label>
                <div class="relative">
                    <i class="fa fa-user absolute left-4 top-1/2 -translate-y-1/2 text-slate-400"></i>
                    <input
                        id="email_or_roll"
                        v-model="form.email_or_roll"
                        type="text"
                        class="w-full pl-12 pr-4 py-3 bg-slate-100 border-transparent rounded-lg focus:ring-2 focus:ring-sky-500 transition placeholder-slate-400"
                        placeholder="MBAYYXXX or College Email"
                        required
                    />
                </div>
            </div>
            <div>
                <label for="password" class="block text-sm font-semibold text-slate-600 mb-2">Password</label>
                <div class="relative">
                    <i class="fa fa-lock absolute left-4 top-1/2 -translate-y-1/2 text-slate-400"></i>
                    <input
                        id="password"
                        v-model="form.password"
                        :type="passwordVisible ? 'text' : 'password'"
                        class="w-full pl-12 pr-4 py-3 bg-slate-100 border-transparent rounded-lg focus:ring-2 focus:ring-sky-500 transition"
                        placeholder="Your password"
                        required
                    />
                    <i
                        class="fa absolute right-4 top-1/2 -translate-y-1/2 text-slate-400 cursor-pointer"
                        :class="passwordVisible ? 'fa-eye-slash' : 'fa-eye'"
                        @click="togglePassword"
                    ></i>
                </div>
            </div>
            <button type="submit"
                class="w-full bg-slate-800 text-white px-6 py-3 rounded-lg font-semibold text-lg hover:bg-sky-500 transition-all duration-300 transform hover:scale-105 shadow-md">
                Login <i class="fa fa-sign-in-alt ml-2"></i>
            </button>
            <p class="text-center text-sm text-slate-600 mt-4">
                Don't have an account? <router-link to="/register" class="text-sky-600 hover:underline font-medium">Register here</router-link>
            </p>
            <p class="text-center text-sm text-slate-600 mt-2">
                Are you a Student Body? <router-link to="/body-login" class="text-sky-600 hover:underline font-medium">Login here</router-link>
            </p>

        </form>
    </div>
</div>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const form = reactive({
    email_or_roll: '',
    password: ''
})

const passwordVisible = ref(false)

const togglePassword = () => {
    passwordVisible.value = !passwordVisible.value
}

const handleSubmit = () => {
    // Mock login logic
    console.log('Login attempt with:', form)
    // Redirect to home/dashboard on success
    router.push('/')
}
</script>
