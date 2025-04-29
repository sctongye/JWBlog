<template>
  <BlogHeader />
  <div id="article-create">
    <h3>发表文章</h3>

    <div class="image-upload-section">
      <h4>文章封面图</h4>
      <div class="upload-container">
        <input
          type="file"
          @change="onAvatarChange"
          accept="image/*"
          ref="avatarInput"
          style="display: none"
        />
        <button @click="triggerAvatarInput" class="upload-btn">
          选择封面图
        </button>
        <div v-if="currentAvatar" class="preview-container">
          <img
            :src="currentAvatar"
            alt="Current Avatar"
            class="preview-image"
          />
          <div class="markdown-link">
            <p>当前封面图链接：</p>
            <div class="link-container">
              <code>![avatar]({{ currentAvatar }})</code>
              <button @click="copyAvatarLink" class="copy-btn">复制</button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="image-upload-section">
      <h4>上传图片</h4>
      <div class="upload-container">
        <input
          type="file"
          @change="onImageChange"
          accept="image/*"
          ref="fileInput"
          style="display: none"
        />
        <button @click="triggerFileInput" class="upload-btn">选择图片</button>
        <div v-if="uploadedImageUrl" class="preview-container">
          <img :src="uploadedImageUrl" alt="Preview" class="preview-image" />
          <div class="markdown-link">
            <p>Markdown链接：</p>
            <div class="link-container">
              <code>![image]({{ uploadedImageUrl }})</code>
              <button @click="copyMarkdownLink" class="copy-btn">复制</button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <form>
      <div class="form-elem">
        <span>标题：</span>
        <input v-model="title" type="text" placeholder="输入标题" />
      </div>

      <div class="form-elem">
        <span>分类：</span>
        <span v-for="category in categories" :key="category.id">
          <button
            class="category-btn"
            :style="categoryStyle(category)"
            @click.prevent="chooseCategory(category)"
          >
            {{ category.title }}
          </button>
        </span>
      </div>

      <div class="form-elem">
        <span>标签：</span>
        <input v-model="tags" type="text" placeholder="输入标签，用逗号分隔" />
      </div>

      <div class="form-elem">
        <span>正文：</span>
        <div class="editor-wrapper" ref="editorRoot">
          <Editor
            v-model="body"
            :initialValue="body"
            :options="{
              height: '500px',
              initialEditType: 'markdown',
              previewStyle: 'vertical',
              toolbarItems: [
                ['heading', 'bold', 'italic', 'strike'],
                ['hr', 'quote'],
                ['ul', 'ol', 'task', 'indent', 'outdent'],
                ['table', 'image', 'link'],
                ['code', 'codeblock'],
              ],
            }"
            @change="handleEditorChange"
          />
        </div>
      </div>

      <div class="form-elem">
        <button v-on:click.prevent="submit">提交</button>
      </div>
    </form>
  </div>
  <BlogFooter />
</template>

<script>
import BlogHeader from "@/components/BlogHeader.vue";
import BlogFooter from "@/components/BlogFooter.vue";
import axios from "axios";
import authorization from "@/utils/authorization";

import "@toast-ui/editor/dist/toastui-editor.css";
import { Editor } from "@toast-ui/editor";

// 配置 API 基础 URL
const API_BASE_URL = "/api"; // 使用相对路径，让 Nginx 处理代理

