import gradio as gr

from modules import shared



def create_ui():
    mu = shared.args.multi_user

    shared.gradio['Chat input'] = gr.State()
    shared.gradio['history'] = gr.State({'internal': [], 'visible': []})

    with gr.Tab('Chat', elem_id='chat-tab', elem_classes=("old-ui" if shared.args.chat_buttons else None)):
        with gr.Row():
            with gr.Column(elem_id='chat-col'):
                shared.gradio['display'] = gr.HTML(value=chat_html_wrapper({'internal': [], 'visible': []}, '', '', 'chat', 'cai-chat', ''))

                with gr.Row(elem_id="chat-input-row"):
                    with gr.Column(scale=1, elem_id='gr-hover-container'):
                        gr.HTML(value='<div class="hover-element" onclick="void(0)"><span style="width: 100px; display: block" id="hover-element-button">&#9776;</span><div class="hover-menu" id="hover-menu"></div>', elem_id='gr-hover')

                    with gr.Column(scale=10, elem_id='chat-input-container'):
                        shared.gradio['textbox'] = gr.Textbox(label='', placeholder='Send a message', elem_id='chat-input', elem_classes=['add_scrollbar'])
                        shared.gradio['show_controls'] = gr.Checkbox(value=shared.settings['show_controls'], label='Show controls (Ctrl+S)', elem_id='show-controls')
                        shared.gradio['typing-dots'] = gr.HTML(value='<div class="typing"><span></span><span class="dot1"></span><span class="dot2"></span></div>', label='typing', elem_id='typing-container')

                    with gr.Column(scale=1, elem_id='generate-stop-container'):
                        with gr.Row():
                            shared.gradio['Stop'] = gr.Button('Stop', elem_id='stop', visible=False)
                            shared.gradio['Generate'] = gr.Button('Generate', elem_id='Generate', variant='primary')

        # Hover menu buttons
        with gr.Column(elem_id='chat-buttons'):
            with gr.Row():
                shared.gradio['Regenerate'] = gr.Button('Regenerate (Ctrl + Enter)', elem_id='Regenerate')
                shared.gradio['Continue'] = gr.Button('Continue (Alt + Enter)', elem_id='Continue')
                shared.gradio['Remove last'] = gr.Button('Remove last reply (Ctrl + Shift + Backspace)', elem_id='Remove-last')

            with gr.Row():
                shared.gradio['Replace last reply'] = gr.Button('Replace last reply (Ctrl + Shift + L)', elem_id='Replace-last')
                shared.gradio['Copy last reply'] = gr.Button('Copy last reply (Ctrl + Shift + K)', elem_id='Copy-last')
                shared.gradio['Impersonate'] = gr.Button('Impersonate (Ctrl + Shift + M)', elem_id='Impersonate')

            with gr.Row():
                shared.gradio['Send dummy message'] = gr.Button('Send dummy message')
                shared.gradio['Send dummy reply'] = gr.Button('Send dummy reply')

            with gr.Row():
                shared.gradio['send-chat-to-default'] = gr.Button('Send to default')
                shared.gradio['send-chat-to-notebook'] = gr.Button('Send to notebook')

        with gr.Row(elem_id='past-chats-row', elem_classes=['pretty_scrollbar']):
            with gr.Column():
                with gr.Row():
                    shared.gradio['unique_id'] = gr.Dropdown(label='Past chats', elem_classes=['slim-dropdown'], interactive=not mu)

                with gr.Row():
                    shared.gradio['rename_chat'] = gr.Button('Rename', elem_classes='refresh-button', interactive=not mu)
                    shared.gradio['delete_chat'] = gr.Button('🗑️', elem_classes='refresh-button', interactive=not mu)
                    shared.gradio['delete_chat-confirm'] = gr.Button('Confirm', variant='stop', visible=False, elem_classes='refresh-button')
                    shared.gradio['delete_chat-cancel'] = gr.Button('Cancel', visible=False, elem_classes='refresh-button')
                    shared.gradio['Start new chat'] = gr.Button('New chat', elem_classes='refresh-button')

                with gr.Row(elem_id='rename-row'):
                    shared.gradio['rename_to'] = gr.Textbox(label='Rename to:', placeholder='New name', visible=False, elem_classes=['no-background'])
                    shared.gradio['rename_to-confirm'] = gr.Button('Confirm', visible=False, elem_classes='refresh-button')
                    shared.gradio['rename_to-cancel'] = gr.Button('Cancel', visible=False, elem_classes='refresh-button')

        with gr.Row():
            shared.gradio['start_with'] = gr.Textbox(label='Start reply with', placeholder='Sure thing!', value=shared.settings['start_with'])

        with gr.Row():
            shared.gradio['mode'] = gr.Radio(choices=['chat', 'chat-instruct', 'instruct'], value='chat', label='Mode', info='Defines how the chat prompt is generated. In instruct and chat-instruct modes, the instruction template selected under Parameters > Instruction template must match the current model.', elem_id='chat-mode')
            shared.gradio['chat_style'] = gr.Dropdown(choices=utils.get_available_chat_styles(), label='Chat style', value=shared.settings['chat_style'], visible=shared.settings['mode'] != 'instruct')
