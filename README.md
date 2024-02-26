🌍 [中文介绍](README_zh.md)

# EasyLLM

## Introduction
EasyLLM is a concise project for applying large models, based on Large Language Models (LLMs), providing functionalities such as dialogue, knowledge base construction, and internet search. It supports API calls on large models deployed on Azure, OpenAI, and locally, and uses Gradio to build the user interface.

EasyLLM 是一个简洁的大模型应用项目，基于大语言模型（LLMs），提供对话、知识库构建和互联网搜索等功能。它支持对部署在 Azure 的 OpenAI 服务 和本地的大型模型进行 API 调用，并使用 Gradio 构建用户界面。

## Disclaimer
Please strictly adhere to the following agreements:

1. Any resources of this project are for academic research purposes only and strictly prohibited for any commercial use.
2. Model outputs are subject to various uncertainties, and this project cannot guarantee their accuracy at present, and are strictly prohibited from being used in any real scenarios.
3. This project assumes no legal responsibility and shall not be liable for any losses incurred due to the use of related resources and output results.

## Features and Characteristics
- Simple integration with LLM APIs deployed on Azure, OpenAI, and locally.
- User-friendly interface built with Gradio.
- Support for dialogue with ChatGLM2's large models.
- Support for deploying local large models as APIs.
- Support for uploading files to construct knowledge bases.
- Support for internet search functionality.
- Flexibility to switch between different local models and knowledge bases.

## How to Use
1. Clone the repository: `git clone https://github.com/your-username/EasyLLM.git`
2. Install dependencies: `pip install -r requirements.txt`
3. Set up related content in the `configs.json` file, including Azure OpenAI's `api_key`, Bing Search's `subscription_key`, project directory `project_dir` for knowledge base storage, and local vector model address `embedding_model_path`.
4. Run the large model API deployment file: `python modules/NLG/nlg_server.py`
5. Run the web UI file: `python easyllm-webui.py`

## Contributing and Improvements
Contributions and improvements are crucial to driving the continuous development of the EasyLLM project. You can participate and support the project in the following ways:

- **Issues and Feedback**: If you encounter any problems, errors, or have suggestions for improvement while using EasyLLM, please provide your feedback on the GitHub Issues page. We welcome any questions and feedback on performance, functionality, or user experience.

- **Pull Requests**: If you have ideas for improving EasyLLM code, functionality, or documentation, feel free to submit a pull request. We will carefully review your contributions and work with you to ensure the quality and stability of the project.

- **Sharing Experience**: If you have unique experiences and best practices in large model applications, we encourage you to share them with the community. You can write blog posts, example code, or provide documentation to help other developers better understand and use EasyLLM.

## Notes
- Before running the program, ensure that the `configs.json` file is correctly configured.
  
- Ensure proper permissions and access to resources for document uploading and indexing.
  
- EasyLLM is built on deep learning technology and can provide valuable suggestions and explanations, but should not be considered a substitute for consulting experts. For important matters, it is recommended to consult professional consultants or institutions.

- This project follows applicable open-source licenses. Please read the license files in the project in detail before using or distributing the code.

## Acknowledgements
We appreciate the contributions of the open-source community and the developers of Gradio for their excellent work.
- Chatbot-Client: https://github.com/Wozzilla/Chatbot-Client
- Search_with_lepton：https://github.com/leptonai/search_with_lepton
- ChuanhuChatGPT: https://github.com/GaiZhenbiao/ChuanhuChatGPT
- ChatGLM-6B: https://github.com/THUDM/ChatGLM-6B
- Langchain-Chatchat: https://github.com/chatchat-space/Langchain-Chatchat


## TODO
- [ ] Add support for more NLG models.
- [ ] Add support for more knowledge base file formats: docx, json.
- [ ] Improve error handling and logging.

## Join the Discussion
Feel free to join the discussion on [GitHub Issues](https://github.com/AIchenkai/EasyLLM/issues) for any questions, suggestions, or feedback.

If you have any questions, suggestions, or ideas about EasyLLM, feel free to join our discussion. You can contact 18222953521@163.com to ask questions, participate in technical discussions, or share your insights.

We sincerely thank you for your attention and participation in the EasyLLM project! We hope that through this project, we can provide more intelligent and reliable solutions for Chinese large model applications.
