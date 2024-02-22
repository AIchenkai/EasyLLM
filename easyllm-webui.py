"""本文件为整个项目的主文件，并使用gradio搭建界面"""
import asyncio
import logging
import gradio as gr
import os
import time
import shutil
from langchain_community.document_loaders import TextLoader
from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain.embeddings.huggingface import HuggingFaceEmbeddings

from modules import utils

from modules.NLG import *
from modules.Search import *



# 设置项目目录
PROJECT_DIR = utils.Configs["settings"]["project_dir"]
VECTOR_STORES_DIR = os.path.join(PROJECT_DIR, "kb")
VECTOR_FILES_DIR = os.path.join(PROJECT_DIR, "file")

embedding_model_path = utils.Configs["settings"]["embedding_model_path"]


nlgService = ChatGLM(utils.Configs["ChatGLM"])
BingService = Search(utils.Configs["Bing Search"])

# 获取项目目录中的所有 FAISS 库
def list_vector_store():
    return [f.replace(".faiss", "") for f in os.listdir(VECTOR_STORES_DIR) if f.endswith(".faiss")]

# 初始化下拉列表选项
vector_stores = list_vector_store()

with gr.Blocks(theme=gr.themes.Soft(), title="EasyLLM, a simple chatbot based on LLM",
               css="./assets/css/EasyLLMStyle.css", js="./assets/js/EasyLLMStyle.js"
               ) as demo:
    with gr.Row(elem_id="baseContainer"):
        with gr.Column(min_width=280, elem_id="sideBar"):

            nlgSwitch = gr.Dropdown([i.name for i in NLGEnum], value=nlgService.type.name, interactive=True,
                                    label="选择NLG模型", elem_id="nlgSwitch")

        with gr.Column(scale=5, elem_id="chatPanel"):
            botComponent = gr.Chatbot(label=nlgService.type.name, avatar_images=utils.getAvatars(), elem_id="chatbot")
            with gr.Row(elem_id="inputPanel"):
                with gr.Row():
                    knowledgebaseSwitch = gr.components.Checkbox(label="知识库")
                    internetSwitch = gr.components.Checkbox(label="互联网")
                    docSwitch = gr.components.Checkbox(label="文档对话")
                textInput = gr.Textbox(placeholder="点击输入", show_label=False, scale=4, elem_id="textInput")
                submitButton = gr.Button(value="发送", size="sm", min_width=80, elem_id="submitButton")
                clearButton = gr.Button(value="清除", size="sm", min_width=80, elem_id="cleanButton")

            with gr.Row(elem_id="KnowledgeBasePanel"):
                with gr.Column(min_width=280, elem_id="sideBar"):

                    select_vector_store = gr.Dropdown(choices=vector_stores, label="选择知识库",placeholder="请选择知识库",
                                                      elem_id="vectorStoreSwitch")
                    with gr.Row(elem_id="inputPanel"):
                        vector_store_name = gr.Textbox(lines=1, placeholder="输入新建知识库名称",
                                                       label="新建知识库")
                        vector_store_file = gr.File(label="上传文件(支持pdf、txt）", file_types=['text'])
                    with gr.Row(elem_id="inputPanel"):
                        build_button = gr.Button(value="知识库创建", size="sm", min_width=80, elem_id="submitButton")
                        load_button = gr.Button(value="文档加载", size="sm", min_width=80, elem_id="submitButton")

                with gr.Column(scale=5, elem_id="searchPanel"):
                    with gr.Row(elem_id="inputPanel"):
                        query = gr.Textbox(lines=5, placeholder="输入要查询的句子", label="查询知识库",
                                           scale=4, elem_id="queryBox")

                        search_button = gr.Button(value="查询", size="sm", min_width=80, elem_id="submitButton")

                    with gr.Row():
                        similar_sentences_output = gr.Textbox(label="查询结果", elem_id="similarSentencesBox")
                        execution_time_output = gr.Textbox(label="查询时间", elem_id="executionTimeBox")




        def cleanAllContent(message, chatHistory):
            """
            清除全部消息
            """
            return "", []


        def textChat(message: str, chatHistory: list, internetSwitch: bool, knowledgebaseSwitch: bool, docSwitch:bool, select_vector_store: str):
            """
            与聊天机器人进行文本聊天
            :param message: str 用户输入的消息
            :param chatHistory: [[str, str]...] 分别为用户输入和机器人回复(先前的)
            """

            if internetSwitch:
                print("Bing search starting...")
                internetmessage = BingService.search_with_bing(message)
                botMessage = nlgService.continuedQuery(internetmessage, chatHistory)
                chatHistory.append((message, botMessage))
            elif knowledgebaseSwitch:
                print("Knowledge base search starting...")
                knowledgebasesearch, _ = search_similar_sentences(message, select_vector_store)

                KB_prompt = """
                        你是大型语言人工智能助手。你将接收到一个用户问题，请针对该问题提供清晰、简洁且准确的答案。你将获得一系列与问题相关的上下文信息，如果适用，请使用上下文信息。

                        你的答案必须正确、准确，并且以专家的角度用客观、专业的语气撰写。请将回答限制在1024个字符内。不要提供与问题无关的信息，也不要重复。如果给定的上下文没有提供足够的信息，请在相关主题后注明“信息缺失”。

                        除了代码、特定的名称和引用外，你的答案必须使用与问题相同的语言撰写，一定要用中文回答中文问题。

                        以下是上下文信息集：

                        {context}

                        请记住，不要盲目地逐字重复上下文内容。以下是用户的问题：
                        
                        """

                knowledgebasemessage = KB_prompt.format(context = knowledgebasesearch) + message
                botMessage = nlgService.continuedQuery(knowledgebasemessage, chatHistory)
                chatHistory.append((message, botMessage))
            elif docSwitch:
                print("document search starting...")
                docsearch, _ = search_similar_sentences(message, select_vector_store)

                KB_prompt = """
                        你是大型语言人工智能助手。你将接收到一个用户问题，请针对该问题提供清晰、简洁且准确的答案。你将获得一系列与问题相关的上下文信息，如果适用，请使用上下文信息。

                        你的答案必须正确、准确，并且以专家的角度用客观、专业的语气撰写。请将回答限制在1024个字符内。不要提供与问题无关的信息，也不要重复。如果给定的上下文没有提供足够的信息，请在相关主题后注明“信息缺失”。

                        除了代码、特定的名称和引用外，你的答案必须使用与问题相同的语言撰写，一定要用中文回答中文问题。

                        以下是上下文信息集：

                        {context}

                        请记住，不要盲目地逐字重复上下文内容。以下是用户的问题：

                        """

                docmessage = KB_prompt.format(context=docsearch) + message
                botMessage = nlgService.continuedQuery(docmessage, chatHistory)
                chatHistory.append((message, botMessage))
            else:
                botMessage = nlgService.continuedQuery(message, chatHistory)
                chatHistory.append((message, botMessage))

            return "", chatHistory, internetSwitch, knowledgebaseSwitch, docSwitch, select_vector_store



        def switchNLG(selectService: str):
            """
            切换NLG模型
            :param selectService: str NLG模型名称
            :return: str NLG模型名称
            """
            global nlgService, nlgSwitch
            currentService = nlgService.type.name  # 当前的NLG模型
            if selectService == currentService:
                return currentService
            else:  # 尝试切换模型
                try:
                    if selectService == NLGEnum.Azure.name:
                        tempService = Azure(utils.Configs["Azure OpenAI"])
                    elif selectService == NLGEnum.ChatGLM.name:
                        tempService = ChatGLM(utils.Configs["ChatGLM"])
                    else:  # 未知的模型选择，不执行切换
                        gr.Warning(f"未知的NLG模型，将不进行切换，当前：{currentService}")
                        return currentService
                    nlgService = tempService
                    gr.Info(f"模型切换成功，当前：{nlgService.type.name}")
                    return nlgService.type.name
                except Exception:
                    gr.Warning("模型切换失败，请检查网络连接或模型配置")
                    return currentService


        async def create_and_save_vector_store(vector_store_name, file):
            model_name = "/root/projects/gpt2_cn/LLMs/text2vec-large-chinese"
            model_kwargs = {"device": "cpu"}
            hf = HuggingFaceEmbeddings(
                model_name=model_name, model_kwargs=model_kwargs
            )

            text_splitter = CharacterTextSplitter(
                separator="\n",
                chunk_size=100,
                chunk_overlap=0,
                length_function=len,
                is_separator_regex=False,
            )

            file_name = file.name
            filename = os.path.splitext(os.path.basename(file_name))[0]
            file_type = os.path.splitext(os.path.basename(file_name))[1]

            save_path = os.path.join(VECTOR_FILES_DIR, filename)

            # 保存文件
            shutil.copyfile(file.name, save_path)

            documents = []
            texts = None

            try:
                if file_type == ".pdf":
                    from langchain_community.document_loaders import PyPDFLoader
                    loader = PyPDFLoader(save_path)
                    documents = loader.load_and_split()
                else:
                    logging.debug("Loading text file...")
                    from langchain.document_loaders import TextLoader
                    loader = TextLoader(save_path, "utf8")
                    texts = loader.load()
                    documents = text_splitter.split_documents(texts)
            except Exception as e:
                import traceback
                logging.error(f"Error loading file: {filename}")
                traceback.print_exc()

            db = FAISS.from_documents(documents, hf)
            db.save_local(os.path.join(VECTOR_STORES_DIR, f"{vector_store_name}.faiss"))

            # 异步更新下拉列表选项
            async def update_dropdown():
                await asyncio.sleep(0.1)  # 等待一小段时间确保文件已保存
                select_vector_store.choices = list_vector_store()
                gr.Info(f"新知识库创建成功：{vector_store_name}")

            await update_dropdown()

            return db

        def construct_index(file):
            model_name = "/root/projects/gpt2_cn/LLMs/text2vec-large-chinese"
            model_kwargs = {"device": "cpu"}
            hf = HuggingFaceEmbeddings(
                model_name=model_name, model_kwargs=model_kwargs
            )

            text_splitter = CharacterTextSplitter(
                separator="\n",
                chunk_size=100,
                chunk_overlap=0,
                length_function=len,
                is_separator_regex=False,
            )

            file_name = file.name
            filename = os.path.splitext(os.path.basename(file_name))[0]
            file_type = os.path.splitext(os.path.basename(file_name))[1]

            save_path = os.path.join(VECTOR_FILES_DIR, filename)

            # 保存文件
            shutil.copyfile(file.name, save_path)

            documents = []
            texts = None

            try:
                if file_type == ".pdf":
                    from langchain_community.document_loaders import PyPDFLoader
                    loader = PyPDFLoader(save_path)
                    documents = loader.load_and_split()
                elif file_type == ".docx":
                    logging.debug("Loading Word...")
                    from langchain.document_loaders import UnstructuredWordDocumentLoader
                    loader = UnstructuredWordDocumentLoader(save_path)
                    texts = loader.load()
                    documents = text_splitter.split_documents(texts)
                elif file_type == ".pptx":
                    logging.debug("Loading PowerPoint...")
                    from langchain.document_loaders import UnstructuredPowerPointLoader
                    loader = UnstructuredPowerPointLoader(save_path)
                    texts = loader.load()
                    documents = text_splitter.split_documents(texts)
                elif file_type == ".epub":
                    logging.debug("Loading EPUB...")
                    from langchain.document_loaders import UnstructuredEPubLoader
                    loader = UnstructuredEPubLoader(save_path)
                    texts = loader.load()
                    documents = text_splitter.split_documents(texts)
                else:
                    logging.debug("Loading text file...")
                    from langchain.document_loaders import TextLoader
                    loader = TextLoader(save_path, "utf8")
                    texts = loader.load()
                    documents = text_splitter.split_documents(texts)
            except Exception as e:
                import traceback
                logging.error(f"Error loading file: {filename}")
                traceback.print_exc()

            db = FAISS.from_documents(documents, hf)

            db.save_local(os.path.join(VECTOR_STORES_DIR, f"{filename}.faiss"))
            gr.Info(f"临时文档加载完成: {filename} ")

            return filename


        def load_vector_store(vector_store_name):

            model_name = "/root/projects/gpt2_cn/LLMs/text2vec-large-chinese"
            model_kwargs = {"device": "cpu"}
            hf = HuggingFaceEmbeddings(
                model_name=model_name, model_kwargs=model_kwargs
            )
            db = FAISS.load_local(os.path.join(VECTOR_STORES_DIR, f"{vector_store_name}.faiss"), hf)
            # print(db)
            gr.Info(f"知识库切换成功，当前：{vector_store_name}")
            return db


        def search_similar_sentences(query, vector_store_name):
            print(f"Selected vector store name: {vector_store_name}")
            start_time = time.time()
            model_name = "/root/projects/gpt2_cn/LLMs/text2vec-large-chinese"
            model_kwargs = {"device": "cpu"}
            hf = HuggingFaceEmbeddings(
                model_name=model_name, model_kwargs=model_kwargs
            )
            embeddings = hf.embed_query(query)
            # print("query:", query)
            # print("embeddings:", embeddings)

            vector_store = load_vector_store(vector_store_name)
            docs = vector_store.similarity_search_by_vector(embeddings, k=3)
            end_time = time.time()
            similar_sentences = [doc.page_content for doc in docs]
            execution_time = end_time - start_time
            return similar_sentences, execution_time


        def vector_store_builder_and_search(query, vector_store_name, raw_documents=None):
            if raw_documents:
                create_and_save_vector_store(vector_store_name, raw_documents)
            vector_store = load_vector_store(vector_store_name)
            similar_sentences, execution_time = search_similar_sentences(query, vector_store)
            return similar_sentences, execution_time


        def list_vector_store():
            # 列出项目目录中的所有 FAISS 库
            vector_stores = [f.replace(".faiss", "") for f in os.listdir(VECTOR_STORES_DIR) if f.endswith(".faiss")]
            return vector_stores



        # 按钮绑定事件
        clearButton.click(cleanAllContent, [textInput, botComponent], [textInput, botComponent])
        submitButton.click(textChat, [textInput, botComponent, internetSwitch, knowledgebaseSwitch, docSwitch, select_vector_store], [textInput, botComponent, internetSwitch, knowledgebaseSwitch, docSwitch, select_vector_store])
        textInput.submit(textChat, [textInput, botComponent, internetSwitch, knowledgebaseSwitch, docSwitch, select_vector_store], [textInput, botComponent, internetSwitch, knowledgebaseSwitch, docSwitch, select_vector_store])
        # 切换模型
        nlgSwitch.change(switchNLG, [nlgSwitch], [nlgSwitch])

        select_vector_store.change(load_vector_store, [select_vector_store])
        build_button.click(create_and_save_vector_store, [vector_store_name, vector_store_file])
        load_button.click(construct_index, [vector_store_file], [select_vector_store])
        query.submit(search_similar_sentences, [query, select_vector_store],
                     [similar_sentences_output, execution_time_output])
        search_button.click(search_similar_sentences, [query, select_vector_store],
                            [similar_sentences_output, execution_time_output])


if __name__ == "__main__":
    demo.launch(server_name = '124.207.219.135')
