<template>
    <BlogHeader />

    <div v-if="article !== null" class="grid-container">
        <div>
            <h1 id="title">{{ article.title }}</h1>
            <p id="subtitle">
                Published on {{ formatted_time(article.created) }}
                <span v-if="isSuperuser">
                    <router-link
                        :to="{
                            name: 'ArticleEdit',
                            params: { id: article.id },
                        }"
                        >更新与删除</router-link
                    >
                </span>
            </p>
            <div v-html="article.body_html" class="article-body"></div>
        </div>
        <div v-if="hasToc">
            <h3>目录</h3>
            <div v-html="article.toc_html" class="toc"></div>
        </div>
    </div>

    <Comments :article="article" />

    <div class="visit-counter">
        <i class="fas fa-eye"></i> 访问量：{{ visitCount }}
    </div>

    <BlogFooter />
</template>

<script>
import BlogHeader from '@/components/BlogHeader.vue';
import BlogFooter from '@/components/BlogFooter.vue';
import Comments from '@/components/Comments.vue';
import authorization from '@/utils/authorization';
import axios from 'axios';
import hljs from 'highlight.js';
import 'highlight.js/styles/atom-one-dark.css';

export default {
    name: 'ArticleDetail',
    components: { BlogHeader, BlogFooter, Comments },
    data: function () {
        return {
            article: null,
            hasLogin: false,
            visitCount: 0,
        };
    },
    mounted() {
        authorization().then((data) => ([this.hasLogin, this.username] = data));
        axios.get('/api/article/' + this.$route.params.id).then((response) => {
            this.article = response.data;
            this.$nextTick(() => {
                // 在内容渲染后应用代码高亮
                document.querySelectorAll('pre code').forEach((block) => {
                    hljs.highlightBlock(block);
                });
            });
        });
        this.getVisitCount();
    },
    methods: {
        formatted_time: function (iso_date_string) {
            const date = new Date(iso_date_string);
            return date.toLocaleDateString('en-US', {
                year: 'numeric',
                month: 'long',
                day: 'numeric',
            });
        },

        getVisitCount() {
            const articleId = this.$route.params.id;
            console.log('Fetching visit count for article:', articleId); // 添加调试日志
            axios.get(`/api/visit-count/article/${articleId}/`).then((response) => {
                console.log('Visit count response:', response.data); // 添加调试日志
                this.visitCount = response.data.count;
            }).catch(error => {
                console.error('Error fetching visit count:', error);
                console.error('Error details:', error.response); // 添加更多错误信息
                this.visitCount = 0;
            });
        },
    },
    computed: {
        isSuperuser() {
            return localStorage.getItem('isSuperuser.myblog') === 'true';
        },
        hasToc() {
            if (!this.article || !this.article.toc_html) return false;
            // 移除所有HTML标签和空白字符后检查是否还有内容
            const content = this.article.toc_html
                .replace(/<[^>]+>/g, '')
                .trim();
            return content.length > 0;
        },
    },
};
</script>

<style scoped>
.grid-container {
    display: grid;
    grid-template-columns: 3fr 1fr;
}

#title {
    text-align: center;
    font-size: x-large;
    font-family: 'Roboto', sans-serif;
}

#subtitle {
    text-align: center;
    color: gray;
    font-size: small;
    font-family: 'Lora', serif;
}
</style>

<style>
.article-body {
    font-family: 'Lora', serif;
}

.article-body p img {
    max-width: 100%;
    border-radius: 10px;
    box-shadow: gray 0 0 10px;
    margin-top: 10px;
    margin-bottom: 10px;
}

/* 代码块样式 */
.article-body pre {
    background-color: #282c34;
    border-radius: 6px;
    padding: 16px;
    overflow: auto;
    margin: 16px 0;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.article-body code {
    font-family: 'Fira Code', 'Consolas', 'Monaco', monospace;
    font-size: 14px;
    line-height: 1.5;
    color: #abb2bf;
}

/* 行内代码样式 */
.article-body p code {
    background-color: #282c34;
    color: #abb2bf;
    padding: 2px 6px;
    border-radius: 3px;
    font-size: 0.9em;
}

.toc ul {
    list-style-type: none;
    font-family: 'Lora', serif;
}

.toc a {
    color: gray;
}

/* 添加全局英文字体设置 */
body {
    font-family: 'Lora', serif;
}
</style>
