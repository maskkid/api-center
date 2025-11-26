# 项目设计

1. 0-saas-center是之前一个完整项目，主要是flask，现在需要把这个项目，使用fastapi重新实现一遍。注意帮我改进架构设计。
2. 根目录有个config.yml文件，用于补充配置到 config.py中。config.py可能会有更多的配置。
3. 入口main.py，使用uvicorn.run 的方式运行。