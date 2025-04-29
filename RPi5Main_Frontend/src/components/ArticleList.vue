<template>
  <div class="page-layout">
    <!-- Main Content -->
    <div class="main-content">


      <div v-for="article in info.results" v-bind:key="article.url" id="articles">
        <div class="grid" :style="gridStyle(article)">
          <div class="image-container" v-if="imageIfExists(article)">
            <router-link
              :to="{ name: 'ArticleDetail', params: { id: article.id } }"
            >
              <img :src="imageIfExists(article)" alt="" class="image" />
            </router-link>
          </div>

          <div class="content-container">
            <div>
              <span v-if="article.category !== null" class="category">
                {{ article.category.title }}
              </span>
              <span v-for="tag in article.tags" v-bind:key="tag" class="tag">{{
                tag
              }}</span>
            </div>
            <div class="a-title-container">
              <router-link
                :to="{ name: 'ArticleDetail', params: { id: article.id } }"
                class="article-title"
              >
                {{ article.title }}
              </router-link>
              <span class="visit-count" v-if="article.visit_count">
                <i class="fas fa-eye"></i> {{ article.visit_count }}
              </span>
            </div>
            <div class="article-date">{{ formatted_time(article.created) }}</div>
          </div>
        </div>
      </div>

      <div id="paginator">
        <span v-if="is_page_exists('previous')">
          <router-link :to="get_path('previous')"> Prev </router-link>
        </span>
        <span class="current-page">
          {{ get_page_param("current") }}
        </span>
        <span v-if="is_page_exists('next')">
          <router-link :to="get_path('next')"> Next </router-link>
        </span>
      </div>
    </div>

    <!-- Sidebar -->
    <div class="sidebar">
      <!-- Tags Section -->
      <div class="sidebar-section">
        <h3 class="sidebar-title">
          <i class="fas fa-tags"></i> Tags
        </h3>
        <div class="sidebar-content">
          <div 
            v-for="tag in recentTags" 
            :key="tag.id" 
            class="sidebar-tag"
            :class="{ active: selectedTag === tag.text }"
            @click="filterByTag(tag.text)"
          >
            {{ tag.text }}
            <span class="tag-count" v-if="tag.count">({{ tag.count }})</span>
          </div>
          <div v-if="recentTags.length === 0" class="empty-message">
            No tags available
          </div>
        </div>
      </div>

      <!-- Categories Section -->
      <div class="sidebar-section">
        <h3 class="sidebar-title">
          <i class="fas fa-folder"></i> Categories
        </h3>
        <div class="sidebar-content">
          <div 
            v-for="category in categories" 
            :key="category.id" 
            class="sidebar-category"
            :class="{ active: selectedCategory === category.id }"
            @click="filterByCategory(category.id)"
          >
            {{ category.title }}
            <span class="category-count" v-if="category.count">({{ category.count }})</span>
          </div>
          <div v-if="categories.length === 0" class="empty-message">
            No categories available
          </div>
        </div>
      </div>

      <!-- Visitors Count Section -->
      <div class="sidebar-section visitors-section" v-if="pageVisitCount">
        <div class="visitors-count">
          <i class="fas fa-glasses"></i>
          <span>Total Visitors: {{ pageVisitCount }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
// import axios from 'axios';

import { ref, watch } from "vue";
import { useRoute, useRouter } from "vue-router";
import getArticleData from "@/composables/getArticleData.js";
import pagination from "@/composables/pagination.js";
import articleGrid from "@/composables/articleGrid.js";
import formattedTime from "@/composables/formattedTime.js";
import axios from "axios";

export default {
  name: "ArticleList",

  setup() {
    const info = ref("");
    const route = useRoute();
    const router = useRouter();
    const pageVisitCount = ref(0);
    const recentTags = ref([]);
    const categories = ref([]);
    const selectedTag = ref(null);
    const selectedCategory = ref(null);
    const error = ref(null);

    const kwargs = ref({ 
      page: 0, 
      searchText: "",
      tag: null,
      category: null
    });
    
    getArticleData(info, route, kwargs);

    const { is_page_exists, get_page_param, get_path } = pagination(
      info,
      route
    );

    const { imageIfExists, gridStyle } = articleGrid();

    const formatted_time = formattedTime;

    // 获取正在使用的标签
    const getRecentTags = async () => {
      try {
        const response = await axios.get("/api/tag/");
        // 按照使用频率排序（如果后端提供了这个信息）
        recentTags.value = response.data;
        error.value = null;
      } catch (error) {
        console.error("Error fetching tags:", error);
        recentTags.value = [];
        error.value = "Failed to load tags";
      }
    };

    // 获取正在使用的分类
    const getCategories = async () => {
      try {
        const response = await axios.get("/api/category/");
        categories.value = response.data;
        error.value = null;
      } catch (error) {
        console.error("Error fetching categories:", error);
        categories.value = [];
        error.value = "Failed to load categories";
      }
    };

    // 根据标签筛选文章
    const filterByTag = (tag) => {
      if (selectedTag.value === tag) {
        selectedTag.value = null;
        router.push({ 
          path: route.path,
          query: { ...route.query, tag: undefined, page: undefined }
        });
      } else {
        selectedTag.value = tag;
        router.push({ 
          path: route.path,
          query: { ...route.query, tag: tag, page: undefined }
        });
      }
    };

    // 根据分类筛选文章
    const filterByCategory = (categoryId) => {
      if (selectedCategory.value === categoryId) {
        selectedCategory.value = null;
        router.push({ 
          path: route.path,
          query: { ...route.query, category: undefined, page: undefined }
        });
      } else {
        selectedCategory.value = categoryId;
        router.push({ 
          path: route.path,
          query: { ...route.query, category: categoryId, page: undefined }
        });
      }
    };

    // 获取首页访问计数
    const getPageVisitCount = async () => {
      try {
        const response = await axios.get("/api/visit-count/home/");
        pageVisitCount.value = response.data.count;
      } catch (error) {
        console.error("Error fetching page visit count:", error);
        pageVisitCount.value = 0;
      }
    };

    // 获取文章访问计数
    const getVisitCounts = async () => {
      if (info.value && info.value.results) {
        for (let article of info.value.results) {
          try {
            const response = await axios.get(
              `/api/visit-count/article/${article.id}/`
            );
            article.visit_count = response.data.count;
          } catch (error) {
            console.error("Error fetching visit count:", error);
            article.visit_count = 0;
          }
        }
      }
    };

    // 监听路由变化，更新筛选状态
    watch(
      () => route.query,
      (query) => {
        selectedTag.value = query.tag || null;
        selectedCategory.value = query.category ? parseInt(query.category) : null;
      },
      { immediate: true }
    );

    // 监听 info 变化，当文章列表加载完成后获取访问计数
    watch(
      () => info.value,
      (newVal) => {
        if (newVal && newVal.results) {
          getVisitCounts();
          // 当文章列表更新时，重新获取标签和分类
          getRecentTags();
          getCategories();
        }
      },
      { immediate: true }
    );

    // 初始化数据
    getPageVisitCount();
    getRecentTags();
    getCategories();

    return {
      info,
      is_page_exists,
      get_page_param,
      get_path,
      imageIfExists,
      gridStyle,
      formatted_time,
      pageVisitCount,
      recentTags,
      categories,
      selectedTag,
      selectedCategory,
      filterByTag,
      filterByCategory,
      error,
    };
  },
};
</script>

<style scoped>
.page-visit-counter-wrapper {
  width: 100%;
  padding: 10px 20px;
  box-sizing: border-box;
  display: flex;
  justify-content: flex-end;
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
  font-family: "Lora", serif;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.page-visit-counter i {
  font-size: 0.9em;
  color: #2e7d32;
}

.image {
  width: 180px;
  height: 120px;
  border-radius: 10px;
  box-shadow: rgb(2, 117, 117) 0 0 12px;
  object-fit: cover;
  object-position: center;
  border: 1px solid #eecfa7;
  box-sizing: border-box;
}

.image-container {
  width: 180px;
  height: 120px;
  overflow: hidden;
  border-radius: 10px;
  margin-right: 20px;
  box-sizing: border-box;
}

.content-container {
  flex: 1;
  padding-left: 10px; /* 从 20px 减小到 10px */
}

.grid {
  padding-bottom: 20px;
  display: flex;
  align-items: flex-start;
}

#articles {
  padding: 10px;
}

.article-title {
  font-size: large;
  font-weight: bolder;
  color: black;
  text-decoration: none;
  font-family: "Roboto", sans-serif;
}

.a-title-container {
  padding: 5px 0 5px 0;
  display: flex;
  align-items: center;
  gap: 10px;
}

.visit-count {
  font-size: 0.8em;
  color: #2e7d32;
  background: rgba(46, 125, 50, 0.1);
  padding: 1px 6px;
  border-radius: 10px;
  display: inline-flex;
  align-items: center;
  gap: 3px;
  font-family: "Lora", serif;
}

.visit-count i {
  font-size: 0.8em;
  color: #2e7d32;
}

.category {
  padding: 5px 10px 5px 10px;
  margin: 5px 5px 5px 0;
  font-family: "Lora", serif;
  font-size: small;
  background-color: rgb(0, 113, 141);
  color: whitesmoke;
  border-radius: 15px;
}

.tag {
  padding: 2px 5px 2px 5px;
  margin: 5px 5px 5px 0;
  font-family: "Lora", serif;
  font-size: small;
  background-color: #4e4e4e;
  color: whitesmoke;
  border-radius: 5px;
}

.article-date {
  font-family: "Lora", serif;
  color: gray;
  font-size: small;
}

#paginator {
  text-align: center;
  padding-top: 50px;
  font-family: "Lora", serif;
}

