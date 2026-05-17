# 项目全局配置文件，新手无需修改
import os
from dotenv import load_dotenv

# 加载.env文件中的密钥
load_dotenv()

# 豆包Doubao配置
DOUBAO_API_KEY = os.getenv("DOUBAO_API_KEY")

# 数据库配置
DB_PATH = "errorbook.db"