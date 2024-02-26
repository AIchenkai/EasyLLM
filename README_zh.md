🌍 \[ [English](README.md) | 中文 \]

# EasyLLM

## 介绍
EasyLLM 是一个简洁的大模型应用项目，基于大语言模型（LLMs），提供对话、知识库构建和互联网搜索等功能。它支持对部署在 Azure 的 OpenAI 服务 和本地的大型模型进行 API 调用，并使用 Gradio 构建用户界面。

## 免责声明
请各位严格遵守如下约定：

1. 本项目任何资源仅供学术研究使用，严禁任何商业用途。
2. 模型输出受多种不确定性因素影响，本项目当前无法保证其准确性，严禁用于任何真实场景。
3. 本项目不承担任何法律责任，亦不对因使用相关资源和输出结果而可能产生的任何损失承担责任。

## 功能和特点
- 与 Azure 的 OpenAI 和本地部署的 LLM api 简单集成。
- 使用 Gradio 构建的用户友好界面。
- 支持与 ChatGLM2 的大模型的对话。
- 支持部署本地大模型为 api 服务。
- 支持上传文件构建知识库。
- 支持互联网搜索功能。
- 可灵活切换不同的本地模型和知识库。

## Webui Demo
https://github.com/AIchenkai/EasyLLM/assets/121413549/0b1d2bad-f249-4dc3-8a22-f6752a299b6b

## 如何使用
1. 克隆仓库：`git clone https://github.com/your-username/EasyLLM.git`
2. 安装依赖项：`pip install -r requirements.txt`
3. 在 config.json 文件设置相关内容，包括 Azure OpenAI 的 api_key、Bing Search 的 subscription_key、知识库存储地址 project_dir、本地向量模型地址 embedding_model_path
4. 运行大模型 api 部署文件：`python modules/NLG/nlg_server.py`
5. 运行 webui 文件：`python easyllm-webui.py`

## 贡献和改进
贡献和改进是推动 EasyLLM 项目持续发展的重要因素。您可以通过以下方式参与和支持项目：

- **问题和反馈**：如果您在使用 EasyLLM 时发现任何问题、错误或有改进建议，请在 GitHub 的 Issues 页面上提出您的反馈。我们欢迎任何关于性能、功能或用户体验方面的问题和意见。

- **Pull 请求**：如果您有能够改进 EasyLLM 的代码、功能或文档的想法，欢迎提交 Pull 请求。我们将仔细审查您的贡献，并与您合作以确保项目的质量和稳定性。

- **分享经验**：如果您在大模型应用方面有独特的经验和最佳实践，我们鼓励您将其分享给社区。您可以编写博客文章、示例代码或提供文档来帮助其他开发者更好地理解和使用 EasyLLM。

## 注意事项
- 在运行程序之前，请确保在 `configs.json` 文件中配置了正确的设置。
  
- 确保为文档上传和索引提供适当的权限和资源访问。
  
- EasyLLM 是基于深度学习技术构建的，它可以提供有价值的建议和解释，但不应视为咨询专家的替代品。在重要的事务中，建议您咨询专业的顾问或者机构。

- 本项目遵循适用的开源许可证。请在使用或分发代码之前，详细阅读项目中的许可证文件。

## 致谢
我们感谢开源社区的贡献者以及 Gradio 的开发人员为其出色的工作。
- Chatbot-Client：https://github.com/Wozzilla/Chatbot-Client
- Search_with_lepton：https://github.com/leptonai/search_with_lepton
- ChuanhuChatGPT：https://github.com/GaiZhenbiao/ChuanhuChatGPT
- ChatGLM-6B：https://github.com/THUDM/ChatGLM-6B
- Langchain-Chatchat：https://github.com/chatchat-space/Langchain-Chatchat

## TODO
- [ ] 增加对更多 NLG 模型的支持。
- [ ] 增加对更多知识库文件格式的支持：docx、json。
- [ ] 改进错误处理和日志记录。

## 参与讨论
欢迎加入 [GitHub Issues](https://github.com/AIchenkai/EasyLLM/issues) 进行讨论，提出任何问题、建议或反馈。

如果您对 EasyLLM 有任何疑问、建议或想法，欢迎加入我们的讨论。您可以联系 18222953521@163.com 提出问题、参与技术讨论或分享您的见解。

我们衷心感谢您对 EasyLLM 项目的关注和参与！希望通过这个项目，能够为中文大模型应用提供更智能、可靠的解决方案。

