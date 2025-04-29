<template>

    <BlogHeader/>


    <ArticleList/>

    <BlogFooter/>

</template>

<script>
    import BlogHeader from '@/components/BlogHeader.vue'
    import BlogFooter from '@/components/BlogFooter.vue'
    import ArticleList from '@/components/ArticleList.vue'
    import { ref, onMounted } from 'vue'
    import axios from 'axios'

    export default {
        name: 'Home',
        components: {BlogHeader, BlogFooter, ArticleList},
        setup() {
            const pageVisitCount = ref(0);

            const getPageVisitCount = async () => {
                try {
                    const response = await axios.get('/api/visit-count/home/');
                    pageVisitCount.value = response.data.count;
                } catch (error) {
                    console.error('Error fetching page visit count:', error);
                    pageVisitCount.value = 0;
                }
            };

            onMounted(() => {
                getPageVisitCount();
            });

            return {
                pageVisitCount
            }
        }
    }
</script>

<style scoped>
.page-visit-counter-wrapper {
    width: 100%;
    padding: 10px 20px;
    box-sizing: border-box;
    display: flex;
    justify-content: flex-end;
    background: #fff;
    border-bottom: 1px solid #eee;
}

.page-visit-counter {
    text-align: right;
    padding: 5px 15px;
    font-size: 0.8em;
    color: #2e7d32;
    background: rgba(46, 125, 50, 0.1);
    border-radius: 12px;
    display: inline-flex;
    align-items: center;
    gap: 4px;
    font-family: 'Lora', serif;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.page-visit-counter i {
    font-size: 0.9em;
    color: #2e7d32;
}
</style>