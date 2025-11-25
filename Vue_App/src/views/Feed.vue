<template>
  <div class="bg-gray-50 min-h-screen">

    <header class="bg-white/80 backdrop-blur-lg border-b border-gray-200 sticky top-0 z-30 lg:hidden">
        <div class="max-w-7xl mx-auto px-4">
            <div class="flex justify-between items-center h-16">
                <div class="font-bold text-xl text-indigo-600">
                    CampusConnect
                </div>

                <button @click="navOpen = !navOpen" class="text-gray-600 hover:text-indigo-600">
                    <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"
                        xmlns="http://www.w3.org/2000/svg">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                            d="M4 6h16M4 12h16m-7 6h7"></path>
                    </svg>
                </button>
            </div>
        </div>
    </header>

    <div v-show="navOpen"
        class="fixed top-0 left-0 w-72 h-full bg-white shadow-lg z-50 overflow-y-auto lg:hidden transition-transform duration-300"
        :class="navOpen ? 'translate-x-0' : '-translate-x-full'"
    >

        <div class="p-5 text-center border-b">
            <div class="w-24 h-24 mx-auto relative">
                <img :src="currentUser.profilePic || '/src/assets/default-profile.png'" class="rounded-full w-full h-full object-cover">
                <span class="absolute bottom-1 right-1 w-4 h-4 bg-green-500 border-2 border-white rounded-full"></span>
            </div>
            <h2 class="mt-3 font-bold text-lg text-gray-800">{{ currentUser.name }}</h2>
            <p class="text-sm text-gray-500">Student</p>

            <component :is="currentUser.user_type === 'student' ? 'router-link' : 'router-link'"
                :to="currentUser.user_type === 'student' ? '/profile/' + currentUser.id : '/body-profile/' + currentUser.id"
                class="mt-4 inline-block bg-slate-800 text-white px-4 py-2 rounded-lg hover:bg-sky-500 font-medium text-sm">View Profile</component>
        </div>

        <nav class="p-4 space-y-2 border-b">
            <router-link to="/feed" class="flex items-center gap-3 px-3 py-2 rounded-lg bg-indigo-50 text-indigo-700 font-semibold">🏠 Feed</router-link>
            <router-link to="/events" class="flex items-center gap-3 px-3 py-2 rounded-lg text-gray-600 hover:bg-gray-100">📅 Events</router-link>
            <a href="#" class="flex items-center gap-3 px-3 py-2 rounded-lg text-gray-600 hover:bg-gray-100">👥 Student Bodies</a>
            <router-link to="/profile/edit" class="flex items-center gap-3 px-3 py-2 rounded-lg text-gray-600 hover:bg-gray-100">⚙️ Settings</router-link>
        </nav>

        <div class="p-5">
            <h3 class="font-semibold text-gray-800 text-lg mb-4">Upcoming Events</h3>
            <ul v-if="events.length" class="space-y-3">
                <li v-for="event in events" :key="event.id" class="flex gap-4 items-center">
                    <div class="bg-indigo-100 text-indigo-600 font-bold w-12 h-12 rounded-lg flex flex-col items-center justify-center">
                        <span>{{ formatMonth(event.date) }}</span>
                        <span>{{ formatDay(event.date) }}</span>
                    </div>
                    <div>
                        <p class="font-semibold text-gray-800">{{ event.title }}</p>
                        <p class="text-sm text-gray-500">{{ formatTime(event.date) }}</p>
                    </div>
                </li>
            </ul>
            <p v-else class="text-gray-500 text-sm">No upcoming events.</p>
        </div>
    </div>

    <div v-show="navOpen" @click="navOpen = false" class="fixed inset-0 bg-black/30 z-40 lg:hidden transition-opacity duration-300"></div>


    <div class="max-w-7xl mx-auto py-0 lg:py-6 grid grid-cols-1 lg:grid-cols-12 lg:gap-8">

        <aside class="hidden lg:block lg:col-span-3">
            <div class="sticky top-6 space-y-6">
                <div class="bg-white shadow rounded-xl p-5 text-center">
                    <div class="w-24 h-24 mx-auto relative">
                        <img :src="currentUser.profilePic || '/src/assets/default-profile.png'" class="rounded-full w-full h-full object-cover">
                        <span class="absolute bottom-1 right-1 w-4 h-4 bg-green-500 border-2 border-white rounded-full"></span>
                    </div>
                    <h2 class="mt-3 font-bold text-lg text-gray-800">{{ currentUser.name }}</h2>
                    <p class="text-sm text-gray-500">Student</p>

                    <component :is="currentUser.user_type === 'student' ? 'router-link' : 'router-link'"
                        :to="currentUser.user_type === 'student' ? '/profile/' + currentUser.id : '/body-profile/' + currentUser.id"
                        class="mt-4 inline-block bg-slate-800 text-white px-4 py-2 rounded-lg hover:bg-sky-500 font-medium text-sm">View Profile</component>
                </div>
                <div class="bg-white shadow rounded-xl p-4">
                    <nav class="space-y-2">
                        <router-link to="/feed" class="block px-3 py-2 rounded-lg bg-indigo-50 text-indigo-700 font-semibold">🏠 Feed</router-link>
                        <router-link to="/events" class="block px-3 py-2 rounded-lg text-gray-600 hover:bg-gray-100">📅 Events</router-link>
                        <a href="#" class="block px-3 py-2 rounded-lg text-gray-600 hover:bg-gray-100">👥 Student Bodies</a>
                        <router-link to="/profile/edit" class="block px-3 py-2 rounded-lg text-gray-600 hover:bg-gray-100">⚙️ Settings</router-link>
                    </nav>
                </div>
            </div>
        </aside>

        <main class="lg:col-span-6 space-y-0 lg:space-y-6">
            <div class="mb-6">
                <router-link to="/posts/create" class="w-full text-center block bg-slate-800 text-white px-4 py-3 rounded-lg shadow hover:bg-sky-500 font-medium transition-colors">
                    Create Post
                </router-link>
            </div>

            <div class="mb-6 bg-white shadow sm:rounded-lg p-2 flex space-x-2">
                <button @click="filter = 'all'" class="flex-1 text-center px-3 py-2 rounded-md font-medium text-sm transition-colors"
                    :class="filter === 'all' ? 'bg-slate-800 text-white shadow' : 'bg-white text-gray-700 hover:bg-gray-50'">
                    All Posts
                </button>
                <button @click="filter = 'student'" class="flex-1 text-center px-3 py-2 rounded-md font-medium text-sm transition-colors"
                    :class="filter === 'student' ? 'bg-slate-800 text-white shadow' : 'bg-white text-gray-700 hover:bg-gray-50'">
                    Student Posts
                </button>
                <button @click="filter = 'body'" class="flex-1 text-center px-3 py-2 rounded-md font-medium text-sm transition-colors"
                    :class="filter === 'body' ? 'bg-slate-800 text-white shadow' : 'bg-white text-gray-700 hover:bg-gray-50'">
                    Body Posts
                </button>
            </div>

            <div v-if="filteredPosts.length > 0">
                <div v-for="post in filteredPosts" :key="post.id" class="bg-white sm:rounded-2xl sm:shadow mb-6 lg:mb-0 border-b sm:border-none">

                    <div class="p-4 flex justify-between items-start gap-3">
                        <div class="flex items-center gap-3">
                            <img :src="post.author.profilePic || '/src/assets/default-profile.png'" class="w-10 h-10 rounded-full object-cover">
                            <div>
                                <component :is="post.author.user_type === 'student' ? 'router-link' : 'router-link'"
                                    :to="post.author.user_type === 'student' ? '/profile/' + post.author.id : '/body-profile/' + post.author.id"
                                    class="font-semibold text-gray-800 hover:underline">{{ post.author.name }}</component>
                                <p class="text-xs text-gray-500">{{ formatDate(post.created_at) }}</p>
                            </div>
                        </div>

                        <router-link v-if="post.author.id === currentUser.id" :to="'/posts/edit/' + post.id"
                            class="text-xs font-medium text-indigo-600 hover:text-indigo-800 bg-indigo-50 hover:bg-indigo-100 px-3 py-1 rounded-full flex-shrink-0">
                            Edit
                        </router-link>
                    </div>

                    <div class="p-4 pt-0">
                        <h2 class="text-lg font-semibold text-gray-800">{{ post.title }}</h2>
                    </div>

                    <img v-if="post.imageUrl" :src="post.imageUrl" class="w-full h-auto max-h-[80vh] object-cover">

                    <div class="p-4">
                        <div class="prose max-w-none text-gray-700" v-html="post.content"></div>

                        <div class="flex items-center mt-4 space-x-3">
                            <button @click="vote(post.id, 'upvote')" class="px-3 py-1 bg-green-100 text-green-700 rounded-lg hover:bg-green-200">⬆</button>
                            <span class="font-semibold text-gray-800">{{ post.voteScore }}</span>
                            <button @click="vote(post.id, 'downvote')" class="px-3 py-1 bg-red-100 text-red-700 rounded-lg hover:bg-red-200">⬇</button>
                        </div>

                        <div class="mt-5 border-t border-gray-100 pt-4">
                            <div class="space-y-2">
                                <div v-for="c in post.comments" :key="c.id" class="text-sm">
                                    <component :is="c.author.user_type === 'student' ? 'router-link' : 'router-link'"
                                        :to="c.author.user_type === 'student' ? '/profile/' + c.author.id : '/body-profile/' + c.author.id"
                                        class="font-medium text-indigo-600 hover:underline">{{ c.author.name }}</component>: {{ c.content }}
                                </div>
                            </div>

                            <form @submit.prevent="submitComment(post.id)" class="mt-4 flex items-center gap-2">
                                <img :src="currentUser.profilePic || '/src/assets/default-profile.png'" class="w-8 h-8 rounded-full object-cover hidden sm:block">
                                <input v-model="newComments[post.id]" type="text" placeholder="Add a comment..."
                                    class="w-full border border-gray-300 rounded-full bg-gray-50 px-4 py-2 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none text-sm transition-colors"
                                    required>
                                <button type="submit" class="hidden">Post</button>
                            </form>
                        </div>
                    </div>
                </div>
            </div>
            <div v-else class="text-center py-20 bg-white shadow rounded-xl">
                <h2 class="text-2xl font-bold text-gray-600">No posts yet!</h2>
                <p class="text-gray-500">The feed is empty.
                    <span v-if="filter !== 'all'">Try selecting "All Posts".</span>
                    <span v-else>Check back later for updates.</span>
                </p>
            </div>
        </main>

        <aside class="hidden lg:block lg:col-span-3">
            <div class="sticky top-6 space-y-6">
                <div class="bg-white shadow rounded-xl p-5">
                    <h3 class="font-semibold text-gray-800 text-lg mb-4">Upcoming Events</h3>
                    <ul v-if="events.length" class="space-y-3">
                        <li v-for="event in events" :key="event.id" class="flex gap-4 items-center">
                            <div class="bg-indigo-100 text-indigo-600 font-bold w-12 h-12 rounded-lg flex flex-col items-center justify-center">
                                <span>{{ formatMonth(event.date) }}</span>
                                <span>{{ formatDay(event.date) }}</span>
                            </div>
                            <div>
                                <p class="font-semibold text-gray-800">{{ event.title }}</p>
                                <p class="text-sm text-gray-500">{{ formatTime(event.date) }}</p>
                            </div>
                        </li>
                    </ul>
                    <p v-else class="text-gray-500 text-sm">No upcoming events.</p>
                </div>
                <div class="bg-white shadow rounded-xl p-5">
                    <h3 class="font-semibold text-gray-800 text-lg mb-4">Quick Links</h3>
                    <ul class="space-y-2">
                        <li>
                            <router-link :to="currentUser.user_type === 'student' ? '/profile/' + currentUser.id : '/body-profile/' + currentUser.id"
                                class="text-indigo-600 hover:underline">My Profile</router-link>
                        </li>
                        <li><router-link to="/events" class="text-indigo-600 hover:underline">All Events</router-link></li>
                        <li><a href="#" class="text-indigo-600 hover:underline">Student Bodies</a></li>
                    </ul>
                </div>
            </div>
        </aside>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref, computed } from 'vue'

