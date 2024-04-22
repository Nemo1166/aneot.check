from ollama_api import OllamaAPI
from utils import md_parser


def content_check(path, i, line):
    text = md_parser(line)