export default {
  name: "ArticleCreate",
  components: { BlogHeader, BlogFooter },
  data: function () {
    return {
      title: "",
      body: "",
      categories: [],
      selectedCategory: null,
      tags: "",
      avatarID: null,
      uploadedImageUrl: "",
      currentAvatar: "",
      editor: null,
    };
  },
  mounted() {
    axios
      .get(`${API_BASE_URL}/category/`)
      .then((response) => (this.categories = response.data))
      .catch((error) => {
        console.error("Error fetching categories:", error);
        if (error.response) {
          console.error("Response status:", error.response.status);
          console.error("Response data:", error.response.data);
        }
      });

    this.$nextTick(() => {
      this.editor = new Editor({
        el: this.$refs.editorRoot,
        height: "500px",
        initialEditType: "markdown",
        previewStyle: "vertical",
        initialValue: this.body,
        toolbarItems: [
          ["heading", "bold", "italic", "strike"],
          ["hr", "quote"],
          ["ul", "ol", "task", "indent", "outdent"],
          ["table", "image", "link"],
          ["code", "codeblock"],
        ],
        hooks: {
          addImageBlobHook: async (blob, callback) => {
            try {
              const reader = new FileReader();
              reader.onload = function(e) {
                const base64 = e.target.result;
                console.log("Base64 image data:", base64.substring(0, 100) + "..."); // 只打印前100个字符
                callback(base64, blob.name);
              };
              reader.readAsDataURL(blob);
            } catch (error) {
              console.error("Error processing image:", error);
              alert("图片处理失败，请重试");
            }
          },
        },
      });

      // 监听编辑器内容变化
      this.editor.on("change", () => {
        this.body = this.editor.getMarkdown();
      });
    });
  },
  beforeUnmount() {
    if (this.editor) {
      this.editor.destroy();
    }
  },
  methods: {
    triggerFileInput() {
      this.$refs.fileInput.click();
    },
    triggerAvatarInput() {
      this.$refs.avatarInput.click();
    },
    onImageChange(e) {
      const file = e.target.files[0];
      if (!file) return;

      // 检查文件类型
      const allowedTypes = ["image/jpeg", "image/png", "image/gif"];
      if (!allowedTypes.includes(file.type)) {
        alert("只支持 JPG、PNG 和 GIF 格式的图片");
        return;
      }

      // 检查文件大小
      const maxSize = 5 * 1024 * 1024; // 5MB
      if (file.size > maxSize) {
        alert("文件大小不能超过 5MB");
        return;
      }

      const formData = new FormData();
      formData.append("content", file);

      axios
        .post(`${API_BASE_URL}/avatar/`, formData, {
          headers: {
            "Content-Type": "multipart/form-data",
            Authorization: "Bearer " + localStorage.getItem("access.myblog"),
          },
        })
        .then((response) => {
          this.uploadedImageUrl = response.data.content;
        })
        .catch((error) => {
          console.error("Error uploading image:", error);
          if (error.response) {
            console.error("Response status:", error.response.status);
            console.error("Response data:", error.response.data);
          }
          alert("图片上传失败，请重试");
        });
    },
    copyMarkdownLink() {
      const markdownLink = `![image](${this.uploadedImageUrl})`;
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(markdownLink)
          .then(() => alert("Markdown链接已复制到剪贴板"))
          .catch(err => {
            console.error("复制失败:", err);
            this.fallbackCopy(markdownLink);
          });
      } else {
        this.fallbackCopy(markdownLink);
      }
    },
    fallbackCopy(text) {
      // 创建一个临时的 textarea 元素
      const textarea = document.createElement('textarea');
      textarea.value = text;
      textarea.style.position = 'fixed';  // 防止滚动
      textarea.style.opacity = '0';
      document.body.appendChild(textarea);
      textarea.select();
      try {
        document.execCommand('copy');
        alert("Markdown链接已复制到剪贴板");
      } catch (err) {
        console.error("复制失败:", err);
        alert("复制失败，请手动复制链接");
      }
      document.body.removeChild(textarea);
    },
    onAvatarChange(e) {
      const file = e.target.files[0];
      if (!file) return;

      // 检查文件类型
      const allowedTypes = ["image/jpeg", "image/png", "image/gif"];
      if (!allowedTypes.includes(file.type)) {
        alert("只支持 JPG、PNG 和 GIF 格式的图片");
        return;
      }

      // 检查文件大小
      const maxSize = 5 * 1024 * 1024; // 5MB
      if (file.size > maxSize) {
        alert("文件大小不能超过 5MB");
        return;
      }

      const formData = new FormData();
      formData.append("content", file);

      axios
        .post(`${API_BASE_URL}/avatar/`, formData, {
          headers: {
            "Content-Type": "multipart/form-data",
            Authorization: "Bearer " + localStorage.getItem("access.myblog"),
          },
        })
        .then((response) => {
          this.currentAvatar = response.data.content;
          this.avatarID = response.data.id;
        })
        .catch((error) => {
          console.error("Error uploading avatar:", error);
          if (error.response) {
            console.error("Response status:", error.response.status);
            console.error("Response data:", error.response.data);
          }
          alert("封面图上传失败，请重试");
        });
    },
    copyAvatarLink() {
      const markdownLink = `![avatar](${this.currentAvatar})`;
      navigator.clipboard
        .writeText(markdownLink)
        .then(() => alert("封面图链接已复制到剪贴板"))
        .catch((err) => console.error("复制失败:", err));
    },
    categoryStyle(category) {
      if (
        this.selectedCategory !== null &&
        category.id === this.selectedCategory.id
      ) {
        return {
          backgroundColor: "black",
        };
      }
      return {
        backgroundColor: "lightgrey",
        color: "black",
      };
    },
    chooseCategory(category) {
      this.selectedCategory = category;
    },
    handleEditorChange() {
      if (this.editor) {
        this.body = this.editor.getMarkdown();
      }
    },
    submit() {
      const that = this;
      this.handleEditorChange();
      authorization().then(function (response) {
        if (response[0]) {
          let data = {
            title: that.title,
            body: that.body,
          };

          // 添加标题图
          data.avatar_id = that.avatarID;

          // 添加分类
          if (that.selectedCategory) {
            data.category_id = that.selectedCategory.id;
          }
          // 预处理并添加标签
          // 逗号分隔标签并剔除无效标签
          data.tags = that.tags
            .split(/[,，]/)
            .map((x) => x.trim())
            .filter((x) => x.charAt(0) !== "");

          // 发送发表文章请求
          // 成功后前往详情页面
          const token = localStorage.getItem("access.myblog");
          axios
            .post(`${API_BASE_URL}/article/`, data, {
              headers: { Authorization: "Bearer " + token },
            })
            .then(function (response) {
              that.$router.push({
                name: "ArticleDetail",
                params: { id: response.data.id },
              });
            })
            .catch((error) => {
              console.error("Error creating article:", error);
              if (error.response) {
                console.error("Response status:", error.response.status);
                console.error("Response data:", error.response.data);
              }
              alert("创建文章失败，请重试");
            });
        } else {
          alert("令牌过期，请重新登录。");
        }
      });
    },
  },
};
</script>

