import axios from 'axios';
import {onMounted, watch} from 'vue'

// 配置 API 基础 URL
const API_BASE_URL = '/api';  // 使用相对路径，让 Nginx 处理代理

export default function getArticleData(info, route, kwargs) {
    const getData = async () => {
        const queryPage = route.query.page !== undefined ? parseInt(route.query.page) : 1;
        if (
            kwargs.value.page === queryPage && 
            kwargs.value.searchText === route.query.search &&
            kwargs.value.tag === route.query.tag &&
            kwargs.value.category === route.query.category
        ) {
            return
        }

        // 使用相对路径
        let url = `${API_BASE_URL}/article/`;

        let params = new URLSearchParams();
        
        // 添加分页和搜索参数
        if (route.query.page) params.append('page', route.query.page);
        if (route.query.search) params.append('search', route.query.search);
        
        // 添加标签和分类过滤参数
        if (route.query.tag) params.append('tag', route.query.tag);
        if (route.query.category) params.append('category', route.query.category);

        const paramsString = params.toString();
        if (paramsString) {
            url += '?' + paramsString;
        }

        try {
            console.log('Fetching articles from:', url);
            const response = await axios.get(url);
            console.log('Response:', response.data);
            info.value = response.data;
            
            // 更新所有查询参数的状态
            kwargs.value.page = queryPage;
            kwargs.value.searchText = route.query.search;
            kwargs.value.tag = route.query.tag;
            kwargs.value.category = route.query.category;
        } catch (error) {
            console.error('Error fetching articles:', error);
            if (error.response) {
                console.error('Response status:', error.response.status);
                console.error('Response data:', error.response.data);
            }
        }
    };

    onMounted(getData);

    watch(route, getData);
}