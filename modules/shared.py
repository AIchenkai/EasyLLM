import argparse






# UI variables
gradio = {}


# Parser copied from https://github.com/vladmandic/automatic
parser = argparse.ArgumentParser(description="Text generation web UI", conflict_handler='resolve', add_help=True, formatter_class=lambda prog: argparse.HelpFormatter(prog, max_help_position=55, indent_increment=2, width=200))



# Gradio
group = parser.add_argument_group('Gradio')
group.add_argument('--listen', action='store_true', help='Make the web UI reachable from your local network.')
group.add_argument('--listen-port', type=int, help='The listening port that the server will use.')
group.add_argument('--listen-host', type=str, help='The hostname that the server will use.')
group.add_argument('--share', action='store_true', help='Create a public URL. This is useful for running the web UI on Google Colab or similar.')
group.add_argument('--auto-launch', action='store_true', default=False, help='Open the web UI in the default browser upon launch.')
group.add_argument('--gradio-auth', type=str, help='Set Gradio authentication password in the format "username:password". Multiple credentials can also be supplied with "u1:p1,u2:p2,u3:p3".', default=None)
group.add_argument('--gradio-auth-path', type=str, help='Set the Gradio authentication file path. The file should contain one or more user:password pairs in the same format as above.', default=None)
group.add_argument('--ssl-keyfile', type=str, help='The path to the SSL certificate key file.', default=None)
group.add_argument('--ssl-certfile', type=str, help='The path to the SSL certificate cert file.', default=None)