<style scoped>
.image-upload-section {
  margin-bottom: 20px;
  padding: 20px;
  background: #f5f5f5;
  border-radius: 8px;
}

.upload-container {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.upload-btn {
  padding: 8px 16px;
  background-color: mediumslateblue;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-family: "Lora", serif;
}

.upload-btn:hover {
  background-color: darkslateblue;
}

.preview-container {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.preview-image {
  max-width: 300px;
  max-height: 200px;
  border-radius: 4px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.markdown-link {
  background: white;
  padding: 10px;
  border-radius: 4px;
  border: 1px solid #ddd;
}

.link-container {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-top: 5px;
}

code {
  background: #f0f0f0;
  padding: 5px 10px;
  border-radius: 4px;
  font-family: monospace;
}

.copy-btn {
  padding: 4px 8px;
  background-color: #4caf50;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.9em;
}

.copy-btn:hover {
  background-color: #45a049;
}

.category-btn {
  margin-right: 10px;
}

#article-create {
  text-align: center;
  font-size: large;
}

form {
  text-align: left;
  padding-left: 100px;
  padding-right: 10px;
}

.form-elem {
  padding: 10px;
}

input {
  height: 25px;
  padding-left: 10px;
  width: 50%;
}

button {
  height: 35px;
  cursor: pointer;
  border: none;
  outline: none;
  background: steelblue;
  color: whitesmoke;
  border-radius: 5px;
  width: 60px;
}

.editor-wrapper {
  width: 100%;
  margin: 20px 0;
  max-width: 100%;
}

.editor-wrapper :deep(.toastui-editor-defaultUI) {
  border: 1px solid #ddd;
  border-radius: 4px;
  width: 100%;
}

.editor-wrapper :deep(.toastui-editor-defaultUI-toolbar) {
  border-bottom: 1px solid #ddd;
  background-color: #f8f9fa;
  width: 100%;
}

.editor-wrapper :deep(.toastui-editor-defaultUI-toolbar-group) {
  border-right: 1px solid #ddd;
}

.editor-wrapper :deep(.toastui-editor-defaultUI-toolbar-group:last-child) {
  border-right: none;
}

.editor-wrapper :deep(.toastui-editor-defaultUI-toolbar-group button) {
  color: #333;
}

.editor-wrapper :deep(.toastui-editor-defaultUI-toolbar-group button:hover) {
  background-color: #e9ecef;
}

.editor-wrapper :deep(.toastui-editor-md-container) {
  border-right: 1px solid #ddd;
  width: 100%;
}

.editor-wrapper :deep(.toastui-editor-md-container .toastui-editor-md-preview) {
  background-color: #fff;
  width: 100%;
}

.editor-wrapper :deep(.toastui-editor-md-container .toastui-editor-md-preview .toastui-editor-contents) {
  font-family: "Lora", serif;
  line-height: 1.6;
  width: 100%;
}
</style>
