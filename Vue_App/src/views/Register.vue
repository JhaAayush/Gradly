<template>
  <div class="flex items-center justify-center min-h-[calc(100vh-var(--navbar-height)-var(--footer-height))]">
    <div class="max-w-lg w-full bg-white/70 backdrop-blur-lg p-8 rounded-2xl shadow-2xl border border-slate-200">
        <div class="text-center mb-8">
            <h2 class="text-3xl font-extrabold text-slate-800 flex items-center justify-center gap-3">
                <i class="fa fa-user-plus text-sky-500"></i> Create Your Account
            </h2>
            <p class="text-slate-500 mt-2">Join Gradly and take control of your academic journey.</p>
        </div>
        <form @submit.prevent="handleSubmit" class="space-y-6">
            <div>
                <label for="roll_number" class="block text-sm font-semibold text-slate-600 mb-2">Roll Number</label>
                <div class="relative">
                    <i class="fa fa-hashtag absolute left-4 top-1/2 -translate-y-1/2 text-slate-400"></i>
                    <input
                        id="roll_number"
                        v-model="form.roll_number"
                        type="text"
                        class="w-full pl-12 pr-4 py-3 bg-slate-100 border-transparent rounded-lg focus:ring-2 focus:ring-sky-500 transition placeholder-slate-400"
                        placeholder="MBA10XXX or MBABA04XXX or MBAHR04XXX"
                        required
                    />
                </div>
            </div>
            <div>
                <label for="name" class="block text-sm font-semibold text-slate-600 mb-2">Full Name</label>
                <div class="relative">
                    <i class="fa fa-signature absolute left-4 top-1/2 -translate-y-1/2 text-slate-400"></i>
                    <input
                        id="name"
                        v-model="form.name"
                        type="text"
                        class="w-full pl-12 pr-4 py-3 bg-slate-100 border-transparent rounded-lg focus:ring-2 focus:ring-sky-500 transition placeholder-slate-400"
                        placeholder="Your Full Name"
                        required
                    />
                </div>
            </div>
            <div>
                <label for="email" class="block text-sm font-semibold text-slate-600 mb-2">Email Address</label>
                <div class="relative">
                    <i class="fa fa-at absolute left-4 top-1/2 -translate-y-1/2 text-slate-400"></i>
                    <input
                        id="email"
                        v-model="form.email"
                        type="email"
                        class="w-full pl-12 pr-4 py-3 bg-slate-100 border-transparent rounded-lg focus:ring-2 focus:ring-sky-500 transition placeholder-slate-400"
                        placeholder="Your College Email"
                        required
                    />
                </div>
            </div>
            <div>
                <label for="password" class="block text-sm font-semibold text-slate-600 mb-2">Password</label>
                <div class="relative">
                    <i class="fa fa-key absolute left-4 top-1/2 -translate-y-1/2 text-slate-400"></i>
                    <input
                        id="password"
                        v-model="form.password"
                        :type="passwordVisible ? 'text' : 'password'"
                        class="w-full pl-12 pr-4 py-3 bg-slate-100 border-transparent rounded-lg focus:ring-2 focus:ring-sky-500 transition"
                        placeholder="Create a strong password"
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
                class="w-full bg-sky-500 text-white px-6 py-3 rounded-lg font-semibold text-lg hover:bg-sky-600 transition-all duration-300 transform hover:scale-105 shadow-md">
                Register <i class="fa fa-user-plus ml-2"></i>
            </button>
            <p class="text-center text-sm text-slate-600 mt-4">
                Already have an account? <router-link to="/login" class="text-sky-600 hover:underline font-medium">Login here</router-link>
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
    roll_number: '',
    name: '',
    email: '',
    password: ''
})

const passwordVisible = ref(false)

const togglePassword = () => {
    passwordVisible.value = !passwordVisible.value
}

const handleSubmit = () => {
    console.log('Register attempt with:', form)
    router.push('/login')
}
</script>