a {
  color: black;
  font-family: "Lora", serif;
}

.current-page {
  font-size: x-large;
  font-weight: bold;
  padding-left: 10px;
  padding-right: 10px;
}

.page-layout {
  display: flex;
  gap: 30px;
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.main-content {
  flex: 1;
  min-width: 0; /* 防止flex子项溢出 */
}

.sidebar {
  width: 250px;
  flex-shrink: 0;
}

.sidebar-section {
  background: white;
  border-radius: 10px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  margin-bottom: 20px;
  overflow: hidden;
}

.sidebar-title {
  margin: 0;
  padding: 15px;
  background: #0288d1;  /* Info blue for title background */
  font-size: 1.1em;
  color: white;
  border-bottom: 1px solid #01579b;
  display: flex;
  align-items: center;
  gap: 8px;
}

.sidebar-title i {
  color: white;
}

.sidebar-content {
  padding: 15px;
}

.sidebar-tag {
  display: inline-block;
  padding: 4px 8px;
  margin: 4px;
  background: rgba(2, 136, 209, 0.1);  /* Light info blue background */
  border-radius: 4px;
  font-size: 0.9em;
  color: #0288d1;  /* Info blue text */
  cursor: pointer;
  transition: all 0.2s ease;
}

.sidebar-tag:hover {
  background: rgba(2, 136, 209, 0.2);  /* Slightly darker on hover */
}

.sidebar-tag.active {
  background: #0288d1;  /* Solid info blue when active */
  color: white;
}

.sidebar-category {
  padding: 8px 12px;
  margin: 4px 0;
  border-radius: 4px;
  font-size: 0.95em;
  color: #0288d1;  /* Info blue text */
  cursor: pointer;
  transition: all 0.2s ease;
}

.sidebar-category:hover {
  background: rgba(2, 136, 209, 0.1);  /* Light info blue on hover */
}

.sidebar-category.active {
  background: #0288d1;  /* Solid info blue when active */
  color: white;
}

.visitors-section {
  padding: 15px;
  text-align: center;
  background: rgba(46, 125, 50, 0.1);
}

.visitors-count {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  color: #2e7d32;
  font-family: "Lora", serif;
  font-size: 0.9em;
}

.visitors-count i {
  font-size: 1.1em;
}

.empty-message {
  color: #666;
  font-style: italic;
  text-align: center;
  padding: 10px;
}

.tag-count,
.category-count {
  font-size: 0.8em;
  opacity: 0.7;
  margin-left: 4px;
}
</style>
