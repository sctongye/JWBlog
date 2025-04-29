<template>
    <div id="header">
        <div class="grid">
            <div></div>
            <div class="title-container">
                <router-link to="/" class="title-link">
                    <h1>JW Blog</h1>
                    <img src="@/assets/jwlogo2sm.png" alt="JW Logo" class="logo">
                </router-link>
                <div class="social-icons">
                    <a href="https://www.instagram.com/sarsywang" target="_blank" rel="noopener noreferrer" class="social-icon instagram">
                        <i class="fab fa-instagram"></i>
                    </a>
                    <a href="https://x.com/JiayuWang" target="_blank" rel="noopener noreferrer" class="social-icon twitter">
                        <i class="fab fa-twitter"></i>
                    </a>
                    <a href="https://www.youtube.com/@tongye" target="_blank" rel="noopener noreferrer" class="social-icon youtube">
                        <i class="fab fa-youtube"></i>
                    </a>
                </div>
            </div>
            <!--引入搜索框组件-->
            <!-- <SearchButton/> -->
        </div>
        <hr>
        <div class="login">
            <div class="nav-links">
                <router-link to="/" class="nav-link" v-if="$route.name !== 'Home'">&lt;&lt; Back to Blog List</router-link>
                <div class="right-links">
                    <div v-if="hasLogin">
                        <div class="dropdown">
                            <button class="dropbtn">欢迎, {{username}}!</button>
                            <div class="dropdown-content">
                                <a href="http://wangjiayu.com" class="home-link">Home</a>
                                <router-link :to="{ name: 'UserCenter', params: { username: username }}">用户中心</router-link>
                                <router-link :to="{ name: 'ArticleCreate' }" v-if="isSuperuser">发表文章</router-link>
                                <router-link to="/" v-on:click.prevent="logout()">Logout</router-link>
                            </div>
                        </div>
                    </div>
                    <div v-else>
                        <a href="http://wangjiayu.com" class="home-link">Home</a>
                        <router-link to="/login" class="login-link">Login</router-link>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    // import SearchButton from '@/components/SearchButton.vue';
    import authorization from '@/utils/authorization';

    export default {
        name: 'BlogHeader',
        // components: {SearchButton},
        data: function () {
            return {
                username: '',
                hasLogin: false,
                isSuperuser: JSON.parse(localStorage.getItem('isSuperuser.myblog')),
            }
        },
        mounted() {
            authorization().then((data) => [this.hasLogin, this.username] = data);
        },
        methods: {
            logout() {
                localStorage.clear();
                window.location.reload(false);
            },
            refresh() {
                this.username = localStorage.getItem('username.myblog');
            }
        }
    }
</script>

<style scoped>
    /*样式来源: https://www.runoob.com/css/css-dropdowns.html*/
    /* 下拉按钮样式 */
    .dropbtn {
        background-color: mediumslateblue;
        color: white;
        padding: 8px 8px 30px 8px;
        font-size: 16px;
        border: none;
        cursor: pointer;
        height: 16px;
        border-radius: 5px;
    }

    /* 容器 <div> - 需要定位下拉内容 */
    .dropdown {
        position: relative;
        display: inline-block;
    }

    /* 下拉内容 (默认隐藏) */
    .dropdown-content {
        display: none;
        position: absolute;
        background-color: #f9f9f9;
        min-width: 120px;
        box-shadow: 0 8px 16px 0 rgba(0, 0, 0, 0.2);
        text-align: center;
    }

    /* 下拉菜单的链接 */
    .dropdown-content a {
        color: black;
        padding: 12px 16px;
        text-decoration: none;
        display: block;
    }

    /* 鼠标移上去后修改下拉菜单链接颜色 */
    .dropdown-content a:hover {
        background-color: #f1f1f1
    }

    /* 在鼠标移上去后显示下拉菜单 */
    .dropdown:hover .dropdown-content {
        display: block;
    }

    /* 当下拉内容显示后修改下拉按钮的背景颜色 */
    .dropdown:hover .dropbtn {
        background-color: darkslateblue;
    }
</style>

<style scoped>
    .login-link {
        color: black;
        margin-left: 15px;
    }

    .home-link {
        color: black;
        text-decoration: none;
    }

    .nav-link {
        color: #666;
        text-decoration: none;
        font-family: 'Lora', serif;
        font-size: 0.9em;
        transition: color 0.3s ease;
    }

    .nav-link:hover {
        color: #000;
    }

    .title-link {
        text-decoration: none;
        color: inherit;
        display: flex;
        align-items: center;
        gap: 10px;
    }

    .title-link:hover {
        opacity: 0.8;
    }

    .login {
        padding: 0 5px;
    }

    .nav-links {
        display: flex;
        justify-content: space-between;
        align-items: center;
        width: 100%;
    }

    .right-links {
        display: flex;
        align-items: center;
        margin-left: auto;
    }

    #header {
        text-align: center;
        margin-top: 20px;
    }

    .grid {
        display: grid;
        grid-template-columns: 1fr 4fr 1fr;
    }

    .title-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        gap: 10px;
    }

    .logo {
        width: 60px;
        height: 60px;
        border-radius: 50%;
        object-fit: cover;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
    }

    .social-icons {
        display: flex;
        gap: 15px;
        align-items: center;
        /* margin-top: 1px; */
        margin-bottom: 2px;
    }

    .social-icon {
        font-size: 30px;
        transition: color 0.3s ease;
        text-decoration: none;
    }

    .social-icon.instagram {
        color: #E1306C;
    }

    .social-icon.twitter {
        color: #1DA1F2;
    }

    .social-icon.youtube {
        color: #FF0000;
    }

    .social-icon:hover {
        opacity: 0.8;
    }
</style>