const navOpen = ref(false)
const filter = ref('all')
const newComments = reactive({})

// Mock Current User
const currentUser = reactive({
    id: 1,
    name: 'Test User',
    user_type: 'student',
    profilePic: null
})

// Mock Events
const events = ref([
    { id: 1, title: 'Annual Tech Fest', date: '2023-11-15T14:00:00' }
])

// Mock Posts
const posts = ref([
    {
        id: 1,
        author: { id: 1, name: 'Test User', user_type: 'student', profilePic: null },
        created_at: '2023-10-22',
        title: 'Welcome to Gradly!',
        content: '<p>This is the first post.</p>',
        imageUrl: null,
        voteScore: 5,
        comments: [
            { id: 1, author: { id: 2, name: 'Jane Doe', user_type: 'student' }, content: 'Great platform!' }
        ]
    }
])

const filteredPosts = computed(() => {
    if (filter.value === 'all') return posts.value
    // Add logic for student/body filtering based on author type if needed
    if (filter.value === 'student') return posts.value.filter(p => p.author.user_type === 'student')
    if (filter.value === 'body') return posts.value.filter(p => p.author.user_type === 'body')
    return posts.value
})

const vote = (postId, action) => {
    const post = posts.value.find(p => p.id === postId)
    if (post) {
        if (action === 'upvote') post.voteScore++
        else post.voteScore--
    }
}

const submitComment = (postId) => {
    const commentText = newComments[postId]
    if (!commentText) return

    const post = posts.value.find(p => p.id === postId)
    if (post) {
        post.comments.push({
            id: Date.now(),
            author: currentUser,
            content: commentText
        })
        newComments[postId] = ''
    }
}

const formatMonth = (dateString) => new Date(dateString).toLocaleDateString('en-US', { month: 'short' })
const formatDay = (dateString) => new Date(dateString).getDate()
const formatTime = (dateString) => new Date(dateString).toLocaleTimeString('en-US', { hour: 'numeric', minute: '2-digit' })
const formatDate = (dateString) => new Date(dateString).toLocaleDateString('en-US', { month: 'long', day: 'numeric', year: 'numeric' })

</